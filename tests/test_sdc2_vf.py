
import json
from collections import namedtuple
from random import choice, randint
from sys import maxsize
from tempfile import NamedTemporaryFile
from unittest.mock import MagicMock, patch, PropertyMock
from uuid import uuid4

from pytest import raises

from onapsdk.exceptions import ResourceNotFound
from onapsdk.sdc2.sdc_resource import LifecycleState, LifecycleOperation
from onapsdk.sdc2.vf import Vf, ResoureTypeEnum


def test_pnf_resource_type():
    assert Vf.resource_type() == ResoureTypeEnum.VF


def test_pnf_create_payload_template():
    assert Vf.create_payload_template() == "sdc2_create_vf.json.j2"


def test_copy_vf():
    vf1 = Vf(name="test_vf1")
    vf2 = Vf(name="test_vf2")
    assert vf1.name == "test_vf1"
    assert vf2.name == "test_vf2"
    assert vf1 != vf2
    vf2._copy_object(vf1)
    assert vf1.name == "test_vf1"
    assert vf2.name == "test_vf1"
    assert vf1 == vf2


@patch("onapsdk.sdc2.vf.Vf._get_active_rough")
@patch("onapsdk.sdc2.vf.Vf._get_archived_rough")
def test_get_all_rough(mock_get_archived, mock_get_active):
    Vf._get_all_rough()
    mock_get_archived.assert_called_once()
    mock_get_active.assert_called_once()


@patch("onapsdk.sdc2.vf.Vf._get_all_rough")
@patch("onapsdk.sdc2.vf.Vf.get_by_name_and_version")
def test_get_by_name(mock_get_by_name_and_version, mock_get_all_rough):
    mock_get_all_rough.return_value = []
    with raises(ResourceNotFound):
        Vf.get_by_name("test_1")

    mock_get_all_rough.return_value = [
        {
            "name": "not_test_1",
            "version": "1.0"
        }
    ]
    with raises(ResourceNotFound):
        Vf.get_by_name("test_1")

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
    Vf.get_by_name("test_1")
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
    Vf.get_by_name("test_1")
    mock_get_by_name_and_version.assert_called_once_with("test_1", "2.0")


@patch("onapsdk.sdc2.vf.Vf.send_message")
def test_delete(mock_send_message_json):
    vf = Vf(name="test_vf", unique_id="test_vf_unique_id")
    vf.delete()
    mock_send_message_json.assert_called_once()
    method, log, url = mock_send_message_json.mock_calls[0].args
    assert method == "DELETE"
    assert "test_vf" in log
    assert url.endswith("test_vf_unique_id")


@patch("onapsdk.sdc2.vf.Vf.send_message")
def test_archive(mock_send_message_json):
    vf = Vf(name="test_vf", unique_id="test_vf_unique_id")
    vf.archive()
    mock_send_message_json.assert_called_once()
    method, log, url = mock_send_message_json.mock_calls[0].args
    assert method == "POST"
    assert "test_vf" in log
    assert url.endswith("test_vf_unique_id/archive")


@patch("onapsdk.sdc2.vf.Vf._get_all_rough")
@patch("onapsdk.sdc2.vf.Vf.get_by_name_and_version")
def test_get_all(mock_get_by_name_and_version, mock_get_all_rough):
    mock_get_all_rough.return_value = []
    Vf.get_all()
    mock_get_by_name_and_version.assert_not_called()

    mock_get_all_rough.return_value = [
        {
            "name": "test_vf_1",
            "version": "1.0"
        }
    ]
    list(Vf.get_all())
    mock_get_by_name_and_version.assert_called_once_with("test_vf_1", "1.0")

    mock_get_by_name_and_version.reset_mock()
    mock_get_all_rough.return_value = (
        {
            "name": f"test_vf_{idx}",
            "version": f"{idx}.0"
        } for idx in range(100)
    )
    list(Vf.get_all())
    assert len(mock_get_by_name_and_version.mock_calls) == 100


@patch("onapsdk.sdc2.vf.Vf.send_message_json")
def test_get_active_rough(mock_send_message_json):
    mock_send_message_json.return_value = {"resources": []}
    assert(len(list(Vf._get_active_rough()))) == 0

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
    assert(len(list(Vf._get_active_rough()))) == 1


