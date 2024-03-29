"""A&AI Complex module."""
#   Copyright 2022 Orange, Deutsche Telekom AG
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
from typing import Any, Dict, Iterator
from urllib.parse import urlencode

from onapsdk.utils.jinja import jinja_env

from ..aai_element import AaiResource
from ..mixins.link_to_geo_region import AaiResourceLinkToGeoRegionMixin


class Complex(AaiResource, AaiResourceLinkToGeoRegionMixin):  # pylint: disable=too-many-instance-attributes
    """Complex class.

    Collection of physical locations that can house cloud-regions.
    """

    def __init__(self,  # NOSONAR  # pylint: disable=too-many-locals, too-many-arguments
                 physical_location_id: str,
                 *,
                 name: str = "",
                 data_center_code: str = "",
                 identity_url: str = "",
                 resource_version: str = "",
                 physical_location_type: str = "",
                 street1: str = "",
                 street2: str = "",
                 city: str = "",
                 state: str = "",
                 postal_code: str = "",
                 country: str = "",
                 region: str = "",
                 latitude: str = "",
                 longitude: str = "",
                 elevation: str = "",
                 lata: str = "",
                 timezone: str = "",
                 data_owner: str = "",
                 data_source: str = "",
                 data_source_version: str = "") -> None:
        """Complex object initialization.

        Args:
            name (str): complex name
            physical_location_id (str): complex ID
            data_center_code (str, optional): complex data center code. Defaults to "".
            identity_url (str, optional): complex identity url. Defaults to "".
            resource_version (str, optional): complex resource version. Defaults to "".
            physical_location_type (str, optional): complex physical location type. Defaults to "".
            street1 (str, optional): complex address street part one. Defaults to "".
            street2 (str, optional): complex address street part two. Defaults to "".
            city (str, optional): complex address city. Defaults to "".
            state (str, optional): complex address state. Defaults to "".
            postal_code (str, optional): complex address postal code. Defaults to "".
            country (str, optional): complex address country. Defaults to "".
            region (str, optional): complex address region. Defaults to "".
            latitude (str, optional): complex geographical location latitude. Defaults to "".
            longitude (str, optional): complex geographical location longitude. Defaults to "".
            elevation (str, optional): complex elevation. Defaults to "".
            lata (str, optional): complex lata. Defaults to "".
            timezone (str, optional): the time zone where the complex is located. Defaults to "".
            data_owner (str, optional): Identifies the entity that is responsible managing this
                inventory object. Defaults to "".
            data_source (str, optional): Identifies the upstream source of the data. Defaults to "".
            data_source_version (str, optional): Identifies the version of the upstream source.
                Defaults to "".

        """
        super().__init__()
        self.name: str = name
        self.physical_location_id: str = physical_location_id
        self.data_center_code: str = data_center_code
        self.identity_url: str = identity_url
        self.resource_version: str = resource_version
        self.physical_location_type: str = physical_location_type
        self.street1: str = street1
        self.street2: str = street2
        self.city: str = city
        self.state: str = state
        self.postal_code: str = postal_code
        self.country: str = country
        self.region: str = region
        self.latitude: str = latitude
        self.longitude: str = longitude
        self.elevation: str = elevation
        self.lata: str = lata
        self.timezone: str = timezone
        self.data_owner: str = data_owner
        self.data_source: str = data_source
        self.data_source_version: str = data_source_version

    def __repr__(self) -> str:
        """Complex object description.

        Returns:
            str: Complex object description

        """
        return (f"Complex(name={self.name}, "
                f"physical_location_id={self.physical_location_id}, "
                f"resource_version={self.resource_version})")

    @property
    def url(self) -> str:
        """Complex url.

        Returns:
            str: Complex url

        """
        return (f"{self.base_url}{self.api_version}/cloud-infrastructure/complexes/complex/"
                f"{self.physical_location_id}")

    @classmethod
    def create(cls,  # NOSONAR  # pylint: disable=too-many-locals, too-many-arguments
               physical_location_id: str,
               *,
               name: str = "",
               data_center_code: str = "",
               identity_url: str = "",
               resource_version: str = "",
               physical_location_type: str = "",
               street1: str = "",
               street2: str = "",
               city: str = "",
               state: str = "",
               postal_code: str = "",
               country: str = "",
               region: str = "",
               latitude: str = "",
               longitude: str = "",
               elevation: str = "",
               lata: str = "",
               timezone: str = "",
               data_owner: str = "",
               data_source: str = "",
               data_source_version: str = "") -> "Complex":
        """Create complex.

        Create complex object by calling A&AI API.
        If API request doesn't fail it returns Complex object.

        Returns:
            Complex: Created complex object

        """
        complex_object: Complex = Complex(
            name=name,
            physical_location_id=physical_location_id,
            data_center_code=data_center_code,
            identity_url=identity_url,
            resource_version=resource_version,
            physical_location_type=physical_location_type,
            street1=street1,
            street2=street2,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            region=region,
            latitude=latitude,
            longitude=longitude,
            elevation=elevation,
            lata=lata,
            timezone=timezone,
            data_owner=data_owner,
            data_source=data_source,
            data_source_version=data_source_version
        )
        payload: str = jinja_env().get_template("complex_create_update.json.j2").render(
            complex=complex_object)
        url: str = (
            f"{cls.base_url}{cls.api_version}/cloud-infrastructure/complexes/complex/"
            f"{complex_object.physical_location_id}"
        )
        cls.send_message("PUT", "create complex", url, data=payload)
        return complex_object

    @classmethod
    def update(cls,  # NOSONAR  # pylint: disable=too-many-locals, too-many-arguments
               physical_location_id: str,
               *,
               name: str = "",
               data_center_code: str = "",
               identity_url: str = "",
               resource_version: str = "",
               physical_location_type: str = "",
               street1: str = "",
               street2: str = "",
               city: str = "",
               state: str = "",
               postal_code: str = "",
               country: str = "",
               region: str = "",
               latitude: str = "",
               longitude: str = "",
               elevation: str = "",
               lata: str = "",
               timezone: str = "",
               data_owner: str = "",
               data_source: str = "",
               data_source_version: str = "") -> "Complex":
        """Update complex.

        Update complex object by calling A&AI API.
        If API request doesn't fail it returns Complex object.

        Returns:
            Complex: Updated complex object

        """
        complex_object: Complex = Complex(
            name=name,
            physical_location_id=physical_location_id,
            data_center_code=data_center_code,
            identity_url=identity_url,
            resource_version=resource_version,
            physical_location_type=physical_location_type,
            street1=street1,
            street2=street2,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            region=region,
            latitude=latitude,
            longitude=longitude,
            elevation=elevation,
            lata=lata,
            timezone=timezone,
            data_owner=data_owner,
            data_source=data_source,
            data_source_version=data_source_version
        )
        payload: str = jinja_env().get_template("complex_create_update.json.j2").render(
            complex=complex_object)
        url: str = (
            f"{cls.base_url}{cls.api_version}/cloud-infrastructure/complexes/complex/"
            f"{complex_object.physical_location_id}"
        )
        cls.send_message("PATCH", "update complex", url, data=payload)
        return complex_object

    @classmethod
    def get_all_url(cls) -> str:  # pylint: disable=arguments-differ
        """Return an url to get all complexes.

        Returns:
            str: URL to get all complexes

        """
        return f"{cls.base_url}{cls.api_version}/cloud-infrastructure/complexes"

    @classmethod
    def get_all(cls,
                physical_location_id: str = None,
                data_center_code: str = None,
                complex_name: str = None,
                identity_url: str = None) -> Iterator["Complex"]:
        """Get all complexes from A&AI.

        Call A&AI API to get all complex objects.

        Args:
            physical_location_id (str, optional): Unique identifier for physical location,
                e.g., CLLI. Defaults to None.
            data_center_code (str, optional): Data center code which can be an alternate way
                to identify a complex. Defaults to None.
            complex_name (str, optional): Gamma complex name for LCP instance. Defaults to None.
            identity_url (str, optional): URL of the keystone identity service. Defaults to None.

        Yields:
            Complex -- Complex object. Can not yield anything if any complex with given filter
                parameters doesn't exist

        """
        filter_parameters: dict = cls.filter_none_key_values(
            {
                "physical-location-id": physical_location_id,
                "data-center-code": data_center_code,
                "complex-name": complex_name,
                "identity-url": identity_url,
            }
        )
        url: str = f"{cls.get_all_url()}?{urlencode(filter_parameters)}"
        for complex_json in cls.send_message_json("GET",
                                                  "get cloud regions",
                                                  url).get("complex", []):
            yield cls.create_from_api_response(complex_json)

    @classmethod
    def get_by_physical_location_id(cls, physical_location_id: str) -> "Complex":
        """Get complex by physical location id.

        Args:
            physical_location_id (str): Physical location id of Complex

        Returns:
            Complex: Complex object

        Raises:
            ResourceNotFound: Complex with given physical location id not found

        """
        response = cls.send_message_json("GET",
                                         "Get complex with physical location id: "
                                         f"{physical_location_id}",
                                         f"{cls.base_url}{cls.api_version}/cloud-infrastructure/"
                                         f"complexes/complex/{physical_location_id}")
        return cls.create_from_api_response(response)

    @classmethod
    def create_from_api_response(cls,
                                 api_response: Dict[str, Any]) -> "Complex":
        """Create complex object using given A&AI API response JSON.

        Args:
            api_response (Dict[str, Any]): Complex A&AI API response

        Returns:
            Complex: Complex object created from given response

        """
        return cls(
            name=api_response.get("complex-name"),
            physical_location_id=api_response["physical-location-id"],
            data_center_code=api_response.get("data-center-code"),
            identity_url=api_response.get("identity-url"),
            resource_version=api_response.get("resource-version"),
            physical_location_type=api_response.get("physical-location-type"),
            street1=api_response.get("street1"),
            street2=api_response.get("street2"),
            city=api_response.get("city"),
            state=api_response.get("state"),
            postal_code=api_response.get("postal-code"),
            country=api_response.get("country"),
            region=api_response.get("region"),
            latitude=api_response.get("latitude"),
            longitude=api_response.get("longitude"),
            elevation=api_response.get("elevation"),
            lata=api_response.get("lata"),
            timezone=api_response.get("time-zone"),
            data_owner=api_response.get("data-owner"),
            data_source=api_response.get("data-source"),
            data_source_version=api_response.get("data-source-version")
        )

    def delete(self) -> None:
        """Delete complex."""
        self.send_message(
            "DELETE",
            f"Delete {self.physical_location_id} complex",
            f"{self.url}?resource-version={self.resource_version}"
        )
