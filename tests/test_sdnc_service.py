"""Test SDNC service creation using GENERIC-RESOURCE-API."""
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
from collections.abc import Iterable
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

SDNC_SERVICES_INFORMATION_GET = {
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

SDNC_SERVICES_INFORMATION_GET_STATUS_MISSING = {
    "GENERIC-RESOURCE-API:service": [
        {
            "service-instance-id": "sdnc-int-test-fffffffffff",
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

SDNC_SERVICES_INFORMATION_GET_DATA_MISSING = {
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
            }
        }
    ]
}

SDNC_SERVICES_INFORMATION_GET_ALL_SERVICE_DATA_MISSING = {
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
                }
            }
        ]
    }
}

SDNC_SERVICES_INFORMATION_GET_ALL_SERVICE_STATUS_MISSING = {
    "services": {
        "service": [
            {
                "service-instance-id": "sdnc-int-test-fffffffffff",
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


@mock.patch.object(Service, "send_message_json")
def test_sdnc_service_gr_api_get(mock_send_message_json):
    mock_send_message_json.return_value = SDNC_SERVICES_INFORMATION_GET
    sdnc_service = Service.get(SDNC_SERVICE_ID)
    assert isinstance(sdnc_service, Service)
    assert sdnc_service.service_instance_id == SDNC_SERVICE_ID


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


@mock.patch.object(Service, "send_message_json")
def test_sdnc_service_gr_api_get_all_key_error_data(mock_send_message_json):
    mock_send_message_json.return_value = SDNC_SERVICES_INFORMATION_GET_ALL_SERVICE_DATA_MISSING
    sdnc_all_services = Service.get_all()
    assert isinstance(sdnc_all_services, Iterable)
    sdnc_all_services_list = list(sdnc_all_services)
    assert len(sdnc_all_services_list) == 1
    service = sdnc_all_services_list[0]
    assert isinstance(service, Service)
    assert service.service_data == {}


@mock.patch.object(Service, "send_message_json")
def test_sdnc_service_gr_api_get_all_key_error_status(mock_send_message_json):
    mock_send_message_json.return_value = SDNC_SERVICES_INFORMATION_GET_ALL_SERVICE_STATUS_MISSING
    sdnc_all_services = Service.get_all()
    assert isinstance(sdnc_all_services, Iterable)
    sdnc_all_services_list = list(sdnc_all_services)
    assert len(sdnc_all_services_list) == 1
    service = sdnc_all_services_list[0]
    assert isinstance(service, Service)
    assert service.service_status == {}


@mock.patch.object(Service, "send_message_json")
def test_sdnc_service_gr_api_get_key_error_data(mock_send_message_json):
    mock_send_message_json.return_value = SDNC_SERVICES_INFORMATION_GET_DATA_MISSING
    sdnc_service = Service.get(SDNC_SERVICE_ID)
    assert isinstance(sdnc_service, Service)
    assert sdnc_service.service_instance_id == SDNC_SERVICE_ID
    assert sdnc_service.service_data == {}


@mock.patch.object(Service, "send_message_json")
def test_sdnc_service_gr_api_get_key_error_status(mock_send_message_json):
    mock_send_message_json.return_value = SDNC_SERVICES_INFORMATION_GET_STATUS_MISSING
    sdnc_service = Service.get(SDNC_SERVICE_ID)
    assert isinstance(sdnc_service, Service)
    assert sdnc_service.service_instance_id == SDNC_SERVICE_ID
    assert sdnc_service.service_status == {}