"""SDC onboarding API module."""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterator, Optional, Type
from urllib.parse import urljoin

from onapsdk.configuration import settings
from onapsdk.sdc2.sdc import SDC
from onapsdk.exceptions import ResourceNotFound
from onapsdk.utils.jinja import jinja_env  # type: ignore


class SdcOnboardingApiItemTypeEnum(Enum):
    """Onboarding API item type enum."""

    VLM = "vlm"
    VSP = "vsp"


class SdcOnboardingApiVersionStatus(Enum):
    """Onboarding API item version status enum."""

    DRAFT = "Draft"
    LOCKED = "Locked"
    CERTIFIED = "Certified"
    DEPRECATED = "Deprecated"
    DELETED = "Deleted"


class SdcOnboardingApiItemStatus(Enum):
    """Onboarding API item status enum."""

    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"


class SdcOnboardingApiItemAction(Enum):
    """Onboarding API item action."""

    ARCHIVE = "ARCHIVE"
    RESTORE = "RESTORE"


class SdcOnboardingApiItemVersionAction(Enum):
    """Onboarding API item version action."""

    SYNC = "Sync"
    COMMIT = "Commit"
    REVERT = "Revert"
    RESET = "Reset"
    CLEAN = "Clean"


class SdcOnboardingApi(SDC, ABC):
    """SDC onboarding API abstract class."""

    base_onboarding_back_url = settings.SDB_ONBOARDING_BE_URL

    @classmethod
    def get_raw_items(cls,
                      item_type: Optional[SdcOnboardingApiItemTypeEnum] = None) -> Iterator[dict]:
        """Get onboarding API raw items.

        Args:
            item_type (SdcOnboardingApiItemTypeEnum | None, optional): Item type. Defaults to None.

        Yields:
            Iterator[dict]: JSON object of an onboarding API item.
        """
        params = None
        if item_type is not None:
            params = {
                "itemType": item_type.value
            }
        yield from cls.send_message_json(
                "GET",
                "Get all version software license",
                urljoin(cls.base_onboarding_back_url,
                        "onboarding-api/v1.0/items"),
                params=params).get("results", [])


class SdcOnboardingApiItemVersion(SdcOnboardingApi):
    """SDC onboarding API item class."""

    def __init__(self,  # pylint: disable=too-many-arguments
                 name: str,
                 version_id: str,
                 description: str,
                 status: SdcOnboardingApiVersionStatus,
                 creation_time: int,
                 modification_time: int,
                 additional_info: dict):
        """Init onboarding api item version object.

        Args:
            version_id (str): Version ID
            description (str): Version description
            status (SdcOnboardingApiVersionStatus): Versions status
            creation_time (int): Version creation time
            modification_time (int): Version modification time
            additional_info (dict): Additional info
        """
        super().__init__(name)
        self.version_id: str = version_id
        self.description: str = description
        self.status: SdcOnboardingApiVersionStatus = status
        self.creation_time: int = creation_time
        self.modification_time: int = modification_time
        self.additional_info: dict = additional_info

    def __repr__(self) -> str:
        """Creta item version object human readable repr string."""
        return f"ItemVersion(name={self.name}, status={self.status.value})"

    @classmethod
    def create_from_api_response(cls, api_response: dict) -> "SdcOnboardingApiItemVersion":
        """Create an onboarding API object from API response.

        Args:
            api_response (dict): Onboarding API response dictionary.

        Returns:
            SdcOnboardingApiItemVersion: Created version object.

        """
        return SdcOnboardingApiItemVersion(
            name=api_response["name"],
            version_id=api_response["id"],
            description=api_response["description"],
            status=SdcOnboardingApiVersionStatus(api_response["status"]),
            creation_time=api_response["creationTime"],
            modification_time=api_response["modificationTime"],
            additional_info=api_response["additionalInfo"]
        )


