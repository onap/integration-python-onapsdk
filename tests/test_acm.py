from unittest.mock import patch, MagicMock

from requests import Response

from onapsdk.clamp.acm import Acm
from onapsdk.configuration import settings

BASIC_AUTH = {"username": "runtimeUser", "password": "test"}
BASE = settings.CLAMP_ACM_URL + "/onap/policy/clamp/acm/v2"


def test_base_url():
    assert Acm.base_url() == BASE


@patch("onapsdk.clamp.acm.Acm.send_message")
def test_commission(mock_send_message):
    mock_response = MagicMock(spec=Response)
    mock_response.json.return_value = {"compositionId": "abc"}
    mock_send_message.return_value = mock_response
    template = {"name": "Simple"}
    response = Acm.commission(template, BASIC_AUTH)
    assert response.json()["compositionId"] == "abc"
    mock_send_message.assert_called_once_with(
        "POST", "Commission automation composition definition",
        BASE + "/compositions",
        basic_auth=BASIC_AUTH, json=template)


@patch("onapsdk.clamp.acm.Acm.send_message")
def test_get_composition(mock_send_message):
    mock_send_message.return_value = MagicMock(spec=Response)
    Acm.get_composition("abc", BASIC_AUTH)
    mock_send_message.assert_called_once_with(
        "GET", "Get automation composition definition",
        BASE + "/compositions/abc",
        basic_auth=BASIC_AUTH)


@patch("onapsdk.clamp.acm.Acm.send_message")
def test_set_composition_state(mock_send_message):
    mock_send_message.return_value = MagicMock(spec=Response)
    Acm.set_composition_state("abc", "PRIME", BASIC_AUTH)
    mock_send_message.assert_called_once_with(
        "PUT", "Set automation composition definition state",
        BASE + "/compositions/abc",
        basic_auth=BASIC_AUTH, json={"primeOrder": "PRIME"})


@patch("onapsdk.clamp.acm.Acm.send_message")
def test_delete_composition(mock_send_message):
    mock_send_message.return_value = MagicMock(spec=Response)
    Acm.delete_composition("abc", BASIC_AUTH)
    mock_send_message.assert_called_once_with(
        "DELETE", "Delete automation composition definition",
        BASE + "/compositions/abc",
        basic_auth=BASIC_AUTH)


@patch("onapsdk.clamp.acm.Acm.send_message")
def test_create_instance(mock_send_message):
    mock_response = MagicMock(spec=Response)
    mock_response.json.return_value = {"instanceId": "def"}
    mock_send_message.return_value = mock_response
    instance = {"name": "SimpleInstance"}
    response = Acm.create_instance("abc", instance, BASIC_AUTH)
    assert response.json()["instanceId"] == "def"
    mock_send_message.assert_called_once_with(
        "POST", "Create automation composition instance",
        BASE + "/compositions/abc/instances",
        basic_auth=BASIC_AUTH, json=instance)


@patch("onapsdk.clamp.acm.Acm.send_message")
def test_get_instance(mock_send_message):
    mock_send_message.return_value = MagicMock(spec=Response)
    Acm.get_instance("abc", "def", BASIC_AUTH)
    mock_send_message.assert_called_once_with(
        "GET", "Get automation composition instance",
        BASE + "/compositions/abc/instances/def",
        basic_auth=BASIC_AUTH)


@patch("onapsdk.clamp.acm.Acm.send_message")
def test_set_instance_state(mock_send_message):
    mock_send_message.return_value = MagicMock(spec=Response)
    Acm.set_instance_state("abc", "def", "DEPLOY", BASIC_AUTH)
    mock_send_message.assert_called_once_with(
        "PUT", "Set automation composition instance state",
        BASE + "/compositions/abc/instances/def",
        basic_auth=BASIC_AUTH, json={"deployOrder": "DEPLOY"})


@patch("onapsdk.clamp.acm.Acm.send_message")
def test_delete_instance(mock_send_message):
    mock_send_message.return_value = MagicMock(spec=Response)
    Acm.delete_instance("abc", "def", BASIC_AUTH)
    mock_send_message.assert_called_once_with(
        "DELETE", "Delete automation composition instance",
        BASE + "/compositions/abc/instances/def",
        basic_auth=BASIC_AUTH)
