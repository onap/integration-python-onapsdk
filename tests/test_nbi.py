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
from collections import namedtuple
from unittest import mock

import pytest
from onapsdk.aai.business import Customer
from onapsdk.exceptions import RequestError
from onapsdk.nbi import Nbi, Service, ServiceOrder, ServiceSpecification, Resource


SERVICE_SPECIFICATION = {
    "id": "a80c901c-6593-491f-9465-877e5acffb46",
    "name": "testService1",
    "invariantUUID": "217deaa7-dfc3-41d8-aa53-bb009029c09f",
    "category": "Network Service",
    "distributionStatus": "DISTRIBUTED",
    "version": "1.0",
    "lifecycleStatus": "CERTIFIED",
    "relatedParty": {
        "id": "cs0008",
        "role": "lastUpdater"
    }
}

SERVICE_SPECIFICATIONS = [
    {
        "id": "a80c901c-6593-491f-9465-877e5acffb46",
        "name": "testService1",
        "invariantUUID": "217deaa7-dfc3-41d8-aa53-bb009029c09f",
        "category": "Network Service",
        "distributionStatus": "DISTRIBUTED",
        "version": "1.0",
        "lifecycleStatus": "CERTIFIED",
        "relatedParty": {
            "id": "cs0008",
            "role": "lastUpdater"
        }
    },
    {
        "id": "b1cda0ab-d968-41ef-9051-d26b33b120be",
        "name": "testService2",
        "invariantUUID": "906c3185-9656-4639-8f4d-d51d9ee0695d",
        "category": "Network Service",
        "distributionStatus": "DISTRIBUTED",
        "version": "1.0",
        "lifecycleStatus": "CERTIFIED",
        "relatedParty": {
            "id": "cs0008"
            , "role": "lastUpdater"
        }
    }
]

SERVICES = [
    {
        "id": "5c855390-7c39-4fe4-b164-2029b09de57c",
        "name": "test6",
        "serviceSpecification": {
            "name": "testService9",
            "id": "125727ad-8660-423e-b4a1-99cd4a749f45"
        },
        "relatedParty": {
            "role": "ONAPcustomer",
            "id": "generic"
        },
        "href": "service/5c855390-7c39-4fe4-b164-2029b09de57c"
    },
    {
        "id": "f948be83-c3e8-4515-a27d-2983eba63911",
        "name": "test4",
        "serviceSpecification": {
            "name": "testService8",
            "id": "0960aedb-3ad8-49e1-ade5-a59414f6fda4"
        },
        "relatedParty": {
            "role": "ONAPcustomer",
            "id": "generic"
        },
        "href": "service/f948be83-c3e8-4515-a27d-2983eba63911"
    },
    {
        "id": "5066eabd-846c-4ed9-886b-69892a12968d",
        "name": "test5",
        "serviceSpecification": {
            "name": "testService8",
            "id": "0960aedb-3ad8-49e1-ade5-a59414f6fda4"
        },
        "relatedParty": {
            "role": "ONAPcustomer",
            "id": "generic"
        },
        "href": "service/5066eabd-846c-4ed9-886b-69892a12968d"
    }
]

SERVICES_CUSTOMER = [
    {
        "id": "6a855390-7c39-4fe4-b164-2029b09de57d",
        "name": "test7",
        "serviceSpecification": {
            "name": "testService9",
            "id": "125727ad-8660-423e-b4a1-99cd4a749f45"
        },
        "relatedParty": {
            "role": "ONAPcustomer",
            "id": "test_customer"
        },
        "href": "service/6a855390-7c39-4fe4-b164-2029b09de57d"
    }
]