class SdcOnboardingApiItem(SdcOnboardingApi, ABC):
    """Abstract SDC onboarding API Item class."""

    subclass_registry: dict = {}
    sdc_onboarding_api_item_action_template: str = "sdc2_action_onboarding_api_item.json.j2"
    sdc_onboarding_api_item_submit_template: str = "sdc2_action_onboarding_api_item_submit.json.j2"

    def __init__(self,  # pylint: disable=too-many-arguments
                 name: str,
                 item_type: str,
                 item_id: str,
                 description: str,
                 owner: str,
                 status: str,
                 properties: dict):
        """Onboarding item init.

        Args:
            item_type (str): Item type
            item_id (str): Item id
            description (str): Item description
            owner (str): Item owner
            status (str): Item status
            properties (dict): Item properties
        """
        super().__init__(name)
        self.type: str = item_type
        self.item_id: str = item_id
        self.description: str = description
        self.owner: str = owner
        self.status: SdcOnboardingApiItemStatus = SdcOnboardingApiItemStatus(status)
        self.properties: dict = properties
        self._version: Optional[str] = None

    def __init_subclass__(cls):
        """Init a subclass.
        
        During subclass init a subclass registry is going to be filled
            with a valid item and a class object.

        """
        super().__init_subclass__()
        cls.subclass_registry[cls.get_item_type()] = cls

    @classmethod
    @abstractmethod
    def get_item_type(cls) -> SdcOnboardingApiItemTypeEnum:
        """Get an item type."""

    @classmethod
    def create_from_response(cls, api_response: dict) -> "SdcOnboardingApiItem":
        """Create an item from response.

        Args:
            api_response (dict): Item API response object.

        Returns:
            SdcOnboardingApiItem: Item object

        """
        subclass: Type[SdcOnboardingApiItem] = cls.subclass_registry[cls.get_item_type()]
        return subclass(
            api_response["name"],
            api_response["type"],
            api_response["id"],
            api_response["description"],
            api_response["owner"],
            api_response["status"],
            api_response["properties"]
        )

    @classmethod
    def get_item_url(cls, item_id: str) -> str:
        """Item url.

        Args:
            item_id (str): Item id to generate url for.

        Returns:
            str: Item url

        """
        return urljoin(cls.base_onboarding_back_url,
                       f"onboarding-api/v1.0/items/{item_id}/")

    @classmethod
    def get_raw_item(cls, item_id: str) -> dict:
        """Get the raw item dictionary.

        Args:
            item_id (str): Item to get raw object id.

        Returns:
            dict: Item dictionary.

        """
        return cls.send_message_json(
            "GET",
            "Get all version software license",
            cls.get_item_url(item_id))

    @property
    @abstractmethod
    def url(self) -> str:
        """Object's url."""

    @property
    def latest_version_url(self) -> str:
        """Url to latest object version.

        The difference is that SDC has two endpoints:
            * to item version -- more generic
            * to object version -- specific object version url.
        These are not the same!

        Returns:
            str: Latest version url

        """
        return urljoin(self.url,
                       f"versions/{self.latest_version.version_id}/")

    @property
    def latest_item_version_url(self) -> str:
        """An url to the latest item version.

        Returns:
            str: Url

        """
        return urljoin(self.get_item_url(self.item_id),
                       f"versions/{self.latest_version.version_id}/")

    @property
    def versions(self) -> Iterator[SdcOnboardingApiItemVersion]:
        """Get all item versions.

        Yields:
            Iterator[SdcOnboardingApiItemVersion]: Item version object.

        """
        for raw_version in self.send_message_json(
                "GET",
                "Get all version software license",
                urljoin(self.get_item_url(self.item_id), "versions/")).get("results", []):
            yield SdcOnboardingApiItemVersion.create_from_api_response(raw_version)

    @property
    def latest_version(self) -> SdcOnboardingApiItemVersion:
        """Get the latest version of an item."""
        return next(iter(sorted(self.versions, key=lambda version: version.creation_time)))

    @classmethod
    def get_all(cls) -> Iterator["SdcOnboardingApiItem"]:
        """Get all items.

        Yields:
            SdcOnboardingApiItem: Item object.

        """
        subclass: Type[SdcOnboardingApiItem] = cls.subclass_registry[cls.get_item_type()]
        for raw_item in cls.get_raw_items(cls.get_item_type()):
            yield subclass.create_from_response(raw_item)

    @classmethod
    def get_by_name(cls, name: str) -> "SdcOnboardingApiItem":
        """Get an item by name.

        Args:
            name (str): Name to get an item by.

        Raises:
            ResourceNotFound: Item with given name not found.

        Returns:
            SdcOnboardingApiItem: Item with given name

        """
        subclass: Type[SdcOnboardingApiItem] = cls.subclass_registry[cls.get_item_type()]
        for item in subclass.get_all():
            if item.name == name:
                return item
        raise ResourceNotFound(f"{subclass.get_item_type()} with {name} name not found")

    def update(self):
        """Update an item status."""
        updated_version: SdcOnboardingApiItem = self.get_by_name(self.name)
        self.status = updated_version.status

    def _action(self, item_action: SdcOnboardingApiItemAction):
        """Perform an item action.

        Args:
            item_action (SdcOnboardingApiItemAction): Action to perform

        """
        self.send_message(
            "PUT",
            f"Perform {item_action.value} on {self.item_id} {self.get_item_type()}",
            urljoin(self.get_item_url(self.item_id), "actions"),
            data=jinja_env().get_template(self.sdc_onboarding_api_item_action_template).render(
                action=item_action.value
            )
        )
        self.update()

    def archive(self):
        """Archive an item."""
        self._action(SdcOnboardingApiItemAction.ARCHIVE)

    def restore(self):
        """Restore an item."""
        self._action(SdcOnboardingApiItemAction.RESTORE)

    def _version_action(self, version_acton: SdcOnboardingApiItemVersionAction):
        """Perform a version action.

        Args:
            version_acton (SdcOnboardingApiItemVersionAction): Version action to perform

        """
        self.send_message(
            "PUT",
            f"Perform {version_acton.value} action on {self.item_id} "
            f"{self.get_item_type()} version",
            urljoin(self.latest_item_version_url, "actions"),
            data=jinja_env().get_template(self.sdc_onboarding_api_item_action_template).render(
                action=version_acton.value
            )
        )
        self.update()

    def commit_version(self):
        """Commit version."""
        self._version_action(SdcOnboardingApiItemVersionAction.COMMIT)

    def submit(self, submit_request_message: str = "ONAP SDK SDC onboarding API submit"):
        """Perform a submit action on latest item version.

        Args:
            submit_request_message (str, optional): Submit action description.
                Defaults to "ONAP SDK SDC onboarding API submit".
        """
        self.send_message_json(
            "PUT",
            f"Submit {self.name} {self.get_item_type()}",
            urljoin(self.latest_version_url, "actions"),
            data=jinja_env().get_template(
                self.sdc_onboarding_api_item_submit_template).render(
                    submit_request_message=submit_request_message)
        )
        self.update()

    def delete(self):
        """Delete onboarding API item."""
        self.send_message(
            "DELETE",
            f"Delete {self.name} {self.get_item_type()}",
            self.url
        )
