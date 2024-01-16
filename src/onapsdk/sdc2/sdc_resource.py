"""SDC resource module."""
#   Copyright 2024 Deutsche Telekom AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.from onapsdk.sdc2.sdc import ResoureTypeEnum
from abc import ABC, abstractmethod
from base64 import b64encode
from enum import Enum, auto
from itertools import chain
from typing import Any, Dict, Iterable, Sequence, Optional
from urllib.parse import urljoin

from onapsdk.exceptions import ResourceNotFound  # type: ignore
from onapsdk.sdc2.component_instance import ComponentInstance
from onapsdk.sdc2.sdc import SDC, ResoureTypeEnum, SDCCatalog
from onapsdk.sdc2.sdc_user import SdcUser
from onapsdk.utils.headers_creator import headers_sdc_artifact_upload  # type: ignore
from onapsdk.utils.jinja import jinja_env  # type: ignore
from onapsdk.sdc2.sdc_category import ResourceCategory, SdcSubCategory
from onapsdk.sdc.vendor import Vendor  # type: ignore
from onapsdk.sdc.vsp import Vsp  # type: ignore


class LifecycleOperation(Enum):  # pylint: disable=too-few-public-methods
    """Resources lifecycle operations enum."""

    CHECKOUT = "checkout"
    UNDO_CHECKOUT = "undoCheckout"
    CHECKIN = "checkin"
    CERIFICATION_REQUEST = "certificationRequest"
    START_CERTIFICATION = "startCertification"
    FAIL_CERTIFICATION = "failCertification"
    CANCEL_CERIFICATION = "cancelCertification"
    CERTIFY = "certify"


class LifecycleState(Enum):  # pylint: disable=too-few-public-methods
    """Resources lifecycle states enum."""

    def _generate_next_value_(name, *_, **__):  # pylint: disable=no-self-argument
        """Return the upper-cased version of the member name."""
        return name.upper()  # pylint: disable=no-member

    READY_FOR_CERTIFICATION = auto()
    CERTIFICATION_IN_PROGRESS = auto()
    CERTIFIED = auto()
    NOT_CERTIFIED_CHECKIN = auto()
    NOT_CERTIFIED_CHECKOUT = auto()


