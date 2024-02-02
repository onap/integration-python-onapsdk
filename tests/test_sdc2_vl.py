
import json
from collections import namedtuple
from random import choice, randint
from sys import maxsize
from tempfile import NamedTemporaryFile
from unittest.mock import patch, PropertyMock
from uuid import uuid4

from pytest import raises

from onapsdk.exceptions import ResourceNotFound
from onapsdk.sdc2.sdc_resource import LifecycleState, LifecycleOperation
from onapsdk.sdc2.vl import Vl, ResoureTypeEnum


def test_pnf_resource_type():
    assert Vl.resource_type() == ResoureTypeEnum.VL


def test_copy_vl():
    vl1 = Vl(name="test_vl1")
    vl2 = Vl(name="test_vl2")
    assert vl1.name == "test_vl1"
    assert vl2.name == "test_vl2"
    assert vl1 != vl2
    vl2._copy_object(vl1)
    assert vl1.name == "test_vl1"
    assert vl2.name == "test_vl1"
    assert vl1 == vl2


@patch("onapsdk.sdc2.vl.Vl._get_active_rough")
@patch("onapsdk.sdc2.vl.Vl._get_archived_rough")
def test_get_all_rough(mock_get_archived, mock_get_active):
    Vl._get_all_rough()
    mock_get_archived.assert_called_once()
    mock_get_active.assert_called_once()


@patch("onapsdk.sdc2.vl.Vl._get_all_rough")
@patch("onapsdk.sdc2.vl.Vl.get_by_name_and_version")
def test_get_by_name(mock_get_by_name_and_version, mock_get_all_rough):
    mock_get_all_rough.return_value = []
    with raises(ResourceNotFound):
        Vl.get_by_name("test_1")

    mock_get_all_rough.return_value = [
        {
            "name": "not_test_1",
            "version": "1.0"
        }
    ]
    with raises(ResourceNotFound):
        Vl.get_by_name("test_1")

    mock_get_all_rough.return_value = [
        {
            "name": "not_test_1",
            "version": "1.0"
        },
        {
            "name": "test_1",
            "version": "1.0"
        }
    ]
    Vl.get_by_name("test_1")
    mock_get_by_name_and_version.assert_called_once_with("test_1", "1.0")

    mock_get_by_name_and_version.reset_mock()
    mock_get_all_rough.return_value = [
        {
            "name": "not_test_1",
            "version": "1.0"
        },
        {
            "name": "test_1",
            "version": "1.0"
        },
        {
            "name": "test_1",
            "version": "2.0"
        }
    ]
    Vl.get_by_name("test_1")
    mock_get_by_name_and_version.assert_called_once_with("test_1", "2.0")


@patch("onapsdk.sdc2.vl.Vl.send_message")
def test_delete(mock_send_message_json):
    vl = Vl(name="test_vl", unique_id="test_vl_unique_id")
    vl.delete()
    mock_send_message_json.assert_called_once()
    method, log, url = mock_send_message_json.mock_calls[0].args
    assert method == "DELETE"
    assert "test_vl" in log
    assert url.endswith("test_vl_unique_id")


@patch("onapsdk.sdc2.vl.Vl.send_message")
def test_archive(mock_send_message_json):
    vl = Vl(name="test_vl", unique_id="test_vl_unique_id")
    vl.archive()
    mock_send_message_json.assert_called_once()
    method, log, url = mock_send_message_json.mock_calls[0].args
    assert method == "POST"
    assert "test_vl" in log
    assert url.endswith("test_vl_unique_id/archive")


@patch("onapsdk.sdc2.vl.Vl._get_all_rough")
@patch("onapsdk.sdc2.vl.Vl.get_by_name_and_version")
def test_get_all(mock_get_by_name_and_version, mock_get_all_rough):
    mock_get_all_rough.return_value = []
    Vl.get_all()
    mock_get_by_name_and_version.assert_not_called()

    mock_get_all_rough.return_value = [
        {
            "name": "test_vl_1",
            "version": "1.0"
        }
    ]
    list(Vl.get_all())
    mock_get_by_name_and_version.assert_called_once_with("test_vl_1", "1.0")

    mock_get_by_name_and_version.reset_mock()
    mock_get_all_rough.return_value = (
        {
            "name": f"test_vl_{idx}",
            "version": f"{idx}.0"
        } for idx in range(100)
    )
    list(Vl.get_all())
    assert len(mock_get_by_name_and_version.mock_calls) == 100


