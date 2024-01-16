"""SDC service module."""
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
#   limitations under the License.
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Iterable, Iterator, Sequence, Optional, Set
from urllib.parse import urljoin

from onapsdk.configuration import settings  # type: ignore
from onapsdk.sdc2.sdc import SDC, ResoureTypeEnum
from onapsdk.sdc2.sdc_category import SdcCategory, ServiceCategory
from onapsdk.sdc2.sdc_resource import SDCResource, SDCResourceCreateMixin
from onapsdk.sdc2.sdc_user import SdcUser
from onapsdk.utils.jinja import jinja_env  # type: ignore


class ServiceInstantiationType(Enum):
    """Service instantiation type enum class.

    Service can be instantiated using `A-la-carte` or `Macro` flow.
    It has to be determined during design time. That class stores these
    two values to set during initialization.

    """

    A_LA_CARTE = "A-la-carte"
    MACRO = "Macro"


class ServiceDistribution(SDC):
    """Service distribution class."""

    DISTRIBUTED_DEPLOYMENT_STATUS = "Distributed"

    @dataclass
    class DistributionStatus:
        """Dataclass of service distribution status. Internal usage only."""

        component_id: str
        timestamp: str
        url: str
        status: str
        error_reason: str

        @property
        def failed(self) -> bool:
            """Flad to determine if distribution status is failed or not.

            If error reason of distribution status is not empty it doesn't mean
                always that distribution failed at all. On some cases that means
                that service was already distributed on that component. That's why
                we checks also if status is not "ALREADY_DEPLOYED".

            Returns:
                bool: True if distribution on component failed or not.

            """
            return self.error_reason != "null" and \
                self.status != "ALREADY_DEPLOYED"

    def __init__(self,  # pylint: disable=too-many-arguments
                 distribution_id: str,
                 timestamp: str,
                 user_id: str,
                 deployment_status: str) -> None:
        """Initialise service distribution class.

        Stores information about service distribution and is a source of truth
            if service is distributed or not.

        Args:
            distribution_id (str): Distribution ID
            timestamp (str): Distribution timestamp
            user_id (str): ID of user which requested distribution.
            deployment_status (str): Status of deployment

        """
        super().__init__(name=distribution_id)
        self.distribution_id: str = distribution_id
        self.timestamp: str = timestamp
        self.user_id: str = user_id
        self.deployment_status: str = deployment_status
        self._distribution_status_list: Optional[
            Sequence["self.DistributionStatus"]] = None  # type: ignore

    @property
    def distributed(self) -> bool:
        """Distribution status.

        Need to pass 3 tests:
         - deployment status of distribution it "Distributed"
         - service was distributed on all components listed
            on settings.SDC_SERVICE_DISTRIBUTION_COMPONENTS
         - there was no distribution error

         An order of tests is fixed to reduce SDC API calls.

        Returns:
            bool: True is service can be considered as distributed, False otherwise.

        """
        return all([
            self._deployment_status_test,
            self._distribution_components_test,
            self._no_distribution_errors_test
        ])

    @property
    def _deployment_status_test(self) -> bool:
        """Test to check a distribution deployment status.

        Passed if distribution status is equal to "Distributed"

        Returns:
            bool: True if distribution deployment status is equal to "Distributed".
                False otherwise

        """
        return self.deployment_status == self.DISTRIBUTED_DEPLOYMENT_STATUS

    @property
    def _distribution_components_test(self) -> bool:
        """Test to check if all required components were notified about distribution.

        List of required components can be configured via SDC_SERVICE_DISTRIBUTION_COMPONENTS
            setting value.

        Returns:
            bool: True if all required components were notified, False otherwise

        """
        notified_components_set: Set[str] = {
            distribution.component_id for distribution in self.distribution_status_list
        }
        return notified_components_set == set(settings.SDC_SERVICE_DISTRIBUTION_COMPONENTS)

    @property
    def _no_distribution_errors_test(self) -> bool:
        """Test to check if there is no error on any component distribution.

        Returns:
            bool: True if no error occured on any component distribution, False otherwise

        """
        return not list(filter(lambda obj: obj.failed,
                               self.distribution_status_list))

    @property
    def distribution_status_list(self) -> Sequence[DistributionStatus]:
        """List of distribution statuses.

        Returns:
            List[DistributionStatus]: List of distribution statuses.

        """
        if not self._distribution_status_list:
            self._distribution_status_list = [self.DistributionStatus(
                    component_id=distribution_status_dict["omfComponentID"],
                    timestamp=distribution_status_dict["timestamp"],
                    url=distribution_status_dict["url"],
                    status=distribution_status_dict["status"],
                    error_reason=distribution_status_dict["errorReason"]
                ) for distribution_status_dict in
                self.send_message_json(
                    "GET",
                    f"Get status of {self.distribution_id} distribution",
                    urljoin(self.base_back_url,
                            f"sdc2/rest/v1/catalog/services/distribution/{self.distribution_id}")
                ).get("distributionStatusList", [])
            ]
        return self._distribution_status_list



