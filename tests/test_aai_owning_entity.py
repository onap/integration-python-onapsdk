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

from onapsdk.aai.business import OwningEntity
from onapsdk.exceptions import ResourceNotFound

OWNING_ENTITIES = {
    "owning-entity": [
        {
            "owning-entity-id": "ff6c945f-89ab-4f14-bafd-0cdd6eac791a",
            "owning-entity-name": "OE-Generic",
            "resource-version": "1588244348931",
        },
        {
            "owning-entity-id": "OE-generic",
            "owning-entity-name": "OE-generic",
            "resource-version": "1587388597761"
        },
        {
            "owning-entity-id": "b3dcdbb0-edae-4384-b91e-2f114472520c"
            , "owning-entity-name": "test",
            "resource-version": "1588145971158"
        }
    ]
}

OWNING_ENTITY = {
    "owning-entity-id": "OE-generic",
    "owning-entity-name": "OE-generic",
    "resource-version": "1587388597761"
}


@mock.patch.object(OwningEntity, "send_message_json")
def test_owning_entity_get_all(mock_send):
    mock_send.return_value = OWNING_ENTITIES
    owning_entities = list(OwningEntity.get_all())
    assert len(owning_entities) == 3
    owning_entity = owning_entities[0]
    assert owning_entity.owning_entity_id == "ff6c945f-89ab-4f14-bafd-0cdd6eac791a"
    assert owning_entity.name == "OE-Generic"
    assert owning_entity.url == (f"{owning_entity.base_url}{owning_entity.api_version}/"
                                 "business/owning-entities/owning-entity/"
                                 f"{owning_entity.owning_entity_id}")


@mock.patch.object(OwningEntity, "send_message_json")
def test_owning_entity_get_by_name(mock_send):
    mock_send.return_value = OWNING_ENTITIES
    with pytest.raises(ResourceNotFound) as exc:
        OwningEntity.get_by_owning_entity_name("invalid name")
    assert exc.type == ResourceNotFound
    owning_entity = OwningEntity.get_by_owning_entity_name("OE-Generic")
    assert owning_entity.owning_entity_id == "ff6c945f-89ab-4f14-bafd-0cdd6eac791a"
    assert owning_entity.name == "OE-Generic"


@mock.patch.object(OwningEntity, "send_message")
@mock.patch.object(OwningEntity, "send_message_json")
def test_owning_entity_create(mock_send_json, mock_send):
    mock_send_json.return_value = OWNING_ENTITY
    OwningEntity.create(
        name="OE-generic",
    )

    owning_entity = OwningEntity.create(
        name="OE-generic",
        owning_entity_id="OE-generic"
    )
    assert owning_entity.owning_entity_id == "OE-generic"
    assert owning_entity.name == "OE-generic"


@mock.patch.object(OwningEntity, "send_message")
def test_owning_entity_delete(mock_send_message):
    owning_entity = OwningEntity(name="test_owning_entity",
                                 owning_entity_id="test_owning_id",
                                 resource_version="12345")
    owning_entity.delete()
    mock_send_message.assert_called_once_with(
        "DELETE",
        "Delete owning entity",
        f"{owning_entity.url}?resource-version={owning_entity.resource_version}"
    )
