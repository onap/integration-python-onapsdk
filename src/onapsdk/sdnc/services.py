"""SDNC services module."""
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
from typing import Any, Dict, Iterable

from onapsdk.utils.headers_creator import headers_sdnc_creator
from onapsdk.utils.jinja import jinja_env

from .sdnc_element import SdncElement

class Svc(SdncElement):
    """SDNC service base class."""

    headers: Dict[str, str] = headers_sdnc_creator(SdncElement.headers)

class Service(Svc):
    """SDNC service."""

    def __init__(self,
                 service_instance_id: str,
                 service_status: Dict[str, Any]) -> None:
        """Service information initialization.

        Args:
            service_instance_id (str):  Service instance id
            service_status: Dict[str, Any]: Service status
            service_data (Dict[str, Any]): Service data
        """
        super().__init__()
        self.service_instance_id: str = service_instance_id
        self.service_status: Dict[str, Any] = service_status

    def __repr__(self) -> str:  # noqa
        """Service information human readable string.

        Returns:
            str: Service information description

        """
        return (f"Service(service_instance_id={self.service_instance_id}, "
                f"service_status={self.service_status}")

    @classmethod
    def get_all(cls) -> Iterable["Service"]:
        """Get all uploaded services using GENERIC-RESOURCES-API.

        Yields:
            Services: Service object
        """
        for service in \
            cls.send_message_json(\
                "GET",\
                "Get SDNC services",\
                f"{cls.base_url}/restconf/config/GENERIC-RESOURCE-API:services"
                                 ).get('services', {}).get('service', []):
            yield Service(service_instance_id=service["service-instance-id"],
                          service_status=service["service-status"]
                          )

    def create(self) -> None:
        """Create service using GENERIC-RESOURCES-API."""
        self.send_message(
            "POST",
            "Create a service using GENERIC-RESOURCES-API",
            (f"{self.base_url}/restconf/config/"
             "GENERIC-RESOURCE-API:services"),
            data=jinja_env().get_template(
                "create_service_gr_api.json.j2").
            render(
                service_instance_id=self.service_instance_id
            )
        )


    def get(self) -> Iterable["Service"]:
        """Get service information by service-instance-id using GENERIC-RESOURCES-API."""
        for service in \
                self.send_message_json(
                        "GET",
                        "Get status of a service using GENERIC-RESOURCES-API",
                        (f"{self.base_url}/rests/data/"
                         f"GENERIC-RESOURCE-API:services/service={self.service_instance_id}")
                    ).get('GENERIC-RESOURCE-API:service', []):
            yield Service(service_instance_id=service["service-instance-id"],
                          service_status=service["service-status"])

    def delete(self) -> None:
        """Delete service using GENERIC-RESOURCES-API."""
        self.send_message(
            "DELETE",
            "Delete a service using GENERIC-RESOURCE-API",
            (f"{self.base_url}/rests/data/"
             f"GENERIC-RESOURCE-API:services/service={self.service_instance_id}")
        )