class SDCResource(SDCCatalog):  # pylint: disable=too-many-instance-attributes
    """SDC resource class."""

    LIFECYCLE_OPERATION_TEMPLATE = "sdc2_resource_action.json.j2"

    def __init__(self,  # pylint: disable=too-many-locals too-many-arguments
                 *,
                 name: str,
                 version: Optional[str] = None,
                 archived: Optional[bool] = None,
                 component_type: Optional[str] = None,
                 icon: Optional[str] = None,
                 unique_id: Optional[str] = None,
                 lifecycle_state: Optional[LifecycleState] = None,
                 last_update_date: Optional[int] = None,
                 uuid: Optional[str] = None,
                 invariant_uuid: Optional[str] = None,
                 system_name: Optional[str] = None,
                 tags: Optional[Sequence[str]] = None,
                 last_updater_user_id: Optional[str] = None,
                 creation_date: Optional[int] = None,
                 description: Optional[str] = None,
                 all_versions: Optional[Dict[str, Any]] = None) -> None:
        """SDC resource initialisation.

        Args:
            name (str): Resource name
            version (Optional[str], optional): Resource version.. Defaults to None.
            archived (Optional[bool], optional): Flag determines if resource object is archived.
                Defaults to None.
            component_type (Optional[str], optional): Component type. Defaults to None.
            icon (Optional[str], optional): Resource icon. Defaults to None.
            unique_id (Optional[str], optional): Resource unique ID. Defaults to None.
            lifecycle_state (Optional[LifecycleState], optional): Resoure lifecycle state.
                Defaults to None.
            last_update_date (Optional[int], optional): Resource last update timestamp.
                Defaults to None.
            uuid (Optional[str], optional): Resource UUID. Defaults to None.
            invariant_uuid (Optional[str], optional): Resource invariant UUID. Defaults to None.
            system_name (Optional[str], optional): Resource system name. Defaults to None.
            tags (Optional[Sequence[str]], optional): Resource tags. Defaults to None.
            last_updater_user_id (Optional[str], optional): Resource last updater user ID.
                Defaults to None.
            creation_date (Optional[int], optional): Resource creation timestamp. Defaults to None.
            description (Optional[str], optional): Resource description. Defaults to None.
            all_versions (Optional[Dict[str, Any]], optional): Dictionary with all resources
                versions. Defaults to None

        """
        super().__init__(name)
        self.version: Optional[str] = version
        self.archived: Optional[bool] = archived
        self.component_type: Optional[str] = component_type
        self.icon: Optional[str] = icon
        self.unique_id: Optional[str] = unique_id
        self.lifecycle_state: Optional[LifecycleState] = \
            LifecycleState(lifecycle_state) if lifecycle_state else None
        self.last_update_date: Optional[int] = last_update_date
        self.uuid: Optional[str] = uuid
        self.invariant_uuid: Optional[str] = invariant_uuid
        self.system_name: Optional[str] = system_name
        self.tags: Optional[Sequence[str]] = tags
        self.last_updater_user_id: Optional[str] = last_updater_user_id
        self.creation_data: Optional[int] = creation_date
        self.description: Optional[str] = description
        self.all_versions: Optional[Dict[str, Any]] = all_versions

    def __repr__(self) -> str:
        """SDC resource description.

        Returns:
            str: SDC resource object description

        """
        return f"{self.__class__.__name__.upper()}(name={self.name})"

    def _copy_object(self, obj: 'SDCCatalog') -> None:
        """
        Copy relevant properties from object.

        Args:
            obj (Sdc): the object to "copy"

        Raises:
            NotImplementedError: this is an abstract method.

        """
        self.__dict__ = obj.__dict__.copy()

    @classmethod
    def get_by_name(cls, name: str) -> "SDCResource":
        """Get resource by name.

        Filter all objects (archived and active) and get a latest one (with highest version)
            which name is equal to one we are looking for.

        Args:
            name (str): Name of a resource

        Raises:
            ResourceNotFound: Resource with given name not found.

        Returns:
            SDCResource: Resource with given name

        """
        try:
            searched_rough_data: Dict[str, Any] = next(
                iter(
                    sorted(
                        filter(
                            lambda obj: obj["name"] == name,
                            cls._get_all_rough()),
                        key=lambda obj: obj["version"],
                    reverse=True)
                )
            )
            return cls.get_by_name_and_version(
                searched_rough_data["name"],
                searched_rough_data["version"]
            )
        except StopIteration as exc:
            cls._logger.warning("%s %s doesn't exist in SDC", cls.__name__, name)
            raise ResourceNotFound from exc

    def delete(self) -> None:
        """Delete resource."""
        self.send_message(
            "DELETE",
            f"Delete {self.name} {self.__class__.__name__}",
            urljoin(self.base_back_url,
                    f"sdc2/rest/v1/catalog/{self.catalog_type()}/{self.unique_id}")
        )

    def archive(self) -> None:
        """Archive resource."""
        self.send_message(
            "POST",
            f"Archive {self.name} {self.__class__.__name__}",
            urljoin(self.base_back_url,
                    f"sdc2/rest/v1/catalog/{self.catalog_type()}/{self.unique_id}/archive")
        )

    @classmethod
    def _get_all_rough(cls) -> Iterable[Dict[str, Any]]:
        """Get all resources values dictionaries.

        Returns:
            Iterable[Dict[str, Any]]: API responses dictionaries of
                both active and archived resources

        """
        return chain(cls._get_active_rough(), cls._get_archived_rough())

    @classmethod
    def get_all(cls) -> Iterable["SDCResource"]:
        """Get all resources iterator.

        Yields:
            SDCResource: SDC resource

        """
        for rough_data in cls._get_all_rough():
            yield cls.get_by_name_and_version(rough_data["name"], rough_data["version"])

    @classmethod
    def _get_active_rough(cls) -> Iterable[Dict[str, Any]]:
        """Get all active resources values dictionaries.

        Yields:
            Dict[str, Any]: API response dictionary with values of active resource

        """
        yield from cls.filter_response_objects_by_resource_type(cls.send_message_json(
            "GET",
            f"Get all {cls.__name__.upper()}",
            urljoin(cls.base_back_url,
                    f"{cls.SCREEN_ENDPOINT}?{cls._build_exclude_types_query(cls.resource_type())}"),
        ))

    @classmethod
    def _get_archived_rough(cls) -> Iterable[Dict[str, Any]]:
        """Get all archived resources values dictionaries.

        Yields:
            Dict[str, Any]: API response dictionary with values of archived resource

        """
        yield from cls.filter_response_objects_by_resource_type(cls.send_message_json(
            "GET",
            f"Get archived {cls.__name__.upper()}",
            urljoin(cls.base_back_url, cls.ARCHIVE_ENDPOINT),
        ))

    @classmethod
    def _build_exclude_types_query(cls, type_to_not_exclude: ResoureTypeEnum) -> str:
        """Build query to exclude resource types from API request.

        There is no API to get a specific resource type from SDC backend, but it is possible
            to exclude some. So that method creates an HTTP query to exclude all types
            but not a one passed as a parameter.

        Args:
            type_to_not_exclude (ResoureTypeEnum): Type which won't be excluded from API
                request

        Returns:
            str: HTTP query

        """
        return "&".join([f"excludeTypes={exclude_type}" for exclude_type in
                         ResoureTypeEnum.iter_without_resource_type(type_to_not_exclude)])

    @classmethod
    @abstractmethod
    def filter_response_objects_by_resource_type(
        cls,
        response: Dict[str, Any]
    ) -> Iterable[Dict[str, Any]]:
        """Filter API response by resource type.

        An abstract method which has to be implemented by subclass

        Args:
            response (Dict[str, Any]): API response to filter

        Yields:
            Dict[str, Any]: Filtered API response values dictionary

        """

    @classmethod
    @abstractmethod
    def resource_type(cls) -> ResoureTypeEnum:
        """Resource object type.

        Abstract classmethod to be implemented.

        Returns:
            ResoureTypeEnum: Resource type

        """

    @classmethod
    @abstractmethod
    def create_from_api_response(cls, _: Dict[str, Any]) -> SDCCatalog:
        """Create resource with values from API response.

        Abstract classmethod to be implemented.

        Returns:
            SDCCatalog: Resource object.

        """

    @classmethod
    def catalog_type(cls) -> str:
        """Resource catalog type.

        Resources can have two catalog types:
         - services
         - resources
        That method returns a proper one for given resource type object class.

        Returns:
            str: Resource catalog type, "services" or "resources"
        """
        if cls.resource_type() == ResoureTypeEnum.SERVICE:
            return "services"
        return "resources"

    @classmethod
    def get_by_name_and_version_endpoint(cls, name: str, version: str) -> str:
        """Get an endpoint to be used to get resource by name and it's version.

        Args:
            name (str): Resource name
            version (str): Resource version

        Returns:
            str: An endpoint to be used to get resource object by name and version

        """
        return f"sdc2/rest/v1/catalog/resources/resourceName/{name}/resourceVersion/{version}"

    @classmethod
    def add_deployment_artifact_endpoint(cls, object_id: str) -> str:
        """Get an endpoint to add deployment artifact into object.

        Args:
            object_id (str): Object/resource ID

        Returns:
            str: An endpoint to be used to send request to add a deployment artifact into resource

        """
        return f"sdc2/rest/v1/catalog/resources/{object_id}/artifacts"

    @classmethod
    def get_by_name_and_version(cls, name: str, version: str) -> "SDCResource":
        """Get resource by name and version.

        Args:
            name (str): Resource name
            version (str): Resource version

        Returns:
            SDCResource: SDC resource object with given name and version

        Raises:
            ResourceNotFoundError: resource with given name and version
                does not exist

        """
        return cls.create_from_api_response(cls.send_message_json(
            "GET",
            f"Get {cls.__name__} by name and version",
            urljoin(cls.base_back_url, cls.get_by_name_and_version_endpoint(name, version))
        ))

    def update(self, api_response: Dict[str, Any]) -> None:
        """Update resource with values from API response dictionary.

        Args:
            api_response (Dict[str, Any]): API response dictionary with values
                used for object update

        """
        self.unique_id = api_response["uniqueId"]
        self.uuid = api_response["uuid"]
        self.invariant_uuid=api_response["invariantUUID"]
        self.version = api_response["version"]
        self.last_update_date = api_response["lastUpdateDate"]
        self.lifecycle_state = api_response["lifecycleState"]
        self.last_updater_user_id = api_response["lastUpdaterUserId"]
        self.all_versions = api_response["allVersions"]

    def lifecycle_operation(self, lifecycle_operation: LifecycleOperation) -> None:
        """Request lifecycle operation on an object.

        Args:
            lifecycle_operation (LifecycleOperation): Lifecycle operation to be requested.

        """
        response: Dict[str, Any] = self.send_message_json(
            "POST",
            (f"Request lifecycle operation {lifecycle_operation} on "
             f"{self.__class__.__name__.upper()} object {self.name}"),
            urljoin(self.base_back_url,
                    (f"sdc2/rest/v1/catalog/{self.catalog_type()}/"
                     f"{self.unique_id}/lifecycleState/{lifecycle_operation}")),
            data=jinja_env().get_template(
                self.LIFECYCLE_OPERATION_TEMPLATE).render(
                    lifecycle_operation=lifecycle_operation)
        )
        self.update(response)

    def add_deployment_artifact(self,  # pylint: disable=too-many-arguments
                                artifact_type: str,
                                artifact_label: str,
                                artifact_name: str,
                                artifact_file_path: str,
                                artifact_group_type: str = "DEPLOYMENT",
                                artifact_description: str = "ONAP SDK ARTIFACT"):
        """
        Add deployment artifact to resource.

        Add deployment artifact to resource using payload data.

        Args:
            artifact_type (str): all SDC artifact types are supported (DCAE_*, HEAT_*, ...)
            artifact_name (str): the artifact file name including its extension
            artifact (str): artifact file to upload
            artifact_label (str): Unique Identifier of the artifact within the VF / Service.

        Raises:
            StatusError: Resource has not DRAFT status

        """
        self._logger.debug("Add deployment artifact to %s %s",
                           self.__class__.__name__.upper(),
                           self.name)
        with open(artifact_file_path, 'rb') as artifact_file:
            data: bytes = artifact_file.read()
        artifact_upload_payload = jinja_env().get_template(
            "sdc2_add_deployment_artifact.json.j2").\
                render(artifact_group_type=artifact_group_type,
                       artifact_description=artifact_description,
                       artifact_name=artifact_name,
                       artifact_label=artifact_label,
                       artifact_type=artifact_type,
                       artifact_payload=b64encode(data).decode('utf-8'))

        self.send_message_json("POST",
                               ("Add deployment artifact to "
                                f"{self.__class__.__name__.upper()} {self.name}"),
                               urljoin(self.base_back_url,
                                       self.add_deployment_artifact_endpoint(self.unique_id)),
                               data=artifact_upload_payload,
                               headers=headers_sdc_artifact_upload(base_header=self.headers,
                                                                   data=artifact_upload_payload))

    @property
    def component_instances(self) -> Iterable["ComponentInstance"]:
        """Iterate through resource's component instances.

        Yields:
            ComponentInstance: Resource's component instance

        """
        for component_instance_dict in self.send_message_json(
            "GET",
            f"Get {self.__class__.__name__} component instances",
            urljoin(self.base_back_url,
                    (f"sdc2/rest/v1/catalog/{self.catalog_type()}/"
                     f"{self.unique_id}/componentInstances"))
        ):
            yield ComponentInstance.create_from_api_response(component_instance_dict, self)

    def get_component_by_name(self, name: str) -> Optional[ComponentInstance]:
        """Get resource's component instance by it's name.

        Args:
            name (str): Component instance's name

        Returns:
            Optional[ComponentInstance]: Component instance with given name,
                None if no component instance has given name

        """
        for component_instance in self.component_instances:
            if component_instance.component_name == name:
                return component_instance
        return None


