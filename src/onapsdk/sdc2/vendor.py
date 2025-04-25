"""Vendor module."""
from urllib.parse import urljoin

from onapsdk.sdc2.sdc_onboarding_api import SdcOnboardingApiItem, SdcOnboardingApiItemTypeEnum
from onapsdk.utils.jinja import jinja_env  # type: ignore


class Vendor(SdcOnboardingApiItem):
    """Vendor class."""

    vendor_create_template: str = "sdc2_create_vendor.json.j2"
    vendor_submit_template: str = "sdc2_submit_vendor.json.j2"

    def __repr__(self) -> str:
        """Get Vendor object human readable repr string."""
        return f"Vendor(name={self.name}, status={self.status.value})"

    @classmethod
    def get_item_type(cls) -> SdcOnboardingApiItemTypeEnum:
        """Get vendor item type."""
        return SdcOnboardingApiItemTypeEnum.VLM

    @classmethod
    def create(cls,
               name: str,
               description: str = "Python ONAP SDK Vendor",
               icon_ref: str = "icon") -> "Vendor":
        """Create vendor.

        Args:
            name (str): Vendor name
            description (str, optional): Vendor description. Defaults to "Python ONAP SDK Vendor".
            icon_ref (str, optional): Vendor icon. Defaults to "icon".

        Returns:
            Vendor: Created vendor object

        """
        cls._logger.info("Create %s Vendor", name)
        response: dict = cls.send_message_json(
            "POST",
            f"Create {name} Vendor",
            urljoin(cls.base_onboarding_back_url,
                    "onboarding-api/v1.0/vendor-license-models"),
            data=jinja_env().get_template(
                cls.vendor_create_template).render(
                    name=name,
                    description=description,
                    icon_ref=icon_ref)
        )
        return cls.create_from_response(cls.get_raw_item(response["itemId"]))

    @property
    def url(self) -> str:
        """Vendor url."""
        return urljoin(self.base_onboarding_back_url,
                       f"onboarding-api/v1.0/vendor-license-models/{self.vendor_id}/")

    @property
    def vendor_id(self) -> str:
        """Vendor ID."""
        return self.item_id
