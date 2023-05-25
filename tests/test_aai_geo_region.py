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
from unittest.mock import patch

from onapsdk.aai.cloud_infrastructure.geo_region import GeoRegion

GEO_REGIONS = {
    "geo-region": [
        {
            "geo-region-id": "123"
        },
        {
            "geo-region-id": "321"
        }
    ]
}

GEO_REGION = {
    "geo-region-id": "123",
    "resource-version": "123"
}

@patch("onapsdk.aai.cloud_infrastructure.geo_region.GeoRegion.send_message_json")
def test_geo_region_get_all(mock_send_message_json):
    mock_send_message_json.return_value = {}
    assert len(list(GeoRegion.get_all())) == 0

    mock_send_message_json.return_value = GEO_REGIONS
    assert len(list(GeoRegion.get_all())) == 2

@patch("onapsdk.aai.cloud_infrastructure.geo_region.GeoRegion.send_message_json")
def test_geo_region_get_by_region_id(mock_send_message_json):
    mock_send_message_json.return_value = GEO_REGION
    geo_region = GeoRegion.get_by_geo_region_id("123")
    assert geo_region.geo_region_id == "123"
    assert geo_region.resource_version == "123"

@patch("onapsdk.aai.cloud_infrastructure.geo_region.GeoRegion.send_message")
@patch("onapsdk.aai.cloud_infrastructure.geo_region.GeoRegion.get_by_geo_region_id")
def test_geo_region_create(mock_get_geo_region_by_id, mock_send_message):
    GeoRegion.create("123")
    mock_send_message.assert_called_once()
    assert mock_get_geo_region_by_id.called_once_with("123")

def test_geo_region_url():
    geo_region = GeoRegion("test-geo-region")
    assert geo_region.url == "https://aai.api.sparky.simpledemo.onap.org:30233/aai/v27/cloud-infrastructure/geo-regions/geo-region/test-geo-region"
