"""SDC onboarding API vsp module."""
from urllib.parse import urljoin
from typing import BinaryIO

from onapsdk.exceptions import ValidationError
from onapsdk.sdc2.sdc_onboarding_api import SdcOnboardingApiItem, SdcOnboardingApiItemTypeEnum
from onapsdk.sdc2.vendor import Vendor
from onapsdk.utils.jinja import jinja_env  # type: ignore


class Vsp(SdcOnboardingApiItem):
    """VSP class."""

    vsp_create_template: str = "sdc2_create_vsp.json.j2"
    vsp_create_package_template: str = "sdc2_action_onboarding_api_item.json.j2"

    def __init__(self, name, item_type, item_id, description, owner, status, properties):  # pylint: disable=too-many-arguments
        """Init VSP object."""
        super().__init__(name, item_type, item_id, description, owner, status, properties)
        self._csar_uuid: str = None

    @classmethod
    def get_item_type(cls) -> SdcOnboardingApiItemTypeEnum:
        """Get VSP item type."""
        return SdcOnboardingApiItemTypeEnum.VSP

    @classmethod
    def create(cls,  # pylint: disable=too-many-arguments
               name: str,
               vendor: Vendor,
               category: str = "resourceNewCategory.generic",
               subcategory: str = "resourceNewCategory.generic.abstract",
               description: str = "ONAP SDK VSP",
               onboarding_method: str = "NetworkPackage") -> "Vsp":
        """Create VSP.

        Args:
            name (str): VSP name
            vendor (Vendor): Vendor object.
            category (str, optional): VSP category. Defaults to "resourceNewCategory.generic".
            subcategory (str, optional): VSP subcategory.
                Defaults to "resourceNewCategory.generic.abstract".
            description (str, optional): VSP description. Defaults to "ONAP SDK VSP".
            onboarding_method (str, optional): VSP onboarding method. Defaults to "NetworkPackage".

        Returns:
            Vsp: Created VSP object

        """
        cls._logger.info("Create %s VSP", name)
        response: dict = cls.send_message_json(
            "POST",
            f"Create {name} Vendor",
            urljoin(cls.base_onboarding_back_url,
                    "onboarding-api/v1.0/vendor-software-products"),
            data=jinja_env().get_template(
                cls.vsp_create_template).render(
                    name=name,
                    description=description,
                    vendor=vendor,
                    category=category,
                    subcategory=subcategory,
                    onboarding_method=onboarding_method)
        )
        return cls.create_from_response(cls.get_raw_item(response["itemId"]))

    @property
    def url(self) -> str:
        """Generate VSP url.

        Returns:
            str: VSP url

        """
        return urljoin(self.base_onboarding_back_url,
                       f"onboarding-api/v1.0/vendor-software-products/{self.vsp_id}/")

    @property
    def vsp_id(self) -> str:
        """Get VSP's ID.

        Returns:
            str: Get VSP ID

        """
        return self.item_id

    @property
    def vendor(self) -> Vendor:
        """Get VSP's vendor related object.

        Returns:
            Vendor: VSP's vendor related object.

        """
        return Vendor.get_by_name(self.properties["vendorName"])

    @property
    def csar_uuid(self) -> str:
        """Get VSP package id."""
        if not self._csar_uuid:
            self.create_package()
        return self._csar_uuid

    def upload_package(self, package: BinaryIO) -> None:
        """Upload VSP package."""
        self._logger.info("Upload package")
        headers = self.headers.copy()
        headers.pop("Content-Type")
        headers["Accept-Encoding"] = "gzip, deflate"
        self.send_message(
            "POST",
            f"Upload package for {self.name} VSP",
            urljoin(self.latest_version_url, "orchestration-template-candidate"),
            headers=headers,
            files={'upload': package}
        )

    def process_package(self, raise_on_failure: bool = False) -> None:
        """Process VSP package."""
        self._logger.info("Process package")
        process_report: dict = self.send_message_json(
            "PUT",
            f"Process {self.name} VSP package",
            urljoin(self.latest_version_url, "orchestration-template-candidate/process")
        )
        status: str = process_report.get("status", "")
        if status.upper() != "SUCCESS":
            if raise_on_failure:
                raise ValidationError("VSP file cannot be processed")
            self._logger.error("VSP file processing error!")

    def create_package(self):
        """Create VSP package."""
        response: dict = self.send_message_json(
            "PUT",
            f"Create package for {self.name} {self.get_item_type()}",
            urljoin(self.latest_version_url, "actions"),
            data=jinja_env().get_template(
                self.vsp_create_package_template).render(
                    action="Create_Package")
        )
        self.update()
        self._csar_uuid = response["packageId"]
