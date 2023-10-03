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

from onapsdk.aai.business.project import Project
from onapsdk.aai.cloud_infrastructure import CloudRegion
from onapsdk.aai.business import OwningEntity
from onapsdk.aai.cloud_infrastructure import Tenant

from onapsdk.exceptions import APIError

TENANTS = {
    "tenant": [
        {
            "name": "test-name",
            "resource-version": "1234"
        },
        {
            "name": "test-name2",
            "resource-version": "4321"
        }
    ]
}

COUNT = {
    "results": [
        {
            "tenant": 1
        }
    ]
}


@mock.patch.object(OwningEntity, "add_relationship")
def test_owning_entity_link_to_tenant(mock_add_rel):
    """Test OwningEntity linking with Tenant.

    Test Relationship object creation
    """
    owning_entity = OwningEntity(name="test_owning_entity",
                                 owning_entity_id="test_owning_id",
                                 resource_version="12345")
    cloud_regin = CloudRegion(cloud_owner="test_cloud_owner",
                              cloud_region_id="test_cloud_region",
                              orchestration_disabled=True,
                              in_maint=False)
    tenant = Tenant(cloud_region=cloud_regin, tenant_id="test_tenant_id", tenant_name="test_tenant_name")

    owning_entity.link_to_tenant(tenant)
    mock_add_rel.assert_called_once()
    relationship = mock_add_rel.call_args[0][0]
    assert relationship.related_to == "tenant"
    assert relationship.related_link == (f"https://aai.api.sparky.simpledemo.onap.org:30233/aai/"
                                         f"v27/cloud-infrastructure/cloud-regions/cloud-region/"
                                         f"test_cloud_owner/test_cloud_region/"
                                         f"tenants/tenant/test_tenant_id?resource-version=None")
    assert len(relationship.relationship_data) == 1


@mock.patch.object(OwningEntity, "delete_relationship")
def test_owning_entity_delete_tenant(mock_add_rel):
    """Test delete OwningEntity's Tenant.

    Test Relationship object deletion
    """
    owning_entity = OwningEntity(name="test_owning_entity",
                                 owning_entity_id="test_owning_id",
                                 resource_version="12345")
    cloud_regin = CloudRegion(cloud_owner="test_cloud_owner",
                              cloud_region_id="test_cloud_region",
                              orchestration_disabled=True,
                              in_maint=False)
    tenant = Tenant(cloud_region=cloud_regin, tenant_id="test_tenant_id", tenant_name="test_tenant_name")

    owning_entity.delete_relationship_with_tenant(tenant)
    mock_add_rel.assert_called_once()
    relationship = mock_add_rel.call_args[0][0]
    assert relationship.related_to == "tenant"
    assert relationship.related_link == (f"https://aai.api.sparky.simpledemo.onap.org:30233/aai/"
                                         f"v27/cloud-infrastructure/cloud-regions/cloud-region/"
                                         f"test_cloud_owner/test_cloud_region/"
                                         f"tenants/tenant/test_tenant_id?resource-version=None")
    assert len(relationship.relationship_data) == 1


def test_tenant_url():
    cloud_regin = CloudRegion(cloud_owner="test_cloud_owner",
                              cloud_region_id="test_cloud_region",
                              orchestration_disabled=True,
                              in_maint=False)
    tenant = Tenant(cloud_region=cloud_regin, tenant_id="test_tenant_id", tenant_name="test_tenant_name")
    assert tenant.url == (f"https://aai.api.sparky.simpledemo.onap.org:30233/aai/v27/cloud-infrastructure/"
                          f"cloud-regions/cloud-region/test_cloud_owner/test_cloud_region/tenants/tenant/"
                          f"test_tenant_id?resource-version=None")


def test_tenant_getall_url():
    cloud_regin = CloudRegion(cloud_owner="test_cloud_owner",
                              cloud_region_id="test_cloud_region",
                              orchestration_disabled=True,
                              in_maint=False)
    tenant = Tenant(cloud_region=cloud_regin, tenant_id="test_tenant_id", tenant_name="test_tenant_name")
    assert tenant.get_all_url(cloud_regin) == (
        f"https://aai.api.sparky.simpledemo.onap.org:30233/aai/v27/cloud-infrastructure/"
        f"cloud-regions/cloud-region/test_cloud_owner/test_cloud_region/tenants/")

@mock.patch.object(Tenant, "send_message")
def test_tenant_delete(mock_send_message):
    cloud_regin = CloudRegion(cloud_owner="test_cloud_owner",
                              cloud_region_id="test_cloud_region",
                              orchestration_disabled=True,
                              in_maint=False)
    tenant = Tenant(cloud_region=cloud_regin, tenant_id="test_tenant_id", tenant_name="test_tenant_name")
    tenant.delete()
    mock_send_message.assert_called_once_with(
        "DELETE",
        f"Remove tenant {tenant.name} from {tenant.cloud_region.cloud_region_id} cloud region",
        url=tenant.url
    )
