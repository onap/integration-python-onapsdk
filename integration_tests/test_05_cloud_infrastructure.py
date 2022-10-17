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
import pytest
import requests

from onapsdk.aai.cloud_infrastructure import CloudRegion, Complex
from onapsdk.exceptions import ResourceNotFound


@pytest.mark.integration
def test_cloud_region_get_all():
    requests.get(f"{CloudRegion.base_url}/reset")
    cloud_regions = list(CloudRegion.get_all())
    assert len(cloud_regions) == 0

    with pytest.raises(ResourceNotFound):
        CloudRegion.get_by_id("test_owner", "test_cloud_region")

    cloud_region: CloudRegion = CloudRegion.create(
        "test_owner", "test_cloud_region", orchestration_disabled=True, in_maint=False
    )
    cloud_regions = list(CloudRegion.get_all())
    assert len(cloud_regions) == 1
    cloud_region = cloud_regions[0]
    assert cloud_region.cloud_owner == "test_owner"
    assert cloud_region.cloud_region_id == "test_cloud_region"


@pytest.mark.integration
def test_complex_get_all():
    requests.get(f"{Complex.base_url}/reset")
    complexes = list(Complex.get_all())
    assert len(complexes) == 0

    cmplx: Complex = Complex.create(
        name="test_complex",
        physical_location_id="test_physical_location_id"
    )
    assert cmplx.name == "test_complex"
    assert cmplx.physical_location_id == "test_physical_location_id"

    complexes = list(Complex.get_all())
    assert len(complexes) == 1

    cmplx = complexes[0]
    assert cmplx.name == "test_complex"
    assert cmplx.physical_location_id == "test_physical_location_id"


@pytest.mark.integration
def test_link_cloud_region_to_complex():

    requests.get(f"{Complex.base_url}/reset")

    cmplx: Complex = Complex.create(
        name="test_complex",
        physical_location_id="test_physical_location_id"
    )
    cloud_region: CloudRegion = CloudRegion.create(
        "test_owner", "test_cloud_region", orchestration_disabled=True, in_maint=False
    )

    assert len(list(cloud_region.relationships)) == 0
    cloud_region.link_to_complex(cmplx)
    assert len(list(cloud_region.relationships)) == 1


@pytest.mark.integration
def test_cloud_region_tenants():

    cloud_region: CloudRegion = CloudRegion.create(
        "test_owner", "test_cloud_region", orchestration_disabled=True, in_maint=False
    )
    assert len(list(cloud_region.tenants)) == 0
    cloud_region.add_tenant(tenant_id="test_tenant_id", tenant_name="test_tenant_name", tenant_context="test_tenant_context")
    assert len(list(cloud_region.tenants)) == 1
    tenant = cloud_region.get_tenant(tenant_id="test_tenant_id")
