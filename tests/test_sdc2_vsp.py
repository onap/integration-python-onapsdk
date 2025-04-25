
from unittest.mock import MagicMock, patch, PropertyMock
from onapsdk.exceptions import ValidationError
from onapsdk.sdc2.vsp import Vsp, SdcOnboardingApiItemTypeEnum

from pytest import raises


def test_vsp_item_type():
    vsp = Vsp("test_name", "test_item_type", "test_item_id", "test_description", "test_owner", "ACTIVE", {})
    assert vsp.get_item_type() == SdcOnboardingApiItemTypeEnum.VSP


@patch("onapsdk.sdc2.vsp.Vsp.send_message_json")
def test_create_vsp(mock_send_message_json):
    mock_send_message_json.side_effect = [
        {
            "itemId": "123"
        },
        {
            "name": "test_name",
            "id": "123",
            "description": "123",
            "status": "ACTIVE",
            "type": "vsp",
            "owner": "cs0008",
            "properties": {}
        }
    ]
    v = Vsp.create("test_name", MagicMock())
    mock_send_message_json.assert_called()
    assert v.name == "test_name"
    assert v.vsp_id == "123"


@patch("onapsdk.sdc2.vsp.Vsp.send_message")
@patch("onapsdk.sdc2.vsp.Vsp.latest_version", new_callable=PropertyMock)
def test_vsp_upload_package(mock_latest_version, mock_send_message):
    vsp = Vsp(name="test_vsp", item_type="vsp", item_id="123",
              description="test_desc", owner="test_owner", status="ACTIVE",
              properties={})
    vsp.upload_package(MagicMock())
    mock_send_message.assert_called_once()


@patch("onapsdk.sdc2.vsp.Vsp.send_message_json")
@patch("onapsdk.sdc2.vsp.Vsp.latest_version", new_callable=PropertyMock)
def test_vsp_process_package(_, mock_send_message_json):
    vsp = Vsp(name="test_vsp", item_type="vsp", item_id="123",
              description="test_desc", owner="test_owner", status="ACTIVE",
              properties={})
    mock_send_message_json.return_value = {
        "status": "FAILED"
    }
    with raises(ValidationError):
        vsp.process_package(raise_on_failure=True)
    mock_send_message_json.assert_called_once()
    vsp.process_package(raise_on_failure=False)

    mock_send_message_json.reset_mock()
    mock_send_message_json.return_value = {
        "status": "SUCCESS"
    }
    vsp.process_package(raise_on_failure=True)


@patch("onapsdk.sdc2.vsp.Vsp.send_message")
@patch("onapsdk.sdc2.vsp.Vsp.latest_version", new_callable=PropertyMock)
@patch("onapsdk.sdc2.vsp.SdcOnboardingApiItem.update")
def test_vsp_create_package(__, _, mock_send_message):
    vsp = Vsp(name="test_vsp", item_type="vsp", item_id="123",
              description="test_desc", owner="test_owner", status="ACTIVE",
              properties={})
    vsp.create_package()
    mock_send_message.assert_called_once()


@patch("onapsdk.sdc2.vsp.Vendor.get_by_name")
def test_vsp_vendor(mock_vendor_get_by_name):
    vsp = Vsp(name="test_vsp", item_type="vsp", item_id="123",
              description="test_desc", owner="test_owner", status="ACTIVE",
              properties={"vendorName": "testVendor"})
    assert vsp.vendor is not None
    mock_vendor_get_by_name.assert_called_once_with("testVendor")


@patch("onapsdk.sdc2.vsp.Vsp.send_message_json")
@patch("onapsdk.sdc2.vsp.SdcOnboardingApiItem.update")
@patch("onapsdk.sdc2.vsp.Vsp.latest_version", new_callable=PropertyMock)
def test_csar_csar_uuidd(_, __, mock_send_message_json):
    vsp = Vsp(name="test_vsp", item_type="vsp", item_id="123",
              description="test_desc", owner="test_owner", status="ACTIVE",
              properties={"vendorName": "testVendor"})
    assert vsp._csar_uuid is None
    mock_send_message_json.return_value = {"packageId": "123"}
    assert vsp.csar_uuid == "123"
