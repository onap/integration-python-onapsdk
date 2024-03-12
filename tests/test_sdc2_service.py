
import json
from collections import namedtuple
from random import choice, randint
from sys import maxsize
from tempfile import NamedTemporaryFile
from unittest.mock import MagicMock, patch, PropertyMock
from uuid import uuid4

from pytest import raises

from onapsdk.configuration import settings
from onapsdk.exceptions import ResourceNotFound
from onapsdk.sdc2.sdc_resource import LifecycleState, LifecycleOperation
from onapsdk.sdc2.service import ServiceInstantiationType, Service, ResoureTypeEnum, ServiceDistribution


def test_service_resource_type():
    assert Service.resource_type() == ResoureTypeEnum.SERVICE


def test_copy_service():
    service1 = Service(name="test_service1")
    service2 = Service(name="test_service2")
    assert service1.name == "test_service1"
    assert service2.name == "test_service2"
    assert service1 != service2
    service2._copy_object(service1)
    assert service1.name == "test_service1"
    assert service2.name == "test_service1"
    assert service1 == service2


@patch("onapsdk.sdc2.service.Service._get_active_rough")
@patch("onapsdk.sdc2.service.Service._get_archived_rough")
def test_get_all_rough(mock_get_archived, mock_get_active):
    Service._get_all_rough()
    mock_get_archived.assert_called_once()
    mock_get_active.assert_called_once()


@patch("onapsdk.sdc2.service.Service._get_all_rough")
@patch("onapsdk.sdc2.service.Service.get_by_name_and_version")
def test_get_by_name(mock_get_by_name_and_version, mock_get_all_rough):
    mock_get_all_rough.return_value = []
    with raises(ResourceNotFound):
        Service.get_by_name("test_1")

    mock_get_all_rough.return_value = [
        {
            "name": "not_test_1",
            "version": "1.0"
        }
    ]
    with raises(ResourceNotFound):
        Service.get_by_name("test_1")

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
    Service.get_by_name("test_1")
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
    Service.get_by_name("test_1")
    mock_get_by_name_and_version.assert_called_once_with("test_1", "2.0")


@patch("onapsdk.sdc2.service.Service.send_message")
def test_delete(mock_send_message_json):
    service = Service(name="test_service", unique_id="test_service_unique_id")
    service.delete()
    mock_send_message_json.assert_called_once()
    method, log, url = mock_send_message_json.mock_calls[0].args
    assert method == "DELETE"
    assert "test_service" in log
    assert url.endswith("test_service_unique_id")


@patch("onapsdk.sdc2.service.Service.send_message")
def test_archive(mock_send_message_json):
    service = Service(name="test_service", unique_id="test_service_unique_id")
    service.archive()
    mock_send_message_json.assert_called_once()
    method, log, url = mock_send_message_json.mock_calls[0].args
    assert method == "POST"
    assert "test_service" in log
    assert url.endswith("test_service_unique_id/archive")


@patch("onapsdk.sdc2.service.Service._get_all_rough")
@patch("onapsdk.sdc2.service.Service.get_by_name_and_version")
def test_get_all(mock_get_by_name_and_version, mock_get_all_rough):
    mock_get_all_rough.return_value = []
    Service.get_all()
    mock_get_by_name_and_version.assert_not_called()

    mock_get_all_rough.return_value = [
        {
            "name": "test_service_1",
            "version": "1.0"
        }
    ]
    list(Service.get_all())
    mock_get_by_name_and_version.assert_called_once_with("test_service_1", "1.0")

    mock_get_by_name_and_version.reset_mock()
    mock_get_all_rough.return_value = (
        {
            "name": f"test_service_{idx}",
            "version": f"{idx}.0"
        } for idx in range(100)
    )
    list(Service.get_all())
    assert len(mock_get_by_name_and_version.mock_calls) == 100


@patch("onapsdk.sdc2.service.Service.send_message_json")
def test_get_active_rough(mock_send_message_json):
    mock_send_message_json.return_value = {"resources": []}
    assert(len(list(Service._get_active_rough()))) == 0

    mock_send_message_json.return_value = {
        "resources": [
            {
                "resourceType": "VF"
            },
            {
                "resourceType": "PNF"
            },
            {
                "resourceType": "VL"
            }
        ],
        "services": [
            {
                "resourceType": "SERVICE"
            }
        ]
    }
    assert(len(list(Service._get_active_rough()))) == 1