SERVICE_ORDERS = [
    {
        "id": "5e9d6d98ae76af6b04e4df9a",
        "href": "serviceOrder/5e9d6d98ae76af6b04e4df9a",
        "externalId": "",
        "priority": "1",
        "description": "testService order for generic customer via Python ONAP SDK",
        "category": "Consumer",
        "state": "rejected",
        "orderDate": "2020-04-20T09:38:32.286Z",
        "completionDateTime": "2020-04-20T09:38:47.866Z",
        "expectedCompletionDate": None,
        "requestedStartDate": "2020-04-20T09:47:49.919Z",
        "requestedCompletionDate": "2020-04-20T09:47:49.919Z",
        "startDate": None,
        "@baseType": None,
        "@type": None,
        "@schemaLocation": None,
        "relatedParty": [
            {
                "id": "generic",
                "href": None,
                "role": "ONAPcustomer",
                "name": "generic",
                "@referredType": None
            }
        ],
        "orderRelationship": None,
        "orderItem": [
            {
                "orderMessage": [],
                "id": "1",
                "action": "add",
                "state": "rejected",
                "percentProgress": "0",
                "@type": None,
                "@schemaLocation": None,
                "@baseType": None,
                "orderItemRelationship": [],
                "service": {
                    "id": None,
                    "serviceType": None,
                    "href": None,
                    "name": "08d960ae-c2e1-4d5c-baf0-6420659ea68a",
                    "serviceState": "active",
                    "@type": None,
                    "@schemaLocation": None,
                    "serviceCharacteristic": None,
                    "serviceRelationship": None,
                    "relatedParty": None,
                    "serviceSpecification": {
                        "id": "a80c901c-6593-491f-9465-877e5acffb46",
                        "href": None,
                        "name": None,
                        "version": None,
                        "targetServiceSchema": None,
                        "@type": None,
                        "@schemaLocation": None,
                        "@baseType": None
                    }
                },
                "orderItemMessage": []
            }
        ],
        "orderMessage": [
            {
                "code": "501",
                "field": None,
                "messageInformation": "Problem with AAI API",
                "severity": "error",
                "correctionRequired": True
            },
            {
                "code": "503",
                "field": None,
                "messageInformation": "tenantId not found in AAI",
                "severity": "error",
                "correctionRequired": True
            }
        ]
    }
]

SERVICE_ORDERS_NO_RELATED_PARTY = [
    {
        "id": "5e9d6d98ae76af6b04e4df9a",
        "href": "serviceOrder/5e9d6d98ae76af6b04e4df9a",
        "externalId": "",
        "priority": "1",
        "description": "testService order for generic customer via Python ONAP SDK",
        "category": "Consumer",
        "state": "rejected",
        "orderDate": "2020-04-20T09:38:32.286Z",
        "completionDateTime": "2020-04-20T09:38:47.866Z",
        "expectedCompletionDate": None,
        "requestedStartDate": "2020-04-20T09:47:49.919Z",
        "requestedCompletionDate": "2020-04-20T09:47:49.919Z",
        "startDate": None,
        "@baseType": None,
        "@type": None,
        "@schemaLocation": None,
        "relatedParty": None,
        "orderRelationship": None,
        "orderItem": [
            {
                "orderMessage": [],
                "id": "1",
                "action": "add",
                "state": "rejected",
                "percentProgress": "0",
                "@type": None,
                "@schemaLocation": None,
                "@baseType": None,
                "orderItemRelationship": [],
                "service": {
                    "id": None,
                    "serviceType": None,
                    "href": None,
                    "name": "08d960ae-c2e1-4d5c-baf0-6420659ea68a",
                    "serviceState": "active",
                    "@type": None,
                    "@schemaLocation": None,
                    "serviceCharacteristic": None,
                    "serviceRelationship": None,
                    "relatedParty": None,
                    "serviceSpecification": {
                        "id": "a80c901c-6593-491f-9465-877e5acffb46",
                        "href": None,
                        "name": None,
                        "version": None,
                        "targetServiceSchema": None,
                        "@type": None,
                        "@schemaLocation": None,
                        "@baseType": None
                    }
                },
                "orderItemMessage": []
            }
        ],
        "orderMessage": [
            {
                "code": "501",
                "field": None,
                "messageInformation": "Problem with AAI API",
                "severity": "error",
                "correctionRequired": True
            },
            {
                "code": "503",
                "field": None,
                "messageInformation": "tenantId not found in AAI",
                "severity": "error",
                "correctionRequired": True
            }
        ]
    }
]

SERVICE_ORDER_STATE_COMPLETED = {
    'state': 'completed'
}

