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
from unittest import mock

from onapsdk.so.so_element import OrchestrationRequest, SoElement
from onapsdk.utils.headers_creator import headers_so_creator
from onapsdk.onap_service import OnapService


IN_PROGRESS = {
    "request": {
        "requestStatus": {
            "requestState": "IN_PROGRESS",
            "statusMessage": "test-message"
        }
    }
}
FAILED = {
    "request": {
        "requestStatus": {
            "requestState": "FAILED",
            "statusMessage": "test-message"
        }
    }
}
COMPLETE = {
    "request": {
        "requestStatus": {
            "requestState": "COMPLETE",
            "statusMessage": "test-message"
        }
    }
}
UNKNOWN = {
    "request": {
        "requestStatus": {
            "requestState": "INVALID",
            "statusMessage": "test-message"
        }
    }
}
BAD_RESPONSE = {}


@mock.patch.object(OrchestrationRequest, "send_message_json")
def test_orchestration_request_status(mock_send_message):
    orchestration_req = OrchestrationRequest(request_id="test")

    mock_send_message.return_value = BAD_RESPONSE
    assert orchestration_req.status == OrchestrationRequest.StatusEnum.UNKNOWN

    mock_send_message.return_value = UNKNOWN
    assert orchestration_req.status == OrchestrationRequest.StatusEnum.UNKNOWN

    mock_send_message.return_value = FAILED
    assert orchestration_req.status == OrchestrationRequest.StatusEnum.FAILED

    mock_send_message.return_value = COMPLETE
    assert orchestration_req.status == OrchestrationRequest.StatusEnum.COMPLETED

    mock_send_message.return_value = IN_PROGRESS
    assert orchestration_req.status == OrchestrationRequest.StatusEnum.IN_PROGRESS
    assert not orchestration_req.finished
    assert not orchestration_req.completed
    assert not orchestration_req.failed

    mock_send_message.return_value = COMPLETE
    assert orchestration_req.finished
    assert orchestration_req.completed
    assert not orchestration_req.failed

    mock_send_message.return_value = FAILED
    assert orchestration_req.finished
    assert not orchestration_req.completed
    assert orchestration_req.failed

@mock.patch.object(OrchestrationRequest, "send_message_json")
def test_orchestration_request_status_message(mock_send_message):
    orchestration_req = OrchestrationRequest(request_id="test")

    mock_send_message.return_value = BAD_RESPONSE
    assert orchestration_req.status_message == "Unknown request state"

    mock_send_message.return_value = UNKNOWN
    assert orchestration_req.status_message == "test-message"

    mock_send_message.return_value = FAILED
    assert orchestration_req.status_message == "test-message"

    mock_send_message.return_value = COMPLETE
    assert orchestration_req.status_message == "test-message"


#Test the Class SoElement
def test_SoElement_headers():
    """Test the header property"""
    element = SoElement()
    assert element.headers != headers_so_creator(OnapService.headers)
    #check x-transactionid for headers


def test_get_subscription_service_type():
    """Test SO Element class method"""
    vf_object_name = SoElement.get_subscription_service_type("vf_name")
    assert vf_object_name == "vf_name"


def test_base_create_url():
    """Test base create url class method"""
    assert SoElement._base_create_url() == "{}/onap/so/infra/serviceInstantiation/{}/serviceInstances".\
                                            format(SoElement.base_url, SoElement.api_version)