@patch("onapsdk.sdc2.vf.Vf.send_message_json")
def test_get_archive_rough(mock_send_message_json):
    mock_send_message_json.return_value = {"resources": []}
    assert(len(list(Vf._get_archived_rough()))) == 0

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
    assert(len(list(Vf._get_archived_rough()))) == 1


def test_get_by_name_and_version_endpoint():
    for i in range(1000):
        assert Vf.get_by_name_and_version_endpoint(
            name=f"vf_{i}",
            version=f"v{i}.0").endswith(
                f"catalog/resources/resourceName/vf_{i}/resourceVersion/v{i}.0")


def test_add_deployment_artifact_endpoint():
    for _ in range(10**3):
        object_id: str = str(uuid4())
        assert Vf.add_deployment_artifact_endpoint(
            object_id=object_id
        ) == f"sdc2/rest/v1/catalog/resources/{object_id}/artifacts"


def test_update():
    vf = Vf(
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
    vf.update(update_dict)
    assert vf.unique_id == update_dict["uniqueId"]
    assert vf.uuid == update_dict["uuid"]
    assert vf.invariant_uuid == update_dict["invariantUUID"]
    assert vf.version == update_dict["version"]
    assert vf.last_update_date == update_dict["lastUpdateDate"]
    assert vf.lifecycle_state == update_dict["lifecycleState"]
    assert vf.last_updater_user_id == update_dict["lastUpdaterUserId"]
    assert vf.all_versions == update_dict["allVersions"]


@patch("onapsdk.sdc2.vf.Vf.send_message_json")
@patch("onapsdk.sdc2.vf.Vf.update")
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
        vf_unique_id = str(uuid4())
        vf = Vf(
            name=str(uuid4()),
            unique_id=vf_unique_id
        )
        vf.lifecycle_operation(lifecycle_operation)
        mock_send_message_json.assert_called_once()
        method, log, url = mock_send_message_json.mock_calls[0].args
        data = mock_send_message_json.mock_calls[0].kwargs["data"]
        assert method == "POST"
        assert log.startswith(f"Request lifecycle operation {lifecycle_operation.value}")
        assert url.endswith(f"sdc2/rest/v1/catalog/resources/{vf_unique_id}/lifecycleState/{lifecycle_operation.value}")
        assert json.loads(data)["userRemarks"] == str(lifecycle_operation.value).lower()
        mock_update.assert_called_once_with(return_dict)


@patch("onapsdk.sdc2.vf.Vf.send_message_json")
@patch("onapsdk.sdc2.vf.Vf.get_by_name_and_version_endpoint")
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
        Vf.get_by_name_and_version(name, version)
        mock_send_message_json.assert_called_once()
        method, log, _ = mock_send_message_json.mock_calls[0].args
        assert method == "GET"
        assert log == "Get Vf by name and version"
        mock_get_endpoint.assert_called_once_with(name, version)


@patch("onapsdk.sdc2.vf.Vf.send_message_json")
def test_add_deployment_artifact(mock_send_message_json):
    with NamedTemporaryFile() as temp_file:
        temp_file.write(b"Hello world!")
        temp_file.seek(0)

        vf = Vf(name=str(uuid4()), unique_id=str(uuid4()))
        vf.add_deployment_artifact(
            str(uuid4()),
            str(uuid4()),
            str(uuid4()),
            temp_file.name
        )
        mock_send_message_json.assert_called_once()


@patch("onapsdk.sdc2.vf.Vf.send_message_json")
@patch("onapsdk.sdc2.sdc_resource.ComponentInstance.create_from_api_response")
def test_add_deployment_artifact(mock_create_component_instance, mock_send_message_json):
    vf = Vf(name=str(uuid4()), unique_id=str(uuid4()))
    mock_send_message_json.return_value = []
    assert len(list(vf.component_instances)) == 0
    mock_send_message_json.assert_called_once_with(
        "GET",
        "Get Vf component instances",
        f"{vf.base_back_url}/sdc2/rest/v1/catalog/resources/{vf.unique_id}/componentInstances"
    )

    mock_send_message_json.return_value = [{}]
    assert len(list(vf.component_instances)) == 1
    mock_create_component_instance.assert_called_once_with({}, vf)


@patch("onapsdk.sdc2.vf.Vf.component_instances", new_callable=PropertyMock)
def test_get_component_by_name(mock_component_instances):
    ComponentInstance = namedtuple("ComponentInstance", ["component_name"])

    vf = Vf(name="test_component_instances")
    mock_component_instances.return_value = []
    assert vf.get_component_by_name("test_name") is None

    mock_component_instances.return_value = [ComponentInstance(component_name="test_name")]
    assert vf.get_component_by_name("test_name") is not None
    assert vf.get_component_by_name("test_name").component_name == "test_name"

    mock_component_instances.return_value = [ComponentInstance(component_name=f"test_name_{i}") for i in range(10**2)]
    assert vf.get_component_by_name("test_name") is None

    random_name = f"test_name_{choice(range(10**2))}"
    assert vf.get_component_by_name(random_name) is not None
    assert vf.get_component_by_name(random_name).component_name == random_name


@patch("onapsdk.sdc2.vf.Vf.send_message_json")
@patch("onapsdk.sdc2.vf.Vf.get_create_payload")
@patch("onapsdk.sdc2.vf.Vf.create_from_api_response")
def test_create(mock_create_from_api_response, mock_get_create_payload, mock_send_message_json):
    mock_get_create_payload.return_value = "test_payload"
    Vf.create(name="test_vf")
    mock_send_message_json.assert_called_once_with(
        "POST",
        "Create VF test_vf",
        Vf.CREATE_ENDPOINT,
        data="test_payload"
    )


@patch("onapsdk.sdc2.sdc_resource.ResourceCategory.get_by_name")
def test_get_create_payload(mock_resource_category_get_by_name):
    mock_vsp = MagicMock(csar_uuid="test_vsp_csar_uuid")
    mock_vendor = MagicMock()
    mock_vendor.name = "test_vendor_name"
    resource_category_mock = MagicMock()
    resource_category_mock.name = "test_category"
    resource_category_mock.unique_id = "category_unique_id"
    resource_subcategory_mock = MagicMock()
    resource_subcategory_mock.name = "test_subcategory"
    resource_subcategory_mock.unique_id = "subcategory_unique_id"
    resource_category_mock.get_subcategory.return_value = resource_subcategory_mock
    mock_resource_category_get_by_name.return_value = resource_category_mock

    create_payload = json.loads(Vf.get_create_payload(
        name="test_vf",
        vsp=mock_vsp,
        vendor=mock_vendor
    ))
    assert create_payload["name"] == "test_vf"
    assert create_payload["contactId"] == "cs0008"
    assert create_payload["componentType"] == "RESOURCE"
    assert create_payload["csarUUID"] == "test_vsp_csar_uuid"
    assert create_payload["csarVersion"] == "1.0"
    assert create_payload["categories"][0]["name"] == "test_category"
    assert create_payload["categories"][0]["uniqueId"] == "category_unique_id"
    assert create_payload["categories"][0]["subcategories"][0]["name"] == "test_subcategory"
    assert create_payload["categories"][0]["subcategories"][0]["uniqueId"] == "subcategory_unique_id"
    assert create_payload["resourceType"] == "VF"
    assert create_payload["description"] == "ONAP SDK Resource"
    assert create_payload["vendorName"] == "test_vendor_name"
    assert create_payload["vendorRelease"] == "1.0"

    create_payload = json.loads(Vf.get_create_payload(
        name="test_vf",
        vsp=mock_vsp,
        vendor=mock_vendor,
        description="test description"
    ))
    assert create_payload["name"] == "test_vf"
    assert create_payload["contactId"] == "cs0008"
    assert create_payload["componentType"] == "RESOURCE"
    assert create_payload["csarUUID"] == "test_vsp_csar_uuid"
    assert create_payload["csarVersion"] == "1.0"
    assert create_payload["categories"][0]["name"] == "test_category"
    assert create_payload["categories"][0]["uniqueId"] == "category_unique_id"
    assert create_payload["categories"][0]["subcategories"][0]["name"] == "test_subcategory"
    assert create_payload["categories"][0]["subcategories"][0]["uniqueId"] == "subcategory_unique_id"
    assert create_payload["resourceType"] == "VF"
    assert create_payload["description"] == "test description"
    assert create_payload["vendorName"] == "test_vendor_name"
    assert create_payload["vendorRelease"] == "1.0"

