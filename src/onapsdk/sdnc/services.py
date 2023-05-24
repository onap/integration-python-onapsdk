"""SDNC services module."""
#   Copyright 2023 Deutsche Telekom AG
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
from typing import Any, Dict, Iterable

from onapsdk.utils.headers_creator import headers_sdnc_creator
from onapsdk.utils.jinja import jinja_env

from .sdnc_element import SdncElement


class Service(SdncElement):
    """SDNC service."""

    headers: Dict[str, str] = headers_sdnc_creator(SdncElement.headers)

    def __init__(self,
                 service_instance_id: str,
                 service_data: Dict[str, Any] = None,
                 service_status: Dict[str, Any] = None) -> None:
        """Service information initialization.

        Args:
            service_instance_id (str):  Service instance id
            service_data (Dict[str, Any]): Service data
            service_status: Dict[str, Any]: Service status
        """
        super().__init__()
        self.service_instance_id: str = service_instance_id
        self.service_data: Dict[str, Any] = service_data
        self.service_status: Dict[str, Any] = service_status

    def __repr__(self) -> str:  # noqa
        """Service information human-readable string.

        Returns:
            str: Service information description

        """
        return (f"Service(service_instance_id={self.service_instance_id}, "
                f"service_data={self.service_data}, "
                f"service_status={self.service_status}")

    @classmethod
    def get_all(cls) -> Iterable["Service"]:
        """Get all uploaded services using GENERIC-RESOURCES-API.

        Yields:
            Services: Service object
        """
        for service in cls.send_message_json(
                "GET",
                "Get SDNC services",
                f"{cls.base_url}/restconf/config/GENERIC-RESOURCE-API:services"
        ).get('services', {}).get('service', []):
            try:
                service_data = service["service-data"]
            except KeyError:
                service_data = {}
            try:
                service_status = service["service-status"]
            except KeyError:
                service_status = {}
            yield Service(service_instance_id=service["service-instance-id"],
                          service_data=service_data,
                          service_status=service_status
                          )

    @classmethod
    def get(cls, service_instance_id) -> "Service":
        """Get service by service-instance-id via GENERIC-RESOURCES-API.

        Return:
            Service
        """
        service_iterable = cls.send_message_json(
            "GET",
            "Get SDNC services",
            f"{cls.base_url}/rests/data/"
            f"GENERIC-RESOURCE-API:services/service={service_instance_id}"
        )
        service = service_iterable["GENERIC-RESOURCE-API:service"][0]
        try:
            service_data = service["service-data"]
        except KeyError:
            service_data = {}
        try:
            service_status = service["service-status"]
        except KeyError:
            service_status = {}
        return Service(service_instance_id=service_instance_id,
                       service_data=service_data,
                       service_status=service_status
                       )

    def create(self) -> None:
        """Create service using GENERIC-RESOURCES-API."""
        service_data = self.service_data if self.service_data is not None else ""
        service_status = self.service_status if self.service_status is not None else ""
        self.send_message(
            "POST",
            "Create a service using GENERIC-RESOURCES-API",
            (f"{self.base_url}/restconf/config/"
             "GENERIC-RESOURCE-API:services"),
            data=jinja_env().get_template(
                "create_service_gr_api.json.j2").
            render(
                {
                    "service": {
                        "service-instance-id": self.service_instance_id,
                        "service-data": service_data,
                        "service-status": service_status
                    }
                }
            )
        )

    def update(self) -> None:
        """Update service information by service-instance-id using GENERIC-RESOURCES-API."""
        service_data = self.service_data if self.service_data is not None else ""
        service_status = self.service_status if self.service_status is not None else ""
        self.send_message(
            "PUT",
            "Update service information by service-instance-id using GENERIC-RESOURCES-API",
            (f"{self.base_url}/rests/data/"
             f"GENERIC-RESOURCE-API:services/service={self.service_instance_id}"),
            data=jinja_env().get_template(
                "create_service_gr_api.json.j2").
            render(
                {
                    "service": {
                        "service-instance-id": self.service_instance_id,
                        "service-data": service_data,
                        "service-status": service_status
                    }
                }
            )
        )

    def delete(self) -> None:
        """Delete service using GENERIC-RESOURCES-API."""
        self.send_message(
            "DELETE",
            "Delete a service using GENERIC-RESOURCE-API",
            (f"{self.base_url}/rests/data/"
             f"GENERIC-RESOURCE-API:services/service={self.service_instance_id}")
        )