SERVICE_ORDER_STATE_FAILED = {
    'state': 'failed'
}

SERVICE_ORDER_STATE_IN_PROGRESS = {
    'state': 'inProgress'
}

SERVICE_ORDER_STATE_REJECTED = {
    'state': 'rejected'
}

SERVICE_ORDER_STATE_UNKNOWN = {
    'state': 'lalala'
}

RESOURCES = [
    {
        "id": "0efe5f46-7233-495d-826e-9d177b1866b4",
        "href": "/nbi/api/v4/resource/0efe5f46-7233-495d-826e-9d177b1866b4",
        "@type": "test_pnf_rollback/null",
        "@baseType": "LogicalResource",
        "value": "vnf-name-test-19-12",
        "lifeCyleState": "Active",
        "resourceSpecification": {
            "id": "22e67c4a-f652-43d0-8975-63006c442718"
        },
        "resourceCharacteristics": [
            {
                "name": "prov-status",
                "value": "NVTPROV"
            },
            {
                "name": "in-maint",
                "value": "false"
            }
        ],
        "relatedParty": [
            {
                "id": "pnf_macro_customer",
                "role": "ONAPcustomer"
            }
        ],
        "note": [
            {
                "text": "vnf-name-test-19-12 is available on k8sregionfour"
            }
        ],
        "place": {
            "id": "k8sregionfour",
            "name": "gnb-cucp-sim-76d58f7bd7-sq8g5",
            "role": "e728fdf9dc5914e2595d6cb9444da113f6042e29d52058c1424434879b600794"
        }
    },
    {
        "id": "cf7b9996-1ae5-49b2-baf6-797599f5d89b",
        "href": "/nbi/api/v4/resource/cf7b9996-1ae5-49b2-baf6-797599f5d89b",
        "@type": "Demo service/null",
        "@baseType": "LogicalResource",
        "value": "test_abhimanyu_04",
        "lifeCyleState": "Active",
        "resourceSpecification": {
            "id": "836398af-de68-404f-bf39-5d3cacfe92ae"
        },
        "resourceCharacteristics": [
            {
                "name": "prov-status",
                "value": "NVTPROV"
            },
            {
                "name": "in-maint",
                "value": "false"
            }
        ],
        "relatedParty": [
            {
                "id": "pnf_macro_customer",
                "role": "ONAPcustomer"
            }
        ],
        "note": [
            {
                "text": "test_abhimanyu_04 is available on "
            }
        ]
    }
]

RESOURCE = {
    "id": "0efe5f46-7233-495d-826e-9d177b1866b4",
    "href": "/nbi/api/v4/resource/0efe5f46-7233-495d-826e-9d177b1866b4",
    "@type": "test_pnf_rollback/null",
    "@baseType": "LogicalResource",
    "value": "vnf-name-test-19-12",
    "lifeCyleState": "Active",
    "resourceSpecification": {
        "id": "22e67c4a-f652-43d0-8975-63006c442718"
    },
    "resourceCharacteristics": [
        {
            "name": "prov-status",
            "value": "NVTPROV"
        },
        {
            "name": "in-maint",
            "value": "false"
        }
    ],
    "relatedParty": [
        {
            "id": "pnf_macro_customer",
            "role": "ONAPcustomer"
        }
    ],
    "note": [
        {
            "text": "vnf-name-test-19-12 is available on k8sregionfour"
        }
    ],
    "place": {
        "id": "k8sregionfour",
        "name": "gnb-cucp-sim-76d58f7bd7-sq8g5",
        "role": "e728fdf9dc5914e2595d6cb9444da113f6042e29d52058c1424434879b600794"
    }
}

@mock.patch.object(Nbi, "send_message")
def test_nbi(mock_send_message):
    assert Nbi.base_url == "https://nbi.api.simpledemo.onap.org:30274"
    assert Nbi.api_version == "/nbi/api/v4"

    mock_send_message.side_effect = RequestError
    assert Nbi.is_status_ok() == False
    mock_send_message.side_effect = None
    assert Nbi.is_status_ok() == True


