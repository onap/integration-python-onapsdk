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

from onapsdk.sdc.component import Component


def test_sdc_component_delete():
    mock_sdc_resource = mock.MagicMock()
    mock_parent_sdc_resource = mock.MagicMock()
    mock_parent_sdc_resource.resource_inputs_url = "http://test.onap.org"
    component = Component(
        created_from_csar=False,
        actual_component_uid="123",
        unique_id="456",
        normalized_name="789",
        name="test_component",
        origin_type="test-origin-type",
        customization_uuid="098",
        component_uid="765",
        component_version="432",
        tosca_component_name="test-tosca-component-name",
        component_name="test-component-name",
        sdc_resource=mock_sdc_resource,
        parent_sdc_resource=mock_parent_sdc_resource,
        group_instances=None
    )
    component.delete()
    mock_sdc_resource.send_message_json.assert_called_once_with(
        "DELETE",
        "Delete test_component component",
        f"http://test.onap.org/resourceInstance/{component.unique_id}"
    )