class SDCResourceCreateMixin(ABC):  # pylint: disable=too-few-public-methods
    """SDC resource object creation mixin class.

    Not all resource object can be created (VL can't) so that's why that mixin was created.
    Object which inherits from that class has to implement:
     - send_message_json
     - create_from_api_response
     - get_create_payload
    methods.
    """

    CREATE_ENDPOINT = urljoin(SDC.base_back_url, "sdc2/rest/v1/catalog/resources")

    @classmethod
    def create(cls,
               name: str,
               *,
               user: Optional[SdcUser] = None,
               description: Optional[str] = None,
               **kwargs: Dict[Any, Any]) -> "SDCResource":
        """Create object.

        Args:
            name (str): Name of an object
            user (Optional[SdcUser], optional): Object creator user ID. Defaults to None.
            description (Optional[str], optional): Object description. Defaults to None.

        Returns:
            SDCResource: Created SDC resource object

        """
        return cls.create_from_api_response(cls.send_message_json(
            "POST",
            f"Create {cls.__name__.upper()} {name}",
            cls.CREATE_ENDPOINT,
            data=cls.get_create_payload(name=name, user=user, description=description, **kwargs)
        ))


class SDCResourceTypeObject(SDCResource, ABC):  # pylint: disable=too-few-public-methods
    """SDC resource type object class."""

    def __init__(self,  # pylint: disable=too-many-locals too-many-arguments
                 *,
                 name: str,
                 version: Optional[str] = None,
                 archived: Optional[bool] = None,
                 component_type: Optional[str] = None,
                 icon: Optional[str] = None,
                 unique_id: Optional[str] = None,
                 lifecycle_state: Optional[LifecycleState] = None,
                 last_update_date: Optional[int] = None,
                 category_normalized_name: Optional[str] = None,
                 sub_category_normalized_name: Optional[str] = None,
                 uuid: Optional[str] = None,
                 invariant_uuid: Optional[str] = None,
                 system_name: Optional[str] = None,
                 description: Optional[str] = None,
                 tags: Optional[Sequence[str]] = None,
                 last_updater_user_id: Optional[str] = None,
                 creation_date: Optional[int] = None,
                 all_versions: Optional[Dict[str, Any]] = None):
        """Initialise SDC resource type object.

        Args:
            name (str): SDC resource object name
            version (Optional[str], optional): SDC resource object version. Defaults to None.
            archived (Optional[bool], optional): Flag determines if object is archived.
                Defaults to None.
            component_type (Optional[str], optional): Resource component type. Defaults to None.
            icon (Optional[str], optional): Resource icon. Defaults to None.
            unique_id (Optional[str], optional): Resource unique ID. Defaults to None.
            lifecycle_state (Optional[LifecycleState], optional): SDC resource object lifecycle
                state. Defaults to None.
            last_update_date (Optional[int], optional): Last update timestamp. Defaults to None.
            category_normalized_name (Optional[str], optional): Category normalized name.
                Defaults to None.
            sub_category_normalized_name (Optional[str], optional): Subcategory normalized name.
                Defaults to None.
            uuid (Optional[str], optional): Object UUID. Defaults to None.
            invariant_uuid (Optional[str], optional): Object invariant UUID. Defaults to None.
            system_name (Optional[str], optional): System name. Defaults to None.
            description (Optional[str], optional): Resource description. Defaults to None.
            tags (Optional[Sequence[str]], optional): Sequence of object tags. Defaults to None.
            last_updater_user_id (Optional[str], optional): ID of user who is
                the latest object's updater. Defaults to None.
            creation_date (Optional[int], optional): Object's creation timestamp. Defaults to None.
            all_versions (Optional[Dict[str, Any]], optional): Dictionary with all resources
                versions. Defaults to None
        """
        super().__init__(
            name=name,
            version=version,
            archived=archived,
            component_type=component_type,
            icon=icon,
            unique_id=unique_id,
            lifecycle_state=lifecycle_state,
            last_update_date=last_update_date,
            uuid=uuid,
            invariant_uuid=invariant_uuid,
            system_name=system_name,
            tags=tags,
            last_updater_user_id=last_updater_user_id,
            creation_date=creation_date,
            description=description,
            all_versions=all_versions
        )
        self.category_nomalized_name = category_normalized_name
        self.sub_category_nomalized_name: Optional[str] = sub_category_normalized_name

    @classmethod
    def filter_response_objects_by_resource_type(
        cls,
        response: Dict[str, Any]
    ) -> Iterable[Dict[str, Any]]:
        """Filter object from response based on resource type.

        Args:
            response (Dict[str, Any]): Response dictionary

        Returns:
            Iterable[Dict[str, Any]]: Iterator object values dictionaries

        """
        for resource in response.get("resources", []):
            if resource.get("resourceType") == cls.resource_type().value:
                yield resource

    @classmethod
    def create_from_api_response(cls, api_response: Dict[str, Any]) -> "SDCResourceTypeObject":
        """Create SDC resource object using API response dictionary values.

        Args:
            api_response (Dict[str, Any]): API responses dictionary

        Returns:
            SDCResourceTypeObject: Object created using API response values.

        """
        return cls(
            archived=api_response["archived"],
            creation_date=api_response["creationDate"],
            component_type=api_response["componentType"],
            description=api_response["description"],
            icon=api_response["icon"],
            invariant_uuid=api_response["invariantUUID"],
            last_update_date=api_response["lastUpdateDate"],
            last_updater_user_id=api_response["lastUpdaterUserId"],
            lifecycle_state=api_response["lifecycleState"],
            name=api_response["name"],
            system_name=api_response["systemName"],
            tags=api_response["tags"],
            unique_id=api_response["uniqueId"],
            uuid=api_response["uuid"],
            version=api_response["version"],
        )