@mock.patch.object(ServiceSpecification, "send_message_json")
def test_service_specification_get_all(mock_service_specification_send_message):
    mock_service_specification_send_message.return_value = []
    assert len(list(ServiceSpecification.get_all())) == 0

    mock_service_specification_send_message.return_value = SERVICE_SPECIFICATIONS
    service_specifications = list(ServiceSpecification.get_all())
    assert len(service_specifications) == 2

    assert service_specifications[0].unique_id == "a80c901c-6593-491f-9465-877e5acffb46"
    assert service_specifications[0].name == "testService1"
    assert service_specifications[0].invariant_uuid == "217deaa7-dfc3-41d8-aa53-bb009029c09f"
    assert service_specifications[0].category == "Network Service"
    assert service_specifications[0].distribution_status == "DISTRIBUTED"
    assert service_specifications[0].version == "1.0"
    assert service_specifications[0].lifecycle_status == "CERTIFIED"

    assert service_specifications[1].unique_id == "b1cda0ab-d968-41ef-9051-d26b33b120be"
    assert service_specifications[1].name == "testService2"
    assert service_specifications[1].invariant_uuid == "906c3185-9656-4639-8f4d-d51d9ee0695d"
    assert service_specifications[1].category == "Network Service"
    assert service_specifications[1].distribution_status == "DISTRIBUTED"
    assert service_specifications[1].version == "1.0"
    assert service_specifications[1].lifecycle_status == "CERTIFIED"


@mock.patch.object(ServiceSpecification, "send_message_json")
def test_service_specification_get_by_id(mock_service_specification_send_message):
    mock_service_specification_send_message.return_value = SERVICE_SPECIFICATION
    service_specification = ServiceSpecification.get_by_id("test")
    assert service_specification.unique_id == "a80c901c-6593-491f-9465-877e5acffb46"
    assert service_specification.name == "testService1"
    assert service_specification.invariant_uuid == "217deaa7-dfc3-41d8-aa53-bb009029c09f"
    assert service_specification.category == "Network Service"
    assert service_specification.distribution_status == "DISTRIBUTED"
    assert service_specification.version == "1.0"
    assert service_specification.lifecycle_status == "CERTIFIED"


@mock.patch.object(ServiceSpecification, "send_message_json")
def test_specification_input_schema(mock_service_specification_schema_send_message):
    mock_service_specification_schema_send_message.return_value = SERVICE_SPECIFICATION
    service_specification_schema = ServiceSpecification.specification_input_schema("test")
    assert service_specification_schema.unique_id == "a80c901c-6593-491f-9465-877e5acffb46"
    assert service_specification_schema.name == "testService1"
    assert service_specification_schema.invariant_uuid == "217deaa7-dfc3-41d8-aa53-bb009029c09f"
    assert service_specification_schema.category == "Network Service"
    assert service_specification_schema.distribution_status == "DISTRIBUTED"
    assert service_specification_schema.version == "1.0"
    assert service_specification_schema.lifecycle_status == "CERTIFIED"


@mock.patch.object(Service, "send_message_json")
@mock.patch.object(Customer, "get_by_global_customer_id")
@mock.patch.object(ServiceSpecification, "get_by_id")
def test_service_get_all(mock_service_specification_get_by_id,
                         mock_customer_get_by_id,
                         mock_service_send_message):
    mock_service_send_message.return_value = []
    assert len(list(Service.get_all())) == 0
    mock_service_send_message.return_value = SERVICES
    services_list = list(Service.get_all())
    assert len(services_list) == 3

    service = services_list[0]

    assert service.name == "test6"
    assert service.service_id == "5c855390-7c39-4fe4-b164-2029b09de57c"
    assert service.service_specification_name == "testService9"
    assert service._service_specification_id == "125727ad-8660-423e-b4a1-99cd4a749f45"
    assert service.customer_id == "generic"
    assert service.customer_role == "ONAPcustomer"
    assert service.href == "service/5c855390-7c39-4fe4-b164-2029b09de57c"

    assert service.customer is not None
    mock_customer_get_by_id.assert_called_once_with(service.customer_id)

    service.customer_id = None
    assert service.customer is None

    assert service.service_specification is not None
    mock_service_specification_get_by_id.assert_called_once_with(service._service_specification_id)

    service._service_specification_id = None
    assert service.service_specification is None

    mock_service_send_message.return_value = SERVICES_CUSTOMER
    services_list = list(Service.get_all(customer_id="test_customer"))
    assert len(services_list) == 1

    service = services_list[0]

    assert service.name == "test7"
    assert service.service_id == "6a855390-7c39-4fe4-b164-2029b09de57d"
    assert service.service_specification_name == "testService9"
    assert service._service_specification_id == "125727ad-8660-423e-b4a1-99cd4a749f45"
    assert service.customer_id == "test_customer"
    assert service.customer_role == "ONAPcustomer"
    assert service.href == "service/6a855390-7c39-4fe4-b164-2029b09de57d"


