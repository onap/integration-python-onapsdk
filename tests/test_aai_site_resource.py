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
from unittest.mock import patch, MagicMock

from onapsdk.aai.network.site_resource import SiteResource

SITE_RESOURCE = {
    "site-resource-id":"123",
    "resource-version":"213"
}

SITE_RESOURCES = {
    "site-resource":[
        SITE_RESOURCE,
        {
            "site-resource-id":"321",
            "resource-version":"312"
        }
    ]
}

@patch("onapsdk.aai.network.site_resource.SiteResource.send_message_json")
def test_site_resource_get_all(mock_send_message_json):
    assert len(list(SiteResource.get_all())) == 0
    mock_send_message_json.return_value = SITE_RESOURCES
    site_resources = list(SiteResource.get_all())
    assert len(site_resources) == 2
    sr1, sr2 = site_resources
    assert sr1.site_resource_id == "123"
    assert sr1.resource_version == "213"
    assert sr2.site_resource_id == "321"
    assert sr2.resource_version == "312"

@patch("onapsdk.aai.network.site_resource.SiteResource.send_message_json")
def test_site_resource_get_by_id(mock_send_message_json):
    mock_send_message_json.return_value = SITE_RESOURCE
    sr = SiteResource.get_by_site_resource_id("123")
    assert sr.site_resource_id == "123"
    assert sr.resource_version == "213"

@patch("onapsdk.aai.network.site_resource.SiteResource.send_message")
@patch("onapsdk.aai.network.site_resource.SiteResource.get_by_site_resource_id")
def test_site_resource_create(mock_get_by_site_resource_id, mock_send_message):
    SiteResource.create("123")
    mock_send_message.assert_called_once()
    assert mock_get_by_site_resource_id.called_once_with("123")

@patch("onapsdk.aai.network.site_resource.SiteResource.add_relationship")
def test_site_resource_link_to_complex(mock_add_relationship):
    cmplx = MagicMock(physical_location_id="test-complex-physical-location-id",
                      url="test-complex-url")
    site_resource = SiteResource("test-site-resource")
    site_resource.link_to_complex(cmplx)
    mock_add_relationship.assert_called_once()
    relationship = mock_add_relationship.call_args[0][0]
    assert relationship.related_to == "complex"
    assert relationship.related_link == "test-complex-url"
    assert relationship.relationship_label == "org.onap.relationships.inventory.Uses"
    assert relationship.relationship_data == [{
        "relationship-key": "complex.physical-location-id",
        "relationship-value": "test-complex-physical-location-id",
    }]


@patch("onapsdk.aai.network.site_resource.SiteResource.add_relationship")
def test_site_resource_link_to_site_resource(mock_add_relationship):
    site_resource_rel = MagicMock(site_resource_id="test-site-resource-id",
                                  url="test-site-resource-url")
    site_resource = SiteResource("test-site-resource")
    site_resource.link_to_site_resource(site_resource_rel)
    mock_add_relationship.assert_called_once()
    relationship = mock_add_relationship.call_args[0][0]
    assert relationship.related_to == "site-resource"
    assert relationship.related_link == "test-site-resource-url"
    assert relationship.relationship_label == "org.onap.relationships.inventory.Supports"
    assert relationship.relationship_data == [{
        "relationship-key": "site_resource.site-resource-id",
        "relationship-value": "test-site-resource-id",
    }]
