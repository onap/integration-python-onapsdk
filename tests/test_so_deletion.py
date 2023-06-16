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

from onapsdk.so.deletion import (
    PnfDeletionRequest,
    ServiceDeletionRequest,
    VfModuleDeletionRequest,
    VnfDeletionRequest
)


@mock.patch.object(ServiceDeletionRequest, "send_message")
def test_service_deletion_request(mock_send_message):
    mock_instance = mock.MagicMock()
    mock_instance.instance_id = "test_instance_id"
    ServiceDeletionRequest.send_request(instance=mock_instance)
    mock_send_message.assert_called_once()
    method, _, url = mock_send_message.call_args[0]
    assert method == "DELETE"
    assert url == (f"{ServiceDeletionRequest.base_url}/onap/so/infra/"
                   f"serviceInstantiation/{ServiceDeletionRequest.api_version}/"
                   "serviceInstances/test_instance_id")


@mock.patch.object(VfModuleDeletionRequest, "send_message")
def test_vf_module_deletion_request(mock_send_message):
    mock_vf_module_instance = mock.MagicMock()
    mock_vf_module_instance.vf_module_id = "test_vf_module_id"

    mock_vnf_instance = mock.MagicMock()
    mock_vnf_instance.vnf_id = "test_vnf_id"
    mock_vf_module_instance.vnf_instance = mock_vnf_instance

    mock_service_instance = mock.MagicMock()
    mock_service_instance.instance_id = "test_service_instance_id"
    mock_vnf_instance.service_instance = mock_service_instance

    VfModuleDeletionRequest.send_request(instance=mock_vf_module_instance)
    mock_send_message.assert_called_once()
    method, _, url = mock_send_message.call_args[0]
    assert method == "DELETE"
    assert url == (f"{VfModuleDeletionRequest.base_url}/onap/so/infra/"
                   f"serviceInstantiation/{VfModuleDeletionRequest.api_version}/"
                   "serviceInstances/test_service_instance_id/"
                   "vnfs/test_vnf_id/vfModules/test_vf_module_id")


@mock.patch.object(VnfDeletionRequest, "send_message")
def test_vnf_deletion_request(mock_send_message):
    mock_vnf_instance = mock.MagicMock()
    mock_vnf_instance.vnf_id = "test_vnf_id"

    mock_service_instance = mock.MagicMock()
    mock_service_instance.instance_id = "test_service_instance"
    mock_vnf_instance.service_instance = mock_service_instance
    VnfDeletionRequest.send_request(instance=mock_vnf_instance)
    mock_send_message.assert_called_once()
    method, _, url = mock_send_message.call_args[0]
    assert method == "DELETE"
    assert url == (f"{VnfDeletionRequest.base_url}/onap/so/infra/"
                   f"serviceInstantiation/{VnfDeletionRequest.api_version}/"
                   "serviceInstances/test_service_instance/"
                   "vnfs/test_vnf_id")

@mock.patch.object(PnfDeletionRequest, "send_message")
def test_pnf_deletion_request(mock_send_message):
    mock_pnf_instance = mock.MagicMock()
    mock_pnf_instance.pnf_id = "test_pnf_id"

    mock_service_instance = mock.MagicMock()
    mock_service_instance.instance_id = "test_service_instance"
    mock_pnf_instance.service_instance = mock_service_instance
    PnfDeletionRequest.send_request(instance=mock_pnf_instance)
    mock_send_message.assert_called_once()
    method, _, url = mock_send_message.call_args[0]
    assert method == "DELETE"
    assert url == (f"{PnfDeletionRequest.base_url}/onap/so/infra/"
                   f"serviceInstantiation/{PnfDeletionRequest.api_version}/"
                   "serviceInstances/test_service_instance/"
                   "pnfs/test_pnf_id")