@patch("onapsdk.sdc2.vl.Vl.send_message_json")
def test_get_active_rough(mock_send_message_json):
    mock_send_message_json.return_value = {"resources": []}
    assert(len(list(Vl._get_active_rough()))) == 0

    mock_send_message_json.return_value = {"resources": [
        {
            "resourceType": "VF"
        },
        {
            "resourceType": "PNF"
        },
        {
            "resourceType": "VL"
        }
    ]}
    assert(len(list(Vl._get_active_rough()))) == 1


@patch("onapsdk.sdc2.vl.Vl.send_message_json")
def test_get_archive_rough(mock_send_message_json):
    mock_send_message_json.return_value = {"resources": []}
    assert(len(list(Vl._get_archived_rough()))) == 0

    mock_send_message_json.return_value = {"resources": [
        {
            "resourceType": "VF"
        },
        {
            "resourceType": "PNF"
        },
        {
            "resourceType": "VL"
        }
    ]}
    assert(len(list(Vl._get_archived_rough()))) == 1


def test_get_by_name_and_version_endpoint():
    for i in range(1000):
        assert Vl.get_by_name_and_version_endpoint(
            name=f"vl_{i}",
            version=f"v{i}.0").endswith(
                f"catalog/resources/resourceName/vl_{i}/resourceVersion/v{i}.0")


def test_add_deployment_artifact_endpoint():
    for _ in range(10**3):
        object_id: str = str(uuid4())
        assert Vl.add_deployment_artifact_endpoint(
            object_id=object_id
        ) == f"sdc2/rest/v1/catalog/resources/{object_id}/artifacts"



def test_update():
    vl = Vl(
        name=str(uuid4()),
        unique_id=str(uuid4()),
        uuid=str(uuid4()),
        invariant_uuid=str(uuid4()),
        version=str(uuid4()),
        last_update_date=randint(0, maxsize),
        lifecycle_state=choice(list(LifecycleState)),
        last_updater_user_id=str(uuid4()),
        all_versions=[str(uuid4()) for _ in range(10**3)]
    )
    update_dict = {
        "uniqueId": str(uuid4()),
        "uuid": str(uuid4()),
        "invariantUUID": str(uuid4()),
        "version": str(uuid4()),
        "lastUpdateDate": randint(0, maxsize),
        "lifecycleState": choice(list(LifecycleState)),
        "lastUpdaterUserId": str(uuid4()),
        "allVersions": [str(uuid4()) for _ in range(10**3)]
    }
    vl.update(update_dict)
    assert vl.unique_id == update_dict["uniqueId"]
    assert vl.uuid == update_dict["uuid"]
    assert vl.invariant_uuid == update_dict["invariantUUID"]
    assert vl.version == update_dict["version"]
    assert vl.last_update_date == update_dict["lastUpdateDate"]
    assert vl.lifecycle_state == update_dict["lifecycleState"]
    assert vl.last_updater_user_id == update_dict["lastUpdaterUserId"]
    assert vl.all_versions == update_dict["allVersions"]


@patch("onapsdk.sdc2.vl.Vl.send_message_json")
@patch("onapsdk.sdc2.vl.Vl.update")
def test_lifecycle_operation(mock_update, mock_send_message_json):
    for lifecycle_operation in LifecycleOperation:
        mock_send_message_json.reset_mock()
        mock_update.reset_mock()
        return_dict = {
            "uniqueId": str(uuid4()),
            "uuid": str(uuid4()),
            "invariantUUID": str(uuid4()),
            "version": str(uuid4()),
            "lastUpdateDate": randint(0, maxsize),
            "lifecycleState": choice(list(LifecycleState)),
            "lastUpdaterUserId": str(uuid4()),
            "allVersions": [str(uuid4()) for _ in range(10**3)]
        }
        mock_send_message_json.return_value = return_dict
        vl_unique_id = str(uuid4())
        vl = Vl(
            name=str(uuid4()),
            unique_id=vl_unique_id
        )
        vl.lifecycle_operation(lifecycle_operation)
        mock_send_message_json.assert_called_once()
        method, log, url = mock_send_message_json.mock_calls[0].args
        data = mock_send_message_json.mock_calls[0].kwargs["data"]
        assert method == "POST"
        assert log.startswith(f"Request lifecycle operation {lifecycle_operation.value}")
        assert url.endswith(f"sdc2/rest/v1/catalog/resources/{vl_unique_id}/lifecycleState/{lifecycle_operation.value}")
        assert json.loads(data)["userRemarks"] == str(lifecycle_operation.value).lower()
        mock_update.assert_called_once_with(return_dict)


