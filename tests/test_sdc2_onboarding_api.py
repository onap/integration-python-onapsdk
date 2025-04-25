
from unittest.mock import patch

from onapsdk.sdc2.sdc_onboarding_api import SdcOnboardingApi, SdcOnboardingApiItemTypeEnum, SdcOnboardingApiItemVersion, SdcOnboardingApiVersionStatus


@patch("onapsdk.sdc2.sdc_onboarding_api.SdcOnboardingApi.send_message_json")
def test_onboarding_api_get_raw_items(mock_send_message_json):
    mock_send_message_json.return_value = {}
    assert list(SdcOnboardingApi.get_raw_items()) == []
    mock_send_message_json.return_value = {"results": []}
    assert list(SdcOnboardingApi.get_raw_items()) == []
    mock_send_message_json.return_value = {"results": [{}]}
    assert list(SdcOnboardingApi.get_raw_items()) == [{}]
    assert list(SdcOnboardingApi.get_raw_items(SdcOnboardingApiItemTypeEnum.VLM)) == [{}]
    assert list(SdcOnboardingApi.get_raw_items(SdcOnboardingApiItemTypeEnum.VSP)) == [{}]


def test_onboarding_api_item_version_create_from_api_response():
    item_version = SdcOnboardingApiItemVersion.create_from_api_response(
        {
            "name": "test",
            "id": "test_id",
            "description": "test_description",
            "status": "Certified",
            "creationTime": "test_creation_time",
            "modificationTime": "test_modification_time",
            "additionalInfo": "test_additional_info"
        }
    )
    assert item_version.name == "test"
    assert item_version.version_id == "test_id"
    assert item_version.description == "test_description"
    assert item_version.status == SdcOnboardingApiVersionStatus.CERTIFIED
    assert item_version.creation_time == "test_creation_time"
    assert item_version.modification_time == "test_modification_time"
    assert item_version.additional_info == "test_additional_info"
    
    item_version = SdcOnboardingApiItemVersion.create_from_api_response(
        {
            "name": "test",
            "id": "test_id",
            "description": "test_description",
            "status": "Draft",
            "creationTime": "test_creation_time",
            "modificationTime": "test_modification_time",
            "additionalInfo": "test_additional_info"
        }
    )
    assert item_version.name == "test"
    assert item_version.version_id == "test_id"
    assert item_version.description == "test_description"
    assert item_version.status == SdcOnboardingApiVersionStatus.DRAFT
    assert item_version.creation_time == "test_creation_time"
    assert item_version.modification_time == "test_modification_time"
    assert item_version.additional_info == "test_additional_info"
    
    item_version = SdcOnboardingApiItemVersion.create_from_api_response(
        {
            "name": "test",
            "id": "test_id",
            "description": "test_description",
            "status": "Locked",
            "creationTime": "test_creation_time",
            "modificationTime": "test_modification_time",
            "additionalInfo": "test_additional_info"
        }
    )
    assert item_version.name == "test"
    assert item_version.version_id == "test_id"
    assert item_version.description == "test_description"
    assert item_version.status == SdcOnboardingApiVersionStatus.LOCKED
    assert item_version.creation_time == "test_creation_time"
    assert item_version.modification_time == "test_modification_time"
    assert item_version.additional_info == "test_additional_info"
    
    item_version = SdcOnboardingApiItemVersion.create_from_api_response(
        {
            "name": "test",
            "id": "test_id",
            "description": "test_description",
            "status": "Deprecated",
            "creationTime": "test_creation_time",
            "modificationTime": "test_modification_time",
            "additionalInfo": "test_additional_info"
        }
    )
    assert item_version.name == "test"
    assert item_version.version_id == "test_id"
    assert item_version.description == "test_description"
    assert item_version.status == SdcOnboardingApiVersionStatus.DEPRECATED
    assert item_version.creation_time == "test_creation_time"
    assert item_version.modification_time == "test_modification_time"
    assert item_version.additional_info == "test_additional_info"
    
    item_version = SdcOnboardingApiItemVersion.create_from_api_response(
        {
            "name": "test",
            "id": "test_id",
            "description": "test_description",
            "status": "Deleted",
            "creationTime": "test_creation_time",
            "modificationTime": "test_modification_time",
            "additionalInfo": "test_additional_info"
        }
    )
    assert item_version.name == "test"
    assert item_version.version_id == "test_id"
    assert item_version.description == "test_description"
    assert item_version.status == SdcOnboardingApiVersionStatus.DELETED
    assert item_version.creation_time == "test_creation_time"
    assert item_version.modification_time == "test_modification_time"
    assert item_version.additional_info == "test_additional_info"
