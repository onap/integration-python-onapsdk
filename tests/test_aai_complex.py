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

from onapsdk.aai.cloud_infrastructure import Complex
from onapsdk.aai.cloud_infrastructure import CloudRegion


COMPLEXES = {
    "complex":[
        {
            "physical-location-id":"integration_test_complex",
            "data-center-code":"1234",
            "complex-name":"integration_test_complex",
            "identity-url":"",
            "resource-version":"1588244056133",
            "physical-location-type":"",
            "street1":"",
            "street2":"",
            "city":"",
            "state":"",
            "postal-code":"",
            "country":"",
            "region":"",
            "latitude":"",
            "longitude":"",
            "elevation":"",
            "lata":"",
            "time-zone":"",
            "data-owner":"",
            "data-source":"",
            "data-source-version":""
        }
    ]
}


COMPLEXES_COUNT = {
    "results":[
        {
            "complex":12
        }
    ]
}


@mock.patch.object(Complex, "send_message")
def test_complex(mock_send_message):
    cmplx = Complex(name="test_complex_name",
                    physical_location_id="test_location_id",
                    resource_version="1234")
    assert cmplx.name == "test_complex_name"
    assert cmplx.physical_location_id == "test_location_id"
    assert cmplx.url == (f"{Complex.base_url}{Complex.api_version}/cloud-infrastructure/"
                         "complexes/complex/test_location_id")

    cmplx2 = Complex.create(name="test_complex_name",
                            physical_location_id="test_location_id")
    mock_send_message.assert_called_once()
    assert cmplx2.name == "test_complex_name"
    assert cmplx2.physical_location_id == "test_location_id"
    assert cmplx2.url == (f"{Complex.base_url}{Complex.api_version}/cloud-infrastructure/"
                         "complexes/complex/test_location_id")
    method, _, url = mock_send_message.call_args[0]
    assert method == "PUT"
    assert url == (f"{Complex.base_url}{Complex.api_version}/cloud-infrastructure/"
                   "complexes/complex/test_location_id")


@mock.patch.object(Complex, "send_message_json")
def test_complex_get_all(mock_send_message_json):
    mock_send_message_json.return_value = COMPLEXES
    complexes = list(Complex.get_all())
    assert len(complexes) == 1
    cmplx = complexes[0]
    assert cmplx.name == "integration_test_complex"
    assert cmplx.physical_location_id == "integration_test_complex"


@mock.patch.object(CloudRegion, "add_relationship")
def test_cloud_region_link_to_complex(mock_add_rel):
    """Test Cloud Region linking with Complex.

    Test Relationship object creation
    """
    cloud_region = CloudRegion(cloud_owner="test_cloud_owner",
                               cloud_region_id="test_cloud_region",
                               orchestration_disabled=True,
                               in_maint=False)
    cmplx = Complex(name="test_complex_name",
                    physical_location_id="test_location_id",
                    resource_version="1234")
    cloud_region.link_to_complex(cmplx)
    mock_add_rel.assert_called_once()
    relationship = mock_add_rel.call_args[0][0]
    assert relationship.related_to == "complex"
    assert relationship.related_link == (f"aai/v13/cloud-infrastructure/complexes/"
                                         f"complex/test_location_id")
    assert len(relationship.relationship_data) == 2


@mock.patch.object(Complex, "send_message_json")
def test_complex_get_by_physical_location_id(mock_send_message_json):
    """Test complex get_by_physical_location_id url creation."""
    Complex.get_by_physical_location_id("test")
    assert mock_send_message_json.called_once_with(
        "GET",
        "Get complex with physical location id: test",
        f"{Complex.base_url}{Complex.api_version}/cloud-infrastructure/"
        f"complexes/complex/test"
    )

@mock.patch.object(Complex, "send_message")
def test_complex_delete(mock_send_message):
    cmplx = Complex(physical_location_id="test_location_id",
                    resource_version="1234")
    cmplx.delete()
    mock_send_message.assert_called_once_with(
        "DELETE",
        "Delete test_location_id complex",
        f"{cmplx.url}?resource-version={cmplx.resource_version}"
    )

@mock.patch.object(Complex, "send_message_json")
def test_complex_count(mock_send_message_json):
    mock_send_message_json.return_value = COMPLEXES_COUNT
    assert Complex.count() == 12