@patch("onapsdk.sdc2.service.Service.send_message_json")
def test_get_archive_rough(mock_send_message_json):
    mock_send_message_json.return_value = {"resources": []}
    assert(len(list(Service._get_archived_rough()))) == 0

    mock_send_message_json.return_value = {
        "resources": [
            {
                "resourceType": "VF"
            },
            {
                "resourceType": "PNF"
            },
            {
                "resourceType": "VL"
            }
        ],
        "services": [
            {
                "resourceType": "SERVICE"
            }
        ]
    }
    assert(len(list(Service._get_archived_rough()))) == 1


def test_get_by_name_and_version_endpoint():
    for i in range(1000):
        assert Service.get_by_name_and_version_endpoint(
            name=f"service_{i}",
            version=f"v{i}.0").endswith(
                f"catalog/services/serviceName/service_{i}/serviceVersion/v{i}.0")


def test_add_deployment_artifact_endpoint():
    for _ in range(10**3):
        object_id: str = str(uuid4())
        assert Service.add_deployment_artifact_endpoint(
            object_id=object_id
        ) == f"sdc2/rest/v1/catalog/services/{object_id}/artifacts"


def test_update():
    service = Service(
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
        "allVersions": [str(uuid4()) for _ in range(10**3)],
        "distributionStatus": str(uuid4())
    }
    service.update(update_dict)
    assert service.unique_id == update_dict["uniqueId"]
    assert service.uuid == update_dict["uuid"]
    assert service.invariant_uuid == update_dict["invariantUUID"]
    assert service.version == update_dict["version"]
    assert service.last_update_date == update_dict["lastUpdateDate"]
    assert service.lifecycle_state == update_dict["lifecycleState"]
    assert service.last_updater_user_id == update_dict["lastUpdaterUserId"]
    assert service.all_versions == update_dict["allVersions"]
    assert service.distribuition_status == update_dict["distributionStatus"]


@patch("onapsdk.sdc2.service.Service.send_message_json")
@patch("onapsdk.sdc2.service.Service.update")
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
        service_unique_id = str(uuid4())
        service = Service(
            name=str(uuid4()),
            unique_id=service_unique_id
        )
        service.lifecycle_operation(lifecycle_operation)
        mock_send_message_json.assert_called_once()
        method, log, url = mock_send_message_json.mock_calls[0].args
        data = mock_send_message_json.mock_calls[0].kwargs["data"]
        assert method == "POST"
        assert log.startswith(f"Request lifecycle operation {lifecycle_operation.value}")
        assert url.endswith(f"sdc2/rest/v1/catalog/services/{service_unique_id}/lifecycleState/{lifecycle_operation.value}")
        assert json.loads(data)["userRemarks"] == str(lifecycle_operation.value).lower()
        mock_update.assert_called_once_with(return_dict)


@patch("onapsdk.sdc2.service.Service.send_message_json")
@patch("onapsdk.sdc2.service.Service.get_by_name_and_version_endpoint")
@patch("onapsdk.sdc2.service.ServiceCategory.get_by_uniqe_id")
def test_get_by_name_and_version(mock_get_category_by_unique_id, mock_get_endpoint, mock_send_message_json):
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
            "actualComponentType": str(uuid4()),
            "distributionStatus": str(uuid4()),
            "categories": [{"uniqueId": str(uuid4())} for _ in range(10**2)],
            "instantiationType": choice(list(ServiceInstantiationType)),
        }
        mock_get_endpoint.reset_mock()
        mock_get_endpoint.return_value = f"{name}/{version}"
        Service.get_by_name_and_version(name, version)
        mock_send_message_json.assert_called_once()
        method, log, _ = mock_send_message_json.mock_calls[0].args
        assert method == "GET"
        assert log == "Get Service by name and version"
        mock_get_endpoint.assert_called_once_with(name, version)


@patch("onapsdk.sdc2.service.Service.send_message_json")
def test_add_deployment_artifact(mock_send_message_json):
    with NamedTemporaryFile() as temp_file:
        temp_file.write(b"Hello world!")
        temp_file.seek(0)

        service = Service(name=str(uuid4()), unique_id=str(uuid4()))
        service.add_deployment_artifact(
            str(uuid4()),
            str(uuid4()),
            str(uuid4()),
            temp_file.name
        )
        mock_send_message_json.assert_called_once()


@patch("onapsdk.sdc2.service.Service.send_message_json")
@patch("onapsdk.sdc2.sdc_resource.ComponentInstance.create_from_api_response")
def test_add_deployment_artifact(mock_create_component_instance, mock_send_message_json):
    service = Service(name=str(uuid4()), unique_id=str(uuid4()))
    mock_send_message_json.return_value = []
    assert len(list(service.component_instances)) == 0
    mock_send_message_json.assert_called_once_with(
        "GET",
        "Get Service component instances",
        f"{service.base_back_url}/sdc2/rest/v1/catalog/services/{service.unique_id}/componentInstances"
    )

    mock_send_message_json.return_value = [{}]
    assert len(list(service.component_instances)) == 1
    mock_create_component_instance.assert_called_once_with({}, service)


