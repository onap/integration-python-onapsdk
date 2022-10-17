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

from onapsdk.aai.cloud_infrastructure.cloud_region import CloudRegion, Tenant
from onapsdk.exceptions import ResourceNotFound


COUNT = {
    "results":[
        {
            "cloud-region":2
        }
    ]
}


@mock.patch("onapsdk.aai.cloud_infrastructure.cloud_region.AaiResource.relationships", new_callable=mock.PropertyMock)
@mock.patch("onapsdk.aai.cloud_infrastructure.cloud_region.Complex.get_by_physical_location_id")
def test_cloud_region_complex_property(mock_complex_get, mock_relationships):
    cr = CloudRegion("test_cloud_owner", "test_cloud_region_id", False, False)

    mock_relationships.return_value = []
    assert cr.complex is None

    mock_relationships.return_value = [mock.MagicMock()]
    assert cr.complex is None

    relationship_mock = mock.MagicMock()
    relationship_mock.related_to = "complex"
    relationship_mock.get_relationship_data.return_value = None
    mock_relationships.return_value = [relationship_mock]
    assert cr.complex is None

    relationship_mock.get_relationship_data.return_value = "123"
    mock_complex_get.side_effect = ResourceNotFound
    assert cr.complex is None

    mock_complex_get.side_effect = None
    mock_complex_get.return_value = mock.MagicMock()
    assert cr.complex is not None

    mock_relationships.side_effect = ResourceNotFound
    assert cr.complex is None

@mock.patch("onapsdk.aai.cloud_infrastructure.cloud_region.CloudRegion.tenants", new_callable=mock.PropertyMock)
def test_cloud_region_get_tenants_by_name(mock_tenants):
    cr = CloudRegion("test_cloud_owner", "test_cloud_region_id", False, False)
    mock_tenants.return_value = iter([
        Tenant(cloud_region="test_cloud_region_id",tenant_id="test-tenant",tenant_name="test-tenant")
    ])
    tenants = list(cr.get_tenants_by_name("test-tenant"))
    assert len(tenants) == 1
    assert isinstance(tenants[0], Tenant)
    assert tenants[0].name == "test-tenant"

@mock.patch("onapsdk.aai.cloud_infrastructure.cloud_region.CloudRegion.send_message_json")
def test_cloud_region_count(mock_send_message_json):
    mock_send_message_json.return_value = COUNT
    assert CloudRegion.count() == 2
