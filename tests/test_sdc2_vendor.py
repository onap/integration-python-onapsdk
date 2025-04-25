
from unittest.mock import MagicMock, patch, PropertyMock
from onapsdk.exceptions import ResourceNotFound
from onapsdk.sdc2.sdc_onboarding_api import SdcOnboardingApiItemAction, SdcOnboardingApiItemVersionAction
from onapsdk.sdc2.vendor import Vendor, SdcOnboardingApiItemTypeEnum

from pytest import raises


def test_vendor_item_type():
    vendor = Vendor("test_name", "test_item_type", "test_item_id", "test_description", "test_owner", "ACTIVE", {})
    assert vendor.get_item_type() == SdcOnboardingApiItemTypeEnum.VLM


@patch("onapsdk.sdc2.vendor.Vendor.send_message_json")
def test_create_vendor(mock_send_message_json):
    mock_send_message_json.side_effect = [
        {
            "itemId": "123"
        },
        {
            "name": "test_name",
            "id": "123",
            "description": "123",
            "status": "ACTIVE",
            "type": "vlm",
            "owner": "cs0008",
            "properties": {}
        }
    ]
    v = Vendor.create("test_name")
    mock_send_message_json.assert_called()
    assert v.name == "test_name"
    assert v.vendor_id == "123"


@patch("onapsdk.sdc2.vendor.Vendor.send_message")
@patch("onapsdk.sdc2.vendor.SdcOnboardingApiItem.update")
def test_action(mock_update, mock_send_message):
    v = Vendor("test", "vlm", "123", "test_Desc", "cs0008", "ACTIVE", {})
    v._action(SdcOnboardingApiItemAction.RESTORE)
    mock_send_message.assert_called_once()
    mock_update.assert_called_once()


@patch("onapsdk.sdc2.vendor.SdcOnboardingApiItem._action")
def test_archive_vendor(mock_action):
    v = Vendor("test", "vlm", "123", "test_Desc", "cs0008", "ACTIVE", {})
    v.archive()
    mock_action.assert_called_once_with(SdcOnboardingApiItemAction.ARCHIVE)


@patch("onapsdk.sdc2.vendor.SdcOnboardingApiItem._action")
def test_restore_vendor(mock_action):
    v = Vendor("test", "vlm", "123", "test_Desc", "cs0008", "ACTIVE", {})
    v.restore()
    mock_action.assert_called_once_with(SdcOnboardingApiItemAction.RESTORE)


@patch("onapsdk.sdc2.vendor.Vendor.send_message")
@patch("onapsdk.sdc2.vendor.SdcOnboardingApiItem.update")
@patch("onapsdk.sdc2.vendor.SdcOnboardingApiItem.latest_item_version_url", new_callable=PropertyMock)
def test_version_action(mock_url, mock_update, mock_send_message):
    mock_url.return_value = "test_url"
    v = Vendor("test", "vlm", "123", "test_Desc", "cs0008", "ACTIVE", {})
    v._version_action(SdcOnboardingApiItemVersionAction.CLEAN)
    mock_send_message.assert_called_once()
    mock_update.assert_called_once()


@patch("onapsdk.sdc2.vendor.SdcOnboardingApiItem._version_action")
def test_commit_vendor_version(mock_version_action):
    v = Vendor("test", "vlm", "123", "test_Desc", "cs0008", "ACTIVE", {})
    v.commit_version()
    mock_version_action.assert_called_once_with(SdcOnboardingApiItemVersionAction.COMMIT)


@patch("onapsdk.sdc2.vendor.Vendor.send_message_json")
@patch("onapsdk.sdc2.vendor.SdcOnboardingApiItem.update")
@patch("onapsdk.sdc2.vendor.SdcOnboardingApiItem.latest_version_url", new_callable=PropertyMock)
def test_vendor_submit(mock_url, mock_update, mock_send_message_json):
    mock_url.return_value = "test_url"
    v = Vendor("test", "vlm", "123", "test_Desc", "cs0008", "ACTIVE", {})
    v.submit()
    mock_send_message_json.assert_called_once()
    mock_update.assert_called_once()


@patch("onapsdk.sdc2.vendor.Vendor.send_message")
def test_vendor_delete(mock_send_message):
    v = Vendor("test", "vlm", "123", "test_Desc", "cs0008", "ACTIVE", {})
    v.delete()
    mock_send_message.assert_called_once()


@patch("onapsdk.sdc2.vendor.SdcOnboardingApiItem.get_all")
def test_vendor_get_by_name(mock_get_all):
    mock_get_all.return_value = []
    with raises(ResourceNotFound):
        Vendor.get_by_name("test_name")
    item_mock = MagicMock()
    item_mock.name = "test_name"
    mock_get_all.return_value = [item_mock]
    v = Vendor.get_by_name("test_name")
    assert v.name == "test_name"


@patch("onapsdk.sdc2.vendor.Vendor.send_message_json")
@patch("onapsdk.sdc2.sdc_onboarding_api.SdcOnboardingApiItemVersion.create_from_api_response")
def test_vendor_versions(mock_create_from_api, mock_send_message_json):
    v = Vendor("test", "vlm", "123", "test_Desc", "cs0008", "ACTIVE", {})
    mock_send_message_json.return_value = {}
    assert list(v.versions) == []

    mock_send_message_json.return_value = {"results": [{}]}
    assert len(list(v.versions)) == 1
    mock_create_from_api.assert_called_once()