@patch("onapsdk.sdc2.service.Service.component_instances", new_callable=PropertyMock)
def test_get_component_by_name(mock_component_instances):
    ComponentInstance = namedtuple("ComponentInstance", ["component_name"])

    service = Service(name="test_component_instances")
    mock_component_instances.return_value = []
    assert service.get_component_by_name("test_name") is None

    mock_component_instances.return_value = [ComponentInstance(component_name="test_name")]
    assert service.get_component_by_name("test_name") is not None
    assert service.get_component_by_name("test_name").component_name == "test_name"

    mock_component_instances.return_value = [ComponentInstance(component_name=f"test_name_{i}") for i in range(10**2)]
    assert service.get_component_by_name("test_name") is None

    random_name = f"test_name_{choice(range(10**2))}"
    assert service.get_component_by_name(random_name) is not None
    assert service.get_component_by_name(random_name).component_name == random_name


@patch("onapsdk.sdc2.service.Service.send_message_json")
@patch("onapsdk.sdc2.service.Service.get_create_payload")
@patch("onapsdk.sdc2.service.Service.create_from_api_response")
def test_create(mock_create_from_api_response, mock_get_create_payload, mock_send_message_json):
    mock_get_create_payload.return_value = "test_payload"
    Service.create(name="test_service")
    mock_send_message_json.assert_called_once_with(
        "POST",
        "Create SERVICE test_service",
        Service.CREATE_ENDPOINT,
        data="test_payload"
    )


@patch("onapsdk.sdc2.service.ServiceCategory.get_by_name")
def test_get_create_payload(mock_resource_category_get_by_name):
    resource_category_mock = MagicMock()
    resource_category_mock.name = "test_category"
    resource_category_mock.unique_id = "category_unique_id"
    mock_resource_category_get_by_name.return_value = resource_category_mock

    create_payload = json.loads(Service.get_create_payload(name="test_service"))
    assert create_payload["componentType"] == "SERVICE"
    assert create_payload["name"] == "test_service"
    assert create_payload["contactId"] == "cs0008"
    assert create_payload["categories"][0]["name"] == "test_category"
    assert create_payload["categories"][0]["uniqueId"] == "category_unique_id"
    assert create_payload["description"] == "ONAP SDK Service"
    assert create_payload["instantiationType"] == "Macro"

    create_payload = json.loads(Service.get_create_payload(name="test_service", description="test description"))
    assert create_payload["componentType"] == "SERVICE"
    assert create_payload["name"] == "test_service"
    assert create_payload["contactId"] == "cs0008"
    assert create_payload["categories"][0]["name"] == "test_category"
    assert create_payload["categories"][0]["uniqueId"] == "category_unique_id"
    assert create_payload["description"] == "test description"
    assert create_payload["instantiationType"] == "Macro"


@patch("onapsdk.sdc2.service.Service.send_message")
def test_add_resource(mock_send_message):
    s = Service(name="test_service", unique_id=str(uuid4()))
    mock_resource = MagicMock()
    mock_resource.name = str(uuid4())
    mock_resource.resource_type.return_value = choice(list(ResoureTypeEnum))
    mock_resource.unique_id = str(uuid4())
    mock_resource.version = str(uuid4())
    mock_resource.icon = str(uuid4())
    s.add_resource(mock_resource)
    mock_send_message.assert_called_once()
    method, log, url = mock_send_message.mock_calls[0].args
    data = json.loads(mock_send_message.mock_calls[0].kwargs["data"])
    assert method == "POST"
    assert log == f"Add resource {mock_resource.name} into service test_service"
    assert url.endswith(f"sdc2/rest/v1/catalog/services/{s.unique_id}/resourceInstance/")
    assert data["name"] == mock_resource.name
    assert data["originType"] == mock_resource.resource_type().value
    assert data["componentUid"] == mock_resource.unique_id
    assert data["componentVersion"] == mock_resource.version
    assert data["icon"] == mock_resource.icon