class Service(SDCResource, SDCResourceCreateMixin):
    """SDC service class."""

    ADD_RESOURCE_TEMPLATE = "sdc2_add_resource.json.j2"
    CREATE_ENDPOINT = urljoin(SDC.base_back_url, "sdc2/rest/v1/catalog/services")
    CREATE_SERVICE_TEMPLATE = "sdc2_create_service.json.j2"

    def __init__(self,  # pylint: disable=too-many-locals too-many-arguments
                 *,
                 name: str,
                 version: Optional[str] = None,
                 archived: Optional[bool] = None,
                 component_type: Optional[str] = None,
                 icon: Optional[str] = None,
                 unique_id: Optional[str] = None,
                 lifecycle_state: Optional[str] = None,
                 last_update_date: Optional[int] = None,
                 uuid: Optional[str] = None,
                 invariant_uuid: Optional[str] = None,
                 system_name: Optional[str] = None,
                 tags: Optional[Sequence[str]] = None,
                 last_updater_user_id: Optional[str] = None,
                 creation_date: Optional[int] = None,
                 description: Optional[str] = None,
                 actual_component_type: Optional[str] = None,
                 all_versions: Optional[Dict[str, str]] = None,
                 categories: Optional[Sequence[SdcCategory]] = None,
                 distribuition_status: Optional[str] = None,
                 instantiation_type: Optional[ServiceInstantiationType] = None) -> None:
        """Initialize service object.

        Args:
            name (str): Service name
            actual_component_type (Optional[str]): Service actual component type. Defaults to None.
            all_versions (Optional[Dict[str, str]]): Dictionary with all versions of service.
                Defaults to None.
            categories (Optional[List[SdcCategory]]): List with all serivce categories.
                Defaults to None.
            version (Optional[str], optional): Service version. Defaults to None.
            archived (Optional[bool], optional): Flag determines if service is archived or not.
                Defaults to None.
            component_type (Optional[str], optional): Service component type. Defaults to None.
            icon (Optional[str], optional): Service icon. Defaults to None.
            unique_id (Optional[str], optional): Service unique ID. Defaults to None.
            lifecycle_state (Optional[str], optional): Service lifecycle state. Defaults to None.
            last_update_date (Optional[int], optional): Service last update date. Defaults to None.
            uuid (Optional[str], optional): Service UUID. Defaults to None.
            invariant_uuid (Optional[str], optional): Service invariant UUID. Defaults to None.
            system_name (Optional[str], optional): Service system name. Defaults to None.
            tags (Optional[List[str]], optional): List with service tags. Defaults to None.
            last_updater_user_id (Optional[str], optional): ID of user who was last service
                updater. Defaults to None.
            creation_date (Optional[int], optional): Timestamp of service creation.
                Defaults to None.
            description (Optional[str], optional): Service description.
                Defaults to None.
            distribuition_status (Optional[str], optional): Service distribution status.
                Defaults to None.
        """
        super().__init__(
            name=name,
            archived=archived,
            version=version,
            icon=icon,
            component_type=component_type,
            unique_id=unique_id,
            uuid=uuid,
            lifecycle_state=lifecycle_state,
            last_update_date=last_update_date,
            tags=tags,
            invariant_uuid=invariant_uuid,
            system_name=system_name,
            creation_date=creation_date,
            last_updater_user_id=last_updater_user_id,
            description=description
        )
        self.actual_component_type: Optional[str] = actual_component_type
        self.all_versions: Optional[Dict[str, str]] = all_versions
        self.distribuition_status: Optional[str] = distribuition_status
        self.categories: Optional[Sequence[SdcCategory]] = categories
        self.instantiation_type: Optional[ServiceInstantiationType] = instantiation_type

    @classmethod
    def resource_type(cls) -> ResoureTypeEnum:
        """Service resource type enum value.

        Returns:
            ResoureTypeEnum: Service resource type enum value

        """
        return ResoureTypeEnum.SERVICE

    @classmethod
    def filter_response_objects_by_resource_type(
        cls,
        response: Dict[str, Any]
    ) -> Iterable[Dict[str, Any]]:
        """Filter list of objects returned by API by resource type.

        Return only "services" from API response to reduce objects to iterate.

        Args:
            response (Dict[str, Any]): API response dictionary

        Returns:
            Iterable[Dict[str, Any]]: Dictionaries containing only services data

        """
        return response.get("services", [])

    @classmethod
    def create_from_api_response(cls, api_response: Dict[str, Any]) -> "Service":  # type: ignore
        """Create Service using values from API response.

        Args:
            api_response (Dict[str, Any]): Dictionary with values returned by API.

        Returns:
            Service: Service object

        """
        return cls(
            actual_component_type=api_response["actualComponentType"],
            all_versions=api_response["allVersions"],
            creation_date=api_response["creationDate"],
            version=api_response["version"],
            component_type=api_response["componentType"],
            unique_id=api_response["uniqueId"],
            icon=api_response["icon"],
            lifecycle_state=api_response["lifecycleState"],
            last_update_date=api_response["lastUpdateDate"],
            name=api_response["name"],
            invariant_uuid=api_response["invariantUUID"],
            distribuition_status=api_response["distributionStatus"],
            description=api_response["description"],
            uuid=api_response["uuid"],
            system_name=api_response["systemName"],
            tags=api_response["tags"],
            last_updater_user_id=api_response["lastUpdaterUserId"],
            archived=api_response["archived"],
            categories=[ServiceCategory.get_by_uniqe_id(response_category["uniqueId"])
                        for response_category in api_response["categories"]],
            instantiation_type=ServiceInstantiationType(api_response["instantiationType"])
        )

    def update(self, api_response: Dict[str, Any]) -> None:
        """Update service with values from API response.

        Args:
            api_response (Dict[str, Any]): API response dictionary which values from are going to
                be used to update service object

        """
        super().update(api_response)
        self.distribuition_status = api_response["distributionStatus"]

    @classmethod
    def get_create_payload(cls,  # pylint: disable=arguments-differ too-many-arguments
                           name: str,
                           *,
                           user: Optional[SdcUser] = None,
                           description: Optional[str] = None,
                           category: Optional[ServiceCategory] = None,
                           instantiation_type: ServiceInstantiationType = \
                            ServiceInstantiationType.MACRO) -> str:
        """Get a payload to be sued for service creation.

        Args:
            name (str): Name of the service to be created
            user (Optional[SdcUser], optional): User which will be marked as a creaton. If no user
                is passed then 'cs0008' user ID is going to be used. Defaults to None.
            description (Optional[str], optional): Service description. Defaults to None.
            category (Optional[ServiceCategory], optional): Service category.
                If no category is given then "Network Service" is going to be used.
                Defaults to None.

        Returns:
            str: Service creation API payload.

        """
        return jinja_env().get_template(cls.CREATE_SERVICE_TEMPLATE).render(
            name=name,
            category=category if category else ServiceCategory.get_by_name("Network Service"),
            user_id=user.user_id if user else "cs0008",
            description=description if description else "ONAP SDK Service",
            instantiation_type=instantiation_type)

    def add_resource(self, resource: SDCResource) -> None:
        """Add resource into service composition.

        Args:
            resource (SDCResource): Resource to be added into service.

        """
        self.send_message(
            "POST",
            f"Add resource {resource.name} into service {self.name}",
            urljoin(self.base_back_url,
                    f"sdc2/rest/v1/catalog/services/{self.unique_id}/resourceInstance/"),
            data=jinja_env().get_template(self.ADD_RESOURCE_TEMPLATE).render(resource=resource)
        )

    def distribute(self, env: str = "PROD") -> None:
        """Distribute service.

        Call a request to distribute service. If no error was returned then service is updated
            using values returned by API.
        SDC allows to distribute services on different environments. By default that method
            distribute service on "PROD" environment.

        Args:
            env (str, optional): Environment to distribute service on. Defaults to "PROD".

        """
        response: Dict[str, Any] = self.send_message_json(
            "POST",
            f"Request distribute Service {self.name}",
            urljoin(self.base_back_url,
                    f"sdc2/rest/v1/catalog/services/{self.unique_id}/distribution/{env}/activate")
        )
        self.update(response)

    @classmethod
    def catalog_type(cls) -> str:
        """Service type resource catalog type.

        SDC resources has two catalog types: resources and services. To create
            API endpoints which can be used by both that classmethod is overwriten
            by Service class.

        Returns:
            str: Service catalog type

        """
        return "services"

    @classmethod
    def get_by_name_and_version_endpoint(cls, name: str, version: str) -> str:
        """Get an endpoint to call a request to get service by it's name and version.

        Service has different endpoint that other resources to send a request
            to get an object by it's name and version.

        Args:
            name (str): Service name
            version (str): Service version

        Returns:
            str: Endpoint to call a request to get service by it name and version

        """
        return f"sdc2/rest/v1/catalog/services/serviceName/{name}/serviceVersion/{version}"

    @classmethod
    def add_deployment_artifact_endpoint(cls, object_id: str) -> str:
        """Get an endpoint to add a deployment artifact into service.

        Service has different endpoint to send a request for adding
            a deployment artifact.

        Args:
            object_id (str): Service object ID to create an endpoint for

        Returns:
            str: Endpoint used to send request to add deployment artifact

        """
        return f"sdc2/rest/v1/catalog/services/{object_id}/artifacts"

    @property
    def distributions(self) -> Iterator[ServiceDistribution]:
        """Get service distributions.

        Service can be distributed multiple times. That property
            returns and iterable object which returns all
            distributions in reversed order we get it from API,
            so first distribution would be the latest one, not the first
            distribution call as it was in API.

        Returns:
            Iterable[ServiceDistribution]: Service distributions iterator

        """
        for distribution_status_dict in reversed(self.send_message_json(
            "GET",
            f"Request Service {self.name} distributions",
            urljoin(self.base_back_url, f"sdc2/rest/v1/catalog/services/{self.uuid}/distribution/")
        ).get("distributionStatusOfServiceList", [])):
            yield ServiceDistribution(distribution_status_dict["distributionID"],
                                      distribution_status_dict["timestamp"],
                                      distribution_status_dict["userId"],
                                      distribution_status_dict["deployementStatus"])

    @property
    def latest_distribution(self) -> Optional[ServiceDistribution]:
        """Get the latest distribution of the service.

        Returns:
            ServiceDistribution|None: Latest service distribution or
                None if service was not distrubuted
        """
        try:
            return next(self.distributions)
        except StopIteration:
            return None

    @property
    def distributed(self) -> bool:
        """Distributed property.

        Return boolean value which determines if serivce was distributed or not.
            It checks if latest distribution of service was successfull.

        Returns:
            bool: True is service was distributed correctly, False otherwise.
        """
        if (latest_distribution := self.latest_distribution) is not None:
            return latest_distribution.distributed
        return False