@mock.patch.object(ServiceOrder, "send_message_json")
def test_service_order(mock_service_order_send_message):
    mock_service_order_send_message.return_value = []
    assert len(list(ServiceOrder.get_all())) == 0

    mock_service_order_send_message.return_value = SERVICE_ORDERS
    service_orders = list(ServiceOrder.get_all())
    assert len(service_orders) == 1
    service_order = service_orders[0]
    assert service_order.unique_id == "5e9d6d98ae76af6b04e4df9a"
    assert service_order.href == "serviceOrder/5e9d6d98ae76af6b04e4df9a"
    assert service_order.priority == "1"
    assert service_order.category == "Consumer"
    assert service_order.description == "testService order for generic customer via Python ONAP SDK"
    assert service_order.external_id == ""
    assert service_order._customer == None
    assert service_order._customer_id == "generic"
    assert service_order._service_specification == None
    assert service_order._service_specification_id == "a80c901c-6593-491f-9465-877e5acffb46"
    assert service_order.service_instance_name == "08d960ae-c2e1-4d5c-baf0-6420659ea68a"
    assert service_order.state == "rejected"


@mock.patch.object(ServiceOrder, "send_message_json")
def test_service_order_status(mock_service_order_send_message):
    mock_service_order_send_message.return_value = SERVICE_ORDERS
    service_order = next(ServiceOrder.get_all())

    mock_service_order_send_message.return_value = SERVICE_ORDER_STATE_COMPLETED
    assert service_order.status == service_order.StatusEnum.COMPLETED
    assert service_order.completed
    assert service_order.finished
    assert not service_order.rejected
    assert not service_order.failed

    mock_service_order_send_message.return_value = SERVICE_ORDER_STATE_FAILED
    assert service_order.status == service_order.StatusEnum.FAILED
    assert not service_order.completed
    assert service_order.finished
    assert not service_order.rejected
    assert service_order.failed

    mock_service_order_send_message.return_value = SERVICE_ORDER_STATE_IN_PROGRESS
    assert service_order.status == service_order.StatusEnum.IN_PROGRESS
    assert not service_order.completed
    assert not service_order.finished
    assert not service_order.rejected
    assert not service_order.failed

    mock_service_order_send_message.return_value = SERVICE_ORDER_STATE_REJECTED
    assert service_order.status == service_order.StatusEnum.REJECTED
    assert not service_order.completed
    assert service_order.finished
    assert service_order.rejected
    assert not service_order.failed

    mock_service_order_send_message.return_value = SERVICE_ORDER_STATE_UNKNOWN
    assert service_order.status == service_order.StatusEnum.UNKNOWN
    assert not service_order.completed
    assert service_order.finished
    assert not service_order.rejected
    assert not service_order.failed

    mock_service_order_send_message.return_value = {}
    assert service_order.status == service_order.StatusEnum.UNKNOWN
    assert not service_order.completed
    assert service_order.finished
    assert not service_order.rejected
    assert not service_order.failed


