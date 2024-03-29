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
from unittest import mock

import pytest

from onapsdk.aai.business import PnfInstance, ServiceInstance, pnf
from onapsdk.exceptions import ResourceNotFound, APIError, ConnectionFailed
from onapsdk.so.deletion import PnfDeletionRequest

PNF_INSTANCE = {
    "pnf-name": "blablabla",
    "pnf-id": "546b282b-2ff7-41a4-9329-55c9a2888477",
    "equip-type": "pnf",
    "equip-vendor": "PNF",
    "equip-model": "Simulated Device",
    "orchestration-status": "Active",
    "ipaddress-v4-oam": "172.30.1.6",
    "sw-version": "2.3.5",
    "in-maint":False,
    "serial-number": "123",
    "ipaddress-v6-oam": "0:0:0:0:0:ffff:a0a:011",
    "resource-version": "1610142659380",
    "nf-role": "sdn controller",
    "model-customization-id": "137ce8e8-bee9-465f-b7e1-0c006f10b443",
    "model-invariant-id": "2ca7ea68-cf61-449c-a733-8122bcac1f9a",
    "model-version-id": "da467f24-a26d-4620-b185-e1afa1d365ac",
    "relationship-list": {
        "relationship":[
            {
                "related-to":"service-instance",
                "relationship-label":"org.onap.relationships.inventory.ComposedOf",
                "related-link":"/aai/v27/business/customers/customer/test/service-subscriptions/service-subscription/test/service-instances/service-instance/4c3ab996-afdb-4956-9c4d-038b4eed3db1",
                "relationship-data":[
                    {
                        "relationship-key":"customer.global-customer-id",
                        "relationship-value":"test"
                    },
                    {
                        "relationship-key":"service-subscription.service-type",
                        "relationship-value":"test"
                    },
                    {
                        "relationship-key":"service-instance.service-instance-id",
                        "relationship-value":"4c3ab996-afdb-4956-9c4d-038b4eed3db1"
                    }
                ],
                "related-to-property":[
                    {
                        "property-key":"service-instance.service-instance-name",
                        "property-value":"blablabla"
                    }
                ]
            }
        ]
    }
}


COUNT = {
    "results":[
        {
            "pnf":12
        }
    ]
}


def test_create_pnf_instance_from_api_response():
    service_instance = mock.MagicMock()
    pnf_instance = PnfInstance.create_from_api_response(
        PNF_INSTANCE,
        service_instance
    )
    assert pnf_instance.pnf_name == "blablabla"
    assert pnf_instance.pnf_id == "546b282b-2ff7-41a4-9329-55c9a2888477"
    assert pnf_instance.equip_type == "pnf"
    assert pnf_instance.equip_vendor == "PNF"
    assert pnf_instance.equip_model == "Simulated Device"
    assert pnf_instance.orchestration_status == "Active"
    assert pnf_instance.ipaddress_v4_oam == "172.30.1.6"
    assert pnf_instance.sw_version == "2.3.5"
    assert pnf_instance.in_maint == False
    assert pnf_instance.serial_number == "123"
    assert pnf_instance.ipaddress_v6_oam == "0:0:0:0:0:ffff:a0a:011"
    assert pnf_instance.resource_version == "1610142659380"
    assert pnf_instance.nf_role == "sdn controller"
    assert pnf_instance.model_customization_id == "137ce8e8-bee9-465f-b7e1-0c006f10b443"
    assert pnf_instance.model_invariant_id == "2ca7ea68-cf61-449c-a733-8122bcac1f9a"
    assert pnf_instance.model_version_id == "da467f24-a26d-4620-b185-e1afa1d365ac"

    assert pnf_instance.url.endswith(pnf_instance.pnf_name)


