"""Test SDNC service creation using GENERIC-RESOURCE-API."""
#   Copyright 2023 Orange, Deutsche Telekom AG
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
import json
from collections.abc import Iterable
from typing import Dict
from unittest import mock

from onapsdk.sdnc.services import Service

SDNC_SERVICES_INFORMATION = {
    "services": {
        "service": [
            {
                "service-instance-id": "sdnc-int-test-fffffffffff",
                "service-status": {
                    "response-code": "string",
                    "response-message": "string",
                    "final-indicator": "string",
                    "request-status": "string",
                    "action": "string",
                    "rpc-name": "string",
                    "rpc-action": "string",
                    "response-timestamp": "string"
                },
                "service-data": {
                    "service-level-oper-status": {
                        "last-rpc-action": "assign",
                        "last-action": "CreateServiceInstance",
                        "order-status": "Created"
                    }
                }
            }
        ]
    }
}

SDNC_SERVICES_INFORMATION_GET ={
    "GENERIC-RESOURCE-API:service": [
        {
            "service-instance-id": "sdnc-int-test-fffffffffff",
            "service-status": {
                    "response-code": "string",
                    "response-message": "string",
                    "final-indicator": "string",
                    "request-status": "string",
                    "action": "string",
                    "rpc-name": "string",
                    "rpc-action": "string",
                    "response-timestamp": "string"
            },
            "service-data": {
                    "service-level-oper-status": {
                        "last-rpc-action": "assign",
                        "last-action": "CreateServiceInstance",
                        "order-status": "Created"
                    }
                }
        }
    ]
}

SDNC_SERVICE_ID = "sdnc-int-test-fffffffffff"
@mock.patch.object(Service, "send_message_json")
def test_sdnc_service_gr_api_get_all(mock_send_message_json):
    mock_send_message_json.return_value = SDNC_SERVICES_INFORMATION
    sdnc_all_services = Service.get_all()
    assert isinstance(sdnc_all_services, Iterable)
    sdnc_all_services_list = list(sdnc_all_services)
    assert len(sdnc_all_services_list) == 1
    service = sdnc_all_services_list[0]
    assert isinstance(service, Service)
    assert service.service_instance_id == SDNC_SERVICE_ID

@mock.patch.object(Service, "send_message")
def test_sdnc_service_gr_api_create(mock_send_message):
    service = Service(SDNC_SERVICES_INFORMATION["services"]["service"][0]["service-instance-id"],
                      SDNC_SERVICES_INFORMATION["services"]["service"][0]["service-status"])
    service.create()

    mock_send_message.assert_called_once()
    method, description, url = mock_send_message.call_args[0]
    assert method == "POST"
    assert description == "Create a service using GENERIC-RESOURCES-API"
    assert url == (f"{Service.base_url}/restconf/config/"
                   "GENERIC-RESOURCE-API:services")

@mock.patch.object(Service, "send_message")
def test_sdnc_service_gr_api_update(mock_send_message):
    service = Service(service_instance_id=SDNC_SERVICES_INFORMATION["services"]["service"][0]["service-instance-id"],
                      service_status=SDNC_SERVICES_INFORMATION["services"]["service"][0]["service-status"],
                      service_data=SDNC_SERVICES_INFORMATION["services"]["service"][0]["service-data"])
    service.update()
    mock_send_message.assert_called_once()
    method, description, url = mock_send_message.call_args[0]
    assert method == "PUT"
    assert description == "Update service information by service-instance-id using GENERIC-RESOURCES-API"
    assert url == (f"{Service.base_url}/rests/data/"
                   f"GENERIC-RESOURCE-API:services/service={service.service_instance_id}")


@mock.patch.object(Service, "send_message")
def test_sdnc_service_gr_api_delete(mock_send_message):
    service = Service(SDNC_SERVICES_INFORMATION["services"]["service"][0]["service-instance-id"],
                      SDNC_SERVICES_INFORMATION["services"]["service"][0]["service-status"])
    service.delete()

    mock_send_message.assert_called_once()
    method, description, url = mock_send_message.call_args[0]
    assert method == "DELETE"
    assert description == "Delete a service using GENERIC-RESOURCE-API"
    assert url == (f"{Service.base_url}/rests/data/"
                   "GENERIC-RESOURCE-API:services/"
                   f"service={SDNC_SERVICE_ID}")