class SDCResourceTypeObjectCreateMixin(SDCResourceCreateMixin, ABC):
    """Mixin class to be used for SDC resource type object creation."""

    @classmethod
    @abstractmethod
    def create_payload_template(cls) -> str:
        """Get payload template to be used for creation request.

        Abstract classmethod

        Returns:
            str: Name of template to be used for payload creation

        """

    @classmethod
    def get_create_payload(cls,  # pylint: disable=too-many-arguments
                           name: str,
                           *,
                           vsp: Vsp,
                           vendor: Vendor,
                           user: Optional[SdcUser] = None,
                           description: Optional[str] = None,
                           category: Optional[ResourceCategory] = None,
                           subcategory: Optional[SdcSubCategory] = None) -> str:
        """Get a payload to create a resource.

        Args:
            vsp (Vsp): VSP object
            vendor (Vendor): Vendor object
            user (Optional[SdcUser], optional): User which be marked as a creator.
                If not given "cs0008" is going to be used. Defaults to None.
            description (Optional[str], optional): Resource description. Defaults to None.
            category (Optional[ResourceCategory], optional): Resource category.
                If not given (with subcategory) then "Generic: Network Service" is going to be used.
                Defaults to None.
            subcategory (Optional[SdcSubCategory], optional): Resource subcategory.
                Defaults to None.

        Returns:
            str: Resource creation payload

        """
        if not all([category, subcategory]):
            category = ResourceCategory.get_by_name("Generic")
            subcategory = category.get_subcategory("Network Service")
        return jinja_env().get_template(cls.create_payload_template()).render(
            name=name,
            vsp=vsp,
            vendor=vendor,
            category=category,
            subcategory=subcategory,
            user_id=user.user_id if user else "cs0008",
            description=description if description else "ONAP SDK Resource"
        )