@mock.patch.object(ServiceOrder, "send_message_json")
def test_service_order_no_related_party(mock_service_order_send_message):
    mock_service_order_send_message.return_value = []
    assert len(list(ServiceOrder.get_all())) == 0

    mock_service_order_send_message.return_value = SERVICE_ORDERS_NO_RELATED_PARTY
    service_orders = list(ServiceOrder.get_all())
    assert len(service_orders) == 1
    service_order = service_orders[0]
    assert service_order.unique_id == "5e9d6d98ae76af6b04e4df9a"
    assert service_order.href == "serviceOrder/5e9d6d98ae76af6b04e4df9a"
    assert service_order.priority == "1"
    assert service_order.category == "Consumer"
    assert service_order.description == "testService order for generic customer via Python ONAP SDK"
    assert service_order.external_id == ""
    assert service_order._customer == None
    assert service_order._customer_id == None
    assert service_order._service_specification == None
    assert service_order._service_specification_id == "a80c901c-6593-491f-9465-877e5acffb46"
    assert service_order.service_instance_name == "08d960ae-c2e1-4d5c-baf0-6420659ea68a"
    assert service_order.state == "rejected"


@mock.patch.object(Customer, "get_by_global_customer_id")
def test_service_order_customer(mock_customer_get_by_id):
    service_order = ServiceOrder("test_unique_id",
                                 "test_href",
                                 "test_priority",
                                 "test_description",
                                 "test_category",
                                 "test_external_id",
                                 "test_service_instance_name")
    assert service_order.customer is None
    assert service_order._customer is None
    service_order._customer_id = "test_customer_id"
    assert service_order.customer is not None
    mock_customer_get_by_id.assert_called_once_with("test_customer_id")
    assert service_order._customer is not None


@mock.patch.object(ServiceSpecification, "get_by_id")
def test_service_order_service_specification(mock_service_spec_get_by_id):
    service_order = ServiceOrder("test_unique_id",
                                 "test_href",
                                 "test_priority",
                                 "test_description",
                                 "test_category",
                                 "test_external_id",
                                 "test_service_instance_name")
    assert service_order.service_specification is None
    assert service_order._service_specification_id is None
    service_order._service_specification_id = "test_service_spec_id"
    assert service_order.service_specification is not None
    mock_service_spec_get_by_id.assert_called_once_with("test_service_spec_id")
    assert service_order._service_specification is not None


@mock.patch.object(ServiceOrder, "send_message_json")
def test_service_order_create(mock_service_order_send_message):
    ServiceOrder.create(customer=mock.MagicMock(),
                        service_specification=mock.MagicMock())
    mock_service_order_send_message.assert_called_once()
    method, _, url = mock_service_order_send_message.call_args[0]
    assert method == "POST"
    assert url == f"{ServiceOrder.base_url}{ServiceOrder.api_version}/serviceOrder"


def test_service_order_wait_for_finish():
    with mock.patch.object(ServiceOrder, "finished", new_callable=mock.PropertyMock) as mock_finished:
        with mock.patch.object(ServiceOrder, "completed", new_callable=mock.PropertyMock) as mock_completed:
            service_order = ServiceOrder(
                unique_id="test",
                href="test",
                priority="test",
                description="test",
                category="test",
                external_id="test",
                service_instance_name="test",
            )
            service_order.WAIT_FOR_SLEEP_TIME = 0
            mock_finished.side_effect = [False, False, True]
            mock_completed.return_value = True
            rv = namedtuple("Value", ["return_value"])
            service_order._wait_for_finish(rv)
            assert rv.return_value

@mock.patch.object(Resource, "send_message_json")
def test_query_resource_get_all(mock_query_resource_get_all):
    mock_query_resource_get_all.return_value = RESOURCES
    resources = Resource.get_all_resources()
    resource = next(resources)
    assert type(resource) == Resource
    assert resource.unique_id is not None
    mock_query_resource_get_all.return_value = []
    resources = Resource.get_all_resources()
    with pytest.raises(StopIteration):
        next(resources)
    mock_query_resource_get_all.return_value = []
    resources = Resource.get_all_resources()
    resource = next(resources, None)
    assert resource is None

@mock.patch.object(Resource, "send_message_json")
def test_query_resource_get_specific_resource(mock_specific_resource):
    resource_id = "0efe5f46-7233-495d-826e-9d177b1866b4"
    mock_specific_resource.return_value = RESOURCE
    resource = Resource.get_specific_resource(resource_id)
    assert type(resource) == Resource
    assert resource.unique_id == RESOURCE.get("id")
    assert resource.href == RESOURCE.get("href")