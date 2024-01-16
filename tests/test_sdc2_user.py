from collections import namedtuple
from random import choice, randint
from sys import maxsize
from unittest.mock import patch
from uuid import uuid4

from pytest import raises

from onapsdk.exceptions import ResourceNotFound
from onapsdk.sdc2.sdc_user import SdcUser


@patch("onapsdk.sdc2.sdc_user.SdcUser.send_message_json")
@patch("onapsdk.sdc2.sdc_user.SdcUser.create_from_api_response")
def test_get_all(mock_create_from_api_response, mock_send_message_json):
    mock_send_message_json.return_value = []

    assert len(list(SdcUser.get_all())) == 0
    mock_create_from_api_response.assert_not_called()

    mock_send_message_json.return_value = [{}]
    assert len(list(SdcUser.get_all())) == 1
    mock_create_from_api_response.assert_called_once_with({})


@patch("onapsdk.sdc2.sdc_user.SdcUser.get_all")
def test_get_by_user_id(mock_get_all):
    mock_get_all.return_value = []
    with raises(ResourceNotFound):
        SdcUser.get_by_user_id("test_user")

    TestUser = namedtuple("TestUser", ["user_id"])
    mock_get_all.return_value = [TestUser("not_test_user")]
    with raises(ResourceNotFound):
        SdcUser.get_by_user_id("test_user")

    mock_get_all.return_value = [TestUser("test_user")]
    assert SdcUser.get_by_user_id("test_user") is not None


def test_create_from_api_response():
    api_response = {
        "userId": str(uuid4()),
        "role": str(uuid4()),
        "email": str(uuid4()),
        "firstName": str(uuid4()),
        "fullName": str(uuid4()),
        "lastLoginTime": randint(0, maxsize),
        "lastName": str(uuid4()),
        "status": choice(list(SdcUser.SdcUserStatus))
    }
    sdc_user = SdcUser.create_from_api_response(api_response)
    assert sdc_user.user_id == api_response["userId"]
    assert sdc_user.role == api_response["role"]
    assert sdc_user.email == api_response["email"]
    assert sdc_user.first_name == api_response["firstName"]
    assert sdc_user.last_login_time == api_response["lastLoginTime"]
    assert sdc_user.last_name == api_response["lastName"]
    assert sdc_user.full_name == api_response["fullName"]
    assert sdc_user.status == SdcUser.SdcUserStatus(api_response["status"])