@patch("onapsdk.sdc2.vl.Vl.send_message_json")
@patch("onapsdk.sdc2.vl.Vl.get_by_name_and_version_endpoint")
def test_get_by_name_and_version(mock_get_endpoint, mock_send_message_json):
    for name, version in [(str(uuid4()), str(uuid4())) for _ in range(10**2)]:
        mock_send_message_json.reset_mock()
        mock_send_message_json.return_value = {
            "uniqueId": str(uuid4()),
            "uuid": str(uuid4()),
            "invariantUUID": str(uuid4()),
            "version": str(uuid4()),
            "lastUpdateDate": randint(0, maxsize),
            "lifecycleState": choice(list(LifecycleState)),
            "lastUpdaterUserId": str(uuid4()),
            "allVersions": [str(uuid4()) for _ in range(10**2)],
            "archived": choice([True, False]),
            "creationDate": randint(0, maxsize),
            "componentType": str(uuid4()),
            "description": str(uuid4()),
            "icon": str(uuid4()),
            "name": str(uuid4()),
            "systemName": str(uuid4()),
            "tags": [str(uuid4()) for _ in range(10**2)],
        }
        mock_get_endpoint.reset_mock()
        mock_get_endpoint.return_value = f"{name}/{version}"
        Vl.get_by_name_and_version(name, version)
        mock_send_message_json.assert_called_once()
        method, log, _ = mock_send_message_json.mock_calls[0].args
        assert method == "GET"
        assert log == "Get Vl by name and version"
        mock_get_endpoint.assert_called_once_with(name, version)


@patch("onapsdk.sdc2.vl.Vl.send_message_json")
def test_add_deployment_artifact(mock_send_message_json):
    with NamedTemporaryFile() as temp_file:
        temp_file.write(b"Hello world!")
        temp_file.seek(0)

        vl = Vl(name=str(uuid4()), unique_id=str(uuid4()))
        vl.add_deployment_artifact(
            str(uuid4()),
            str(uuid4()),
            str(uuid4()),
            temp_file.name
        )
        mock_send_message_json.assert_called_once()


@patch("onapsdk.sdc2.vl.Vl.send_message_json")
@patch("onapsdk.sdc2.sdc_resource.ComponentInstance.create_from_api_response")
def test_get_component_instances(mock_create_component_instance, mock_send_message_json):
    vl = Vl(name=str(uuid4()), unique_id=str(uuid4()))
    mock_send_message_json.return_value = []
    assert len(list(vl.component_instances)) == 0
    mock_send_message_json.assert_called_once_with(
        "GET",
        "Get Vl component instances",
        f"{vl.base_back_url}/sdc2/rest/v1/catalog/resources/{vl.unique_id}/componentInstances"
    )

    mock_send_message_json.return_value = [{}]
    assert len(list(vl.component_instances)) == 1
    mock_create_component_instance.assert_called_once_with({}, vl)


@patch("onapsdk.sdc2.vl.Vl.component_instances", new_callable=PropertyMock)
def test_get_component_by_name(mock_component_instances):
    ComponentInstance = namedtuple("ComponentInstance", ["component_name"])

    vl = Vl(name="test_component_instances")
    mock_component_instances.return_value = []
    assert vl.get_component_by_name("test_name") is None

    mock_component_instances.return_value = [ComponentInstance(component_name="test_name")]
    assert vl.get_component_by_name("test_name") is not None
    assert vl.get_component_by_name("test_name").component_name == "test_name"

    mock_component_instances.return_value = [ComponentInstance(component_name=f"test_name_{i}") for i in range(10**2)]
    assert vl.get_component_by_name("test_name") is None

    random_name = f"test_name_{choice(range(10**2))}"
    assert vl.get_component_by_name(random_name) is not None
    assert vl.get_component_by_name(random_name).component_name == random_name