@mock.patch.object(PnfDeletionRequest, "send_request")
def test_delete_pnf_instance(mock_pnf_deletion_request):
    service_instance = ServiceInstance(None,
                                       instance_id="test_service_instance_id")
    pnf_instance = PnfInstance(service_instance,
                               pnf_id="test_pnf_id",
                               pnf_name="test_pnf_name",
                               serial_number="test_serial_number",
                               in_maint=False)

    assert pnf_instance.service_instance == service_instance
    assert pnf_instance.pnf_id == "test_pnf_id"
    assert pnf_instance.in_maint is False
    assert pnf_instance.serial_number == "test_serial_number"
    assert pnf_instance._pnf is None
    assert pnf_instance.url == (f"{pnf_instance.base_url}{pnf_instance.api_version}/network/"
                                f"pnfs/pnf/{pnf_instance.pnf_name}")
    pnf_instance.delete()
    mock_pnf_deletion_request.assert_called_once_with(pnf_instance, True)



def test_pnf_instance_pnf():
    service_instance = mock.MagicMock()
    pnf_instance = PnfInstance.create_from_api_response(
        PNF_INSTANCE,
        service_instance
    )

    assert pnf_instance._pnf is None
    service_instance.sdc_service.pnfs = []
    with pytest.raises(ResourceNotFound) as exc:
        pnf_instance.pnf
    assert exc.type == ResourceNotFound
    assert pnf_instance._pnf is None

    pnf = mock.MagicMock()
    pnf.model_version_id = "da467f24-a26d-4620-b185-e1afa1d365ac"
    service_instance.sdc_service.pnfs = [pnf]
    assert pnf == pnf_instance.pnf
    assert pnf_instance._pnf is not None
    assert pnf_instance.pnf == pnf_instance._pnf

@mock.patch.object(PnfInstance, "send_message_json")
def test_pnf_count(mock_send_message_json):
    mock_send_message_json.return_value = COUNT
    assert PnfInstance.count() == 12

@mock.patch.object(PnfInstance,"send_message")
def test_delete_from_aai_success(mock_send_message):
    
    delete_response = mock.MagicMock()
    delete_response.status_code = 204 #success case

    mock_send_message.return_value= delete_response
    pnf_instance = PnfInstance(service_instance=None,
                               pnf_id="test_pnf_id",
                               pnf_name="test_pnf_name",
                               serial_number="test_serial_number",
                               in_maint=False)
    try:
        pnf_instance.delete_from_aai()
    except APIError:
        assert False  # Exception is not expected

@mock.patch.object(PnfInstance,"send_message")
def test_delete_from_aai_failure(mock_send_message):
    
    mock_send_message.side_effect = ConnectionFailed('Can not connect to AAI')

    pnf_instance = PnfInstance(service_instance=None,
                               pnf_id="test_pnf_id",
                               pnf_name="test_pnf_name",
                               serial_number="test_serial_number",
                               in_maint=False)
    with pytest.raises(ConnectionFailed):
        pnf_instance.delete_from_aai()

@mock.patch.object(PnfInstance,"send_message")
def test_put_in_aai_success(mock_send_message):
    put_response = mock.MagicMock()
    put_response.status_code = 201 #success case

    mock_send_message.return_value = put_response
    pnf_instance = PnfInstance(service_instance=None,
                               pnf_id="test_pnf_id",
                               pnf_name="test_pnf_name",
                               serial_number="test_serial_number",
                               in_maint=False)
    try:
        pnf_instance.put_in_aai()
    except APIError:
        assert False  # Exception is not expected

@mock.patch.object(PnfInstance,"send_message")
def test_put_in_aai_success_with_none_attribute(mock_send_message):
    put_response = mock.MagicMock()
    put_response.status_code = 201 #success case

    mock_send_message.return_value = put_response
    pnf_instance = PnfInstance(service_instance=None,
                               pnf_id="test_pnf_id",
                               pnf_name="test_pnf_name",
                               serial_number=None,
                               in_maint=False)
    try:
        pnf_instance.put_in_aai()
    except APIError:
        assert False  # Exception is not expected

@mock.patch.object(PnfInstance,"send_message")
def test_put_in_aai_failure(mock_send_message):
    mock_send_message.side_effect = ConnectionFailed('Can not connect to AAI')
    pnf_instance = PnfInstance(service_instance=None,
                               pnf_id="test_pnf_id",
                               pnf_name="test_pnf_name",
                               serial_number="test_serial_number",
                               in_maint=False)
    with pytest.raises(ConnectionFailed):
        pnf_instance.put_in_aai()