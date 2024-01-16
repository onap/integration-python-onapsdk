
from collections import namedtuple
from json import loads
from random import randint
from sys import maxsize
from unittest.mock import MagicMock, patch, PropertyMock
from uuid import uuid4

from onapsdk.configuration import settings
from onapsdk.sdc2.component_instance import ComponentInstance, ComponentInstanceInput


def test_component_instance_create_from_api_response():
    data = {
        "actualComponentUid": str(uuid4()),
        "componentName": str(uuid4()),
        "componentUid": str(uuid4()),
        "componentVersion": str(uuid4()),
        "creationTime": randint(0, maxsize),
        "customizationUUID": str(uuid4()),
        "icon": str(uuid4()),
        "invariantName": str(uuid4()),
        "isProxy": bool(randint(0, 1)),
        "modificationTime": randint(0, maxsize),
        "name": str(uuid4()),
        "normalizedName": str(uuid4()),
        "originType": str(uuid4()),
        "toscaComponentName": str(uuid4()),
        "uniqueId": str(uuid4()),
    }
    ci = ComponentInstance.create_from_api_response(
        data, sdc_resource=MagicMock()
    )
    assert ci.name == data["name"]
    assert ci.actual_component_uid == data["actualComponentUid"]
    assert ci.component_name == data["componentName"]
    assert ci.component_uid == data["componentUid"]
    assert ci.component_version == data["componentVersion"]
    assert ci.creation_time == data["creationTime"]
    assert ci.customization_uuid == data["customizationUUID"]
    assert ci.icon == data["icon"]
    assert ci.invariant_name == data["invariantName"]
    assert ci.is_proxy == data["isProxy"]
    assert ci.modification_time == data["modificationTime"]
    assert ci.normalized_name == data["normalizedName"]
    assert ci.origin_type == data["originType"]
    assert ci.tosca_component_name == data["toscaComponentName"]
    assert ci.unique_id == data["uniqueId"]


@patch("onapsdk.sdc2.component_instance.ComponentInstanceInput.create_from_api_response")
@patch("onapsdk.sdc2.component_instance.ComponentInstance.send_message_json")
def test_component_instance_inputs(mock_send_message_json, mock_input_create_from_api_response):
    sdc_resource_mock = MagicMock(unique_id=str(uuid4()))
    sdc_resource_mock.catalog_type.return_value = "mocked"
    ci = ComponentInstance(
        actual_component_uid=str(uuid4()),
        component_name=str(uuid4()),
        component_uid=str(uuid4()),
        component_version=str(uuid4()),
        creation_time=randint(0, maxsize),
        customization_uuid=str(uuid4()),
        icon=str(uuid4()),
        invariant_name=str(uuid4()),
        is_proxy=bool(randint(0, 1)),
        modification_time=randint(0, maxsize),
        name=str(uuid4()),
        normalized_name=str(uuid4()),
        origin_type=str(uuid4()),
        sdc_resource=sdc_resource_mock,
        tosca_component_name=str(uuid4()),
        unique_id=str(uuid4())
    )
    mock_send_message_json.return_value = []
    assert len(list(ci.inputs)) == 0
    mock_send_message_json.assert_called_once_with(
        "GET",
        "Get inputs",
        f"{settings.SDC_BE_URL}/sdc2/rest/v1/catalog/mocked/{sdc_resource_mock.unique_id}/componentInstances/{ci.unique_id}/{ci.actual_component_uid}/inputs"
    )

    mock_send_message_json.reset_mock()
    mock_send_message_json.return_value = [{}]
    assert len(list(ci.inputs)) == 1
    mock_input_create_from_api_response.assert_called_once_with({}, ci)
    mock_send_message_json.assert_called_once_with(
        "GET",
        "Get inputs",
        f"{settings.SDC_BE_URL}/sdc2/rest/v1/catalog/mocked/{sdc_resource_mock.unique_id}/componentInstances/{ci.unique_id}/{ci.actual_component_uid}/inputs"
    )


@patch("onapsdk.sdc2.component_instance.ComponentInstance.inputs", new_callable=PropertyMock)
def test_get_component_input_by_name(mock_inputs):
    ci = ComponentInstance(
        actual_component_uid=str(uuid4()),
        component_name=str(uuid4()),
        component_uid=str(uuid4()),
        component_version=str(uuid4()),
        creation_time=randint(0, maxsize),
        customization_uuid=str(uuid4()),
        icon=str(uuid4()),
        invariant_name=str(uuid4()),
        is_proxy=bool(randint(0, 1)),
        modification_time=randint(0, maxsize),
        name=str(uuid4()),
        normalized_name=str(uuid4()),
        origin_type=str(uuid4()),
        sdc_resource=MagicMock(),
        tosca_component_name=str(uuid4()),
        unique_id=str(uuid4())
    )

    mock_inputs.return_value = []
    assert ci.get_input_by_name("test_name") is None

    Input = namedtuple("Input", ["name"])
    mock_inputs.return_value = [Input("test_name")]
    assert ci.get_input_by_name("test_name") is not None

    mock_inputs.return_value = [Input(f"test_name_{i}") for i in range(10**2)]
    assert ci.get_input_by_name("test_name") is None

    mock_inputs.return_value = [Input(f"test_name_{i}") for i in range(10**2)]
    for i in range(10**2):
        assert ci.get_input_by_name(f"test_name_{i}") is not None


def test_component_instance_input_create_from_api_response():
    api_response={
        "definition": bool(randint(0, 1)),
        "hidden": bool(randint(0, 1)),
        "uniqueId": str(uuid4()),
        "type": str(uuid4()),
        "required": bool(randint(0, 1)),
        "password": bool(randint(0, 1)),
        "name": str(uuid4()),
        "immutable": bool(randint(0, 1)),
        "mappedToComponentProperty": bool(randint(0, 1)),
        "isDeclaredListInput": bool(randint(0, 1)),
        "userCreated": bool(randint(0, 1)),
        "getInputProperty": bool(randint(0, 1)),
        "empty": bool(randint(0, 1))
    }
    cli = ComponentInstanceInput.create_from_api_response(
        component_instance=MagicMock(),
        api_response=api_response
    )
    assert cli.name == api_response["name"]
    assert cli.definition == api_response["definition"]
    assert cli.hidden == api_response["hidden"]
    assert cli.unique_id == api_response["uniqueId"]
    assert cli.input_type == api_response["type"]
    assert cli.required == api_response["required"]
    assert cli.password == api_response["password"]
    assert cli.immutable == api_response["immutable"]
    assert cli.mapped_to_component_property == api_response["mappedToComponentProperty"]
    assert cli.is_declared_list_input == api_response["isDeclaredListInput"]
    assert cli.user_created == api_response["userCreated"]
    assert cli.get_input_property == api_response["getInputProperty"]
    assert cli.empty == api_response["empty"]
    assert cli.description is None
    assert cli.label is None
    assert cli.value is None


@patch("onapsdk.sdc2.component_instance.ComponentInstanceInput.send_message_json")
def test_component_instance_input_set_value(mock_send_message_json):
    sdc_resource_mock = MagicMock()
    sdc_resource_mock.name = "mocked sdc resource"
    sdc_resource_mock.catalog_type.return_value = "mocked"
    sdc_resource_mock.unique_id = "mockUid"
    component_instance_mock = MagicMock(sdc_resource=sdc_resource_mock)
    component_instance_mock.unique_id = "mockUid"
    cii = ComponentInstanceInput(
        component_instance=component_instance_mock,
        name=str(uuid4()),
        definition=bool(randint(0, 1)),
        hidden=bool(randint(0, 1)),
        required=bool(randint(0, 1)),
        password=bool(randint(0, 1)),
        immutable=bool(randint(0, 1)),
        mapped_to_component_property=bool(randint(0, 1)),
        is_declared_list_input=bool(randint(0, 1)),
        user_created=bool(randint(0, 1)),
        get_input_property=bool(randint(0, 1)),
        empty=bool(randint(0, 1)),
        unique_id=str(uuid4()),
        input_type=str(uuid4())
    )
    cii.value = "!23"
    mock_send_message_json.assert_called_once()
    method, log, url = mock_send_message_json.mock_calls[0].args
    data = loads(mock_send_message_json.mock_calls[0].kwargs["data"])
    assert method == "POST"
    assert log == f"Set value of mocked sdc resource resource input {cii.name}"
    assert url == f"{settings.SDC_BE_URL}/sdc2/rest/v1/catalog/mocked/mockUid/resourceInstance/mockUid/inputs"
    assert data[0]["name"] == cii.name
    assert data[0]["parentUniqueId"] == component_instance_mock.unique_id
    assert data[0]["type"] == cii.input_type
    assert data[0]["uniqueId"] == cii.unique_id
    assert data[0]["value"] == "!23"
    assert data[0]["toscaPresentation"]["ownerId"] == component_instance_mock.unique_id
