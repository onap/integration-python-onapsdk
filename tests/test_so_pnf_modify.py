from unittest import mock

from onapsdk.so.modification import PnfModificationRequest
from onapsdk.aai.business.owning_entity import OwningEntity


@mock.patch.object(PnfModificationRequest, "send_message_json")
@mock.patch.object(OwningEntity, "get_by_owning_entity_id")
def test_pnf_modification(mock_owning_entity_get, mock_pnf_modification_send_message):
    aai_service_instance_mock = mock.MagicMock()
    aai_service_instance_mock.instance_id = "test_instance_id"

    pnf_object_mock = mock.MagicMock()
    pnf_object_mock.pnf_id = "test_pnf_id"

    relation_1 = mock.MagicMock()
    relation_1.related_to = "owning-entity"
    relation_1.relationship_data = [{"relationship-value": "test"}]
    relation_2 = mock.MagicMock()
    relation_2.related_to = "project"
    relation_2.relationship_data = [{"relationship-value": "test"}]

    aai_service_instance_mock.relationships = (item for item in [relation_1, relation_2])

    pnf_modification = PnfModificationRequest. \
        send_request(aai_service_instance=aai_service_instance_mock,
                     pnf_object=pnf_object_mock,
                     sdc_service=mock.MagicMock())

    mock_pnf_modification_send_message.assert_called_once()
    method, _, url = mock_pnf_modification_send_message.call_args[0]
    assert method == "PUT"
    assert url == (f"{PnfModificationRequest.base_url}/onap/so/infra/serviceInstantiation/"
                   f"{PnfModificationRequest.api_version}/serviceInstances/"
                   f"{aai_service_instance_mock.instance_id}/pnfs/{pnf_object_mock.pnf_id}")