@patch("onapsdk.sdc2.service.Service.send_message_json")
@patch("onapsdk.sdc2.service.Service.update")
def test_distribute(mock_update, mock_send_message_json):
    s = Service(name="test_service", unique_id=str(uuid4()))
    s.distribute()
    mock_send_message_json.assert_called_once()
    method, log, url = mock_send_message_json.mock_calls[0].args
    assert method == "POST"
    assert log == "Request distribute Service test_service"
    assert url.endswith(f"sdc2/rest/v1/catalog/services/{s.unique_id}/distribution/PROD/activate")

    mock_send_message_json.reset_mock()
    s.distribute(env="TEST")
    mock_send_message_json.assert_called_once()
    method, log, url = mock_send_message_json.mock_calls[0].args
    assert method == "POST"
    assert log == "Request distribute Service test_service"
    assert url.endswith(f"sdc2/rest/v1/catalog/services/{s.unique_id}/distribution/TEST/activate")


@patch("onapsdk.sdc2.service.Service.send_message_json")
def test_distributions(mock_send_message_json):
    s = Service(name="test_service", uuid=str(uuid4()))

    mock_send_message_json.return_value = {}
    assert len(list(s.distributions)) == 0
    method, log, url = mock_send_message_json.mock_calls[0].args
    assert method == "GET"
    assert log == "Request Service test_service distributions"
    assert url.endswith(f"sdc2/rest/v1/catalog/services/{s.uuid}/distribution/")

    mock_send_message_json.return_value = {
        "distributionStatusOfServiceList": [
            {
                "distributionID": str(uuid4()),
                "timestamp": randint(0, maxsize),
                "userId": str(uuid4()),
                "deployementStatus": str(uuid4())
            }
        ]
    }
    assert len(list(s.distributions)) == 1

    mock_send_message_json.return_value = {
        "distributionStatusOfServiceList": [
            {
                "distributionID": str(uuid4()),
                "timestamp": randint(0, maxsize),
                "userId": str(uuid4()),
                "deployementStatus": str(uuid4())
            } for _ in range(10**2)
        ]
    }
    assert len(list(s.distributions)) == 10**2


@patch("onapsdk.sdc2.service.Service.distributions", new_callable=PropertyMock)
def test_latest_distribution(mock_distributions):
    s = Service(name="test_service")

    mock_distributions.return_value = iter([])
    assert s.latest_distribution is None

    mock_distributions.return_value = iter([1])  # Whatever
    assert s.latest_distribution is not None


@patch("onapsdk.sdc2.service.Service.latest_distribution", new_callable=PropertyMock)
def test_service_distributed(mock_latest_distribution):
    s = Service(name="test_service")

    mock_latest_distribution.return_value = None
    assert s.distributed is False

    LatestDistribution = namedtuple("LatestDistribution", "distributed")
    mock_latest_distribution.return_value = LatestDistribution(False)
    assert s.distributed is False

    mock_latest_distribution.return_value = LatestDistribution(True)
    assert s.distributed is True


def test_service_distribution_deployment_status_test():
    sd = ServiceDistribution(
        distribution_id=str(uuid4()),
        timestamp=str(randint(0, maxsize)),
        user_id=str(uuid4()),
        deployment_status=str(uuid4())
    )
    assert sd._deployment_status_test is False
    sd.deployment_status = ServiceDistribution.DISTRIBUTED_DEPLOYMENT_STATUS
    assert sd._deployment_status_test is True


@patch("onapsdk.sdc2.service.ServiceDistribution.distribution_status_list", new_callable=PropertyMock)
def test_service_distribution_distribution_components_test(mock_distribution_status_list):
    mock_distribution_status_list.return_value = []
    sd = ServiceDistribution(
        distribution_id=str(uuid4()),
        timestamp=str(randint(0, maxsize)),
        user_id=str(uuid4()),
        deployment_status=str(uuid4())
    )
    assert sd._distribution_components_test is False

    mock_distribution_status_list.return_value = [
        ServiceDistribution.DistributionStatus(
            component_id=component_id,
            timestamp=str(randint(0, maxsize)),
            status=str(uuid4()),
            url=str(uuid4()),
            error_reason=str(uuid4())
        ) for component_id in settings.SDC_SERVICE_DISTRIBUTION_COMPONENTS
    ]
    assert sd._distribution_components_test is True

    mock_distribution_status_list.return_value = [
        ServiceDistribution.DistributionStatus(
            component_id=component_id,
            timestamp=str(randint(0, maxsize)),
            status=str(uuid4()),
            url=str(uuid4()),
            error_reason=str(uuid4())
        ) for component_id in settings.SDC_SERVICE_DISTRIBUTION_COMPONENTS + ["additional-test-component"]
    ]
    assert sd._distribution_components_test is True


@patch("onapsdk.sdc2.service.ServiceDistribution.distribution_status_list", new_callable=PropertyMock)
def test_service_distribution_no_distribution_errors_test(mock_distribution_status_list):
    mock_distribution_status_list.return_value = []
    sd = ServiceDistribution(
        distribution_id=str(uuid4()),
        timestamp=str(randint(0, maxsize)),
        user_id=str(uuid4()),
        deployment_status=str(uuid4())
    )
    assert sd._no_distribution_errors_test is True

    DistributionStatus = namedtuple("DistributionStatus", ["failed"])
    mock_distribution_status_list.return_value = [
        DistributionStatus(failed=True)
    ]
    assert sd._no_distribution_errors_test is False

    mock_distribution_status_list.return_value = [
        DistributionStatus(failed=True),
        DistributionStatus(failed=False)
    ]
    assert sd._no_distribution_errors_test is False

    mock_distribution_status_list.return_value = [
        DistributionStatus(failed=False),
        DistributionStatus(failed=False)
    ]
    assert sd._no_distribution_errors_test is True


@patch("onapsdk.sdc2.service.ServiceDistribution.send_message_json")
def test_service_distribution_distributon_status_list(mock_send_message_json):
    mock_send_message_json.return_value = {
        "distributionStatusList": []
    }
    sd = ServiceDistribution(
        distribution_id=str(uuid4()),
        timestamp=str(randint(0, maxsize)),
        user_id=str(uuid4()),
        deployment_status=str(uuid4())
    )
    assert sd.distribution_status_list == []

    distribution_status_data = {
        "omfComponentID": str(uuid4()),
        "timestamp": str(randint(0, maxsize)),
        "status": str(uuid4()),
        "url": str(uuid4()),
        "errorReason": str(uuid4())
    }
    mock_send_message_json.return_value = {
        "distributionStatusList": [distribution_status_data]
    }
    assert len(sd.distribution_status_list) == 1
    assert sd.distribution_status_list[0].component_id == distribution_status_data["omfComponentID"]
    assert sd.distribution_status_list[0].timestamp == distribution_status_data["timestamp"]
    assert sd.distribution_status_list[0].status == distribution_status_data["status"]
    assert sd.distribution_status_list[0].url == distribution_status_data["url"]
    assert sd.distribution_status_list[0].error_reason == distribution_status_data["errorReason"]


@patch("onapsdk.sdc2.service.ServiceDistribution.send_message_json")
def test_service_distribution_distributon_status_list_with_errors(mock_send_message_json):
    mock_send_message_json.return_value = {
        "distributionStatusList": []
    }
    sd = ServiceDistribution(
        distribution_id=str(uuid4()),
        timestamp=str(randint(0, maxsize)),
        user_id=str(uuid4()),
        deployment_status=str(uuid4())
    )
    assert sd.distribution_status_list == []

    distribution_status_data_null_error_reason = {
        "omfComponentID": str(uuid4()),
        "timestamp": str(randint(0, maxsize)),
        "status": str(uuid4()),
        "url": str(uuid4()),
        "errorReason": "null"
    }
    mock_send_message_json.return_value = {
        "distributionStatusList": [distribution_status_data_null_error_reason]
    }
    sd._distribution_status_list = None
    assert len(sd.distribution_status_list) == 1
    assert not sd.distribution_status_list[0].failed

    distribution_status_data_artifact_not_used_error_reason = {
        "omfComponentID": str(uuid4()),
        "timestamp": str(randint(0, maxsize)),
        "status": str(uuid4()),
        "url": str(uuid4()),
        "errorReason": "The artifact has not been used by the modules defined in the resource"
    }
    mock_send_message_json.return_value = {
        "distributionStatusList": [distribution_status_data_artifact_not_used_error_reason]
    }
    sd._distribution_status_list = None
    assert len(sd.distribution_status_list) == 1
    assert not sd.distribution_status_list[0].failed

    distribution_status_data_already_deployed_status = {
        "omfComponentID": str(uuid4()),
        "timestamp": str(randint(0, maxsize)),
        "status": "ALREADY_DEPLOYED",
        "url": str(uuid4()),
        "errorReason": str(uuid4())
    }
    mock_send_message_json.return_value = {
        "distributionStatusList": [distribution_status_data_already_deployed_status]
    }
    sd._distribution_status_list = None
    assert len(sd.distribution_status_list) == 1
    assert not sd.distribution_status_list[0].failed

    distribution_status_data_any_error_reason = {
        "omfComponentID": str(uuid4()),
        "timestamp": str(randint(0, maxsize)),
        "status": str(uuid4()),
        "url": str(uuid4()),
        "errorReason": str(uuid4())
    }
    mock_send_message_json.return_value = {
        "distributionStatusList": [distribution_status_data_any_error_reason]
    }
    sd._distribution_status_list = None
    assert len(sd.distribution_status_list) == 1
    assert sd.distribution_status_list[0].failed
