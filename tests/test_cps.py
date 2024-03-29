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

import requests
from unittest import mock
from typing import List

import pytest
from onapsdk.cps import Anchor, Dataspace, SchemaSet, SchemaSetModuleReference
from onapsdk.exceptions import (APIError, ResourceNotFound, SDKException)

DATASPACE_ANCHOR = {
    "name": "anchor1",
    "schemaSetName": "schemaSet1"
}

DATASPACE_ANCHORS = [
    DATASPACE_ANCHOR,
    {
        "name": "anchor2",
        "schemaSetName": "schemaSet2"
    }
]

DATASPACE_SCHEMA_SET = {
    "name": "schemaSet1",
    "moduleReferences": [
        {
            "name": "mr1",
            "namespace": "mr1_namespace",
            "revision": "mr1_revision",
        },
        {
            "name": "mr2",
            "namespace": "mr2_namespace",
            "revision": "mr2_revision",
        }
    ]
}

# Dataspace tests
def test_dataspace():
    ds = Dataspace(name="test_ds")
    assert ds.name == "test_ds"
    assert f"cps/api/v2/dataspaces/{ds.name}" in ds.url

@mock.patch("onapsdk.cps.Dataspace.send_message")
def test_dataspace_create_anchor(mock_send_message):
    ds = Dataspace(name="test_ds")
    anchor = ds.create_anchor(mock.MagicMock(), "test_anchor")
    mock_send_message.assert_called_once()
    assert anchor.name == "test_anchor"

@mock.patch("onapsdk.cps.Dataspace.send_message_json")
def test_dataspace_get_anchors(mock_send_message_json):
    mock_send_message_json.return_value = DATASPACE_ANCHORS
    ds = Dataspace(name="test_ds")
    anchors = list(ds.get_anchors())
    assert len(anchors) == 2
    anchor_1, anchor_2 = anchors
    assert isinstance(anchor_1, Anchor)
    assert isinstance(anchor_2, Anchor)
    assert anchor_1.name == "anchor1"
    assert isinstance(anchor_1.schema_set, SchemaSet)
    assert anchor_1.schema_set.name == "schemaSet1"
    assert anchor_1.schema_set.dataspace == ds
    assert anchor_2.name == "anchor2"
    assert isinstance(anchor_2.schema_set, SchemaSet)
    assert anchor_2.schema_set.name == "schemaSet2"
    assert anchor_2.schema_set.dataspace == ds

@mock.patch("onapsdk.cps.Dataspace.send_message_json")
def test_dataspace_get_anchor(mock_send_message_json):
    mock_send_message_json.return_value = DATASPACE_ANCHOR
    ds = Dataspace(name="test_ds")
    anchor = ds.get_anchor("anything")
    assert anchor.name == "anchor1"
    assert anchor.schema_set.name == "schemaSet1"
    assert anchor.schema_set.dataspace == ds

@mock.patch("onapsdk.cps.Dataspace.send_message")
def test_dataspace_delete_anchor(mock_send_message):
    ds = Dataspace(name="test_ds")
    ds.delete_anchor("some-anchor")
    mock_send_message.assert_called_once()
    args = mock_send_message.call_args
    assert args[0][0] == "DELETE"
    assert args[0][2].split('/')[-1] == "some-anchor"

@mock.patch("onapsdk.cps.Dataspace.send_message_json")
def test_dataspace_get_schema_set(mock_send_message_json):
    mock_send_message_json.return_value = DATASPACE_SCHEMA_SET
    ds = Dataspace(name="test_ds")
    schema_set = ds.get_schema_set("anything")
    assert isinstance(schema_set, SchemaSet)
    assert schema_set.dataspace == ds
    assert schema_set.name == "schemaSet1"
    assert len(schema_set.module_refences) == 2
    mr_1, mr_2 = schema_set.module_refences
    assert mr_1.name == "mr1"
    assert mr_1.namespace == "mr1_namespace"
    assert mr_1.revision == "mr1_revision"
    assert mr_2.name == "mr2"
    assert mr_2.namespace == "mr2_namespace"
    assert mr_2.revision == "mr2_revision"

@mock.patch("onapsdk.cps.Dataspace.send_message")
@mock.patch("onapsdk.cps.Dataspace.get_schema_set")
def test_dataspace_create_schema_set(mock_get_chema_set, mock_send_message):
    ds = Dataspace(name="test_ds")
    _ = ds.create_schema_set("test_schema_set_name", b"fake_file")
    mock_send_message.assert_called_once()
    mock_get_chema_set.assert_called_once_with("test_schema_set_name")

@mock.patch("onapsdk.cps.Dataspace.send_message")
def test_dataspace_delete(mock_send_message):
    ds = Dataspace(name="test_ds")
    ds.delete()
    mock_send_message.assert_called_once()

@mock.patch("onapsdk.cps.Dataspace.send_message_json")
def test_dataspace_get_dataspace(mock_send_message_json):
    mock_send_message_json.return_value = {"name": "test_ds"}
    dataspace_name = "test_ds"
    dataspace = Dataspace.get_dataspace(dataspace_name)
    assert dataspace.name == dataspace_name

# Schemaset tests
def test_schema_set():
    schema_set = SchemaSet(name="test", dataspace=mock.MagicMock())
    assert schema_set.name == "test"
    assert isinstance(schema_set.module_refences, List)
    assert not len(schema_set.module_refences)

    schema_set = SchemaSet(name="test_with_mr", dataspace=mock.MagicMock(),
                           module_references=[SchemaSetModuleReference(name="mr1", namespace="mr1_n", revision="mr1_rev"),
                                              SchemaSetModuleReference(name="mr2", namespace="mr2_n", revision="mr2_rev")])
    assert schema_set.name == "test_with_mr"
    assert isinstance(schema_set.module_refences, List)
    assert len(schema_set.module_refences) == 2
    mr_1, mr_2 = schema_set.module_refences
    assert isinstance(mr_1, SchemaSetModuleReference)
    assert isinstance(mr_2, SchemaSetModuleReference)
    assert mr_1.name == "mr1"
    assert mr_1.namespace == "mr1_n"
    assert mr_1.revision == "mr1_rev"
    assert mr_2.name == "mr2"
    assert mr_2.namespace == "mr2_n"
    assert mr_2.revision == "mr2_rev"

@mock.patch("onapsdk.cps.SchemaSet.send_message")
def test_schemaset_delete(mock_send_message):
    schema_set = SchemaSet(name="test", dataspace=mock.MagicMock())
    schema_set.delete()
    mock_send_message.assert_called_once()

# Anchor tests
def test_anchor():
    anchor = Anchor(name="test_anchor", schema_set=mock.MagicMock())
    assert anchor.name == "test_anchor"
    assert "test_anchor" in anchor.url

@mock.patch("onapsdk.cps.Anchor.send_message")
def test_anchor_delete(mock_send_message):
    anchor = Anchor(name="test_anchor", schema_set=mock.MagicMock())
    anchor.delete()
    mock_send_message.assert_called_once()
    url = mock_send_message.call_args[0][2]
    assert anchor.url.rstrip("/") in url

@mock.patch("onapsdk.cps.Anchor.send_message")
def test_anchor_create_node(mock_send_message):
    anchor = Anchor(name="test_anchor", schema_set=mock.MagicMock())
    anchor.create_node('{"test": "data"}')
    mock_send_message.assert_called_once()
    data = mock_send_message.call_args[1]["data"]
    assert data == '{"test": "data"}'

@mock.patch("onapsdk.cps.Anchor.send_message_json")
def test_anchor_get_node(mock_send_message_json):
    anchor = Anchor(name="test_anchor", schema_set=mock.MagicMock())
    anchor.get_node("test-xpath")
    mock_send_message_json.assert_called_once()
    params = mock_send_message_json.call_args.kwargs["params"]
    assert "xpath" in params and params["xpath"] == "test-xpath"
    assert "descendants" in params and params["descendants"] == 0

    mock_send_message_json.reset_mock()
    anchor.get_node("test-xpath-2", descendants=-1)
    mock_send_message_json.assert_called_once()
    params = mock_send_message_json.call_args.kwargs["params"]
    assert "xpath" in params and params["xpath"] == "test-xpath-2"
    assert "descendants" in params and params["descendants"] == -1

    mock_send_message_json.reset_mock()
    anchor.get_node("test-xpath-3", descendants=2)
    mock_send_message_json.assert_called_once()
    params = mock_send_message_json.call_args.kwargs["params"]
    assert "xpath" in params and params["xpath"] == "test-xpath-3"
    assert "descendants" in params and params["descendants"] == 2

@mock.patch("onapsdk.cps.Anchor.send_message")
def test_anchor_update_node(mock_send_message):
    anchor = Anchor(name="test_anchor", schema_set=mock.MagicMock())
    anchor.update_node("test-xpath", '{"test": "data"}')
    mock_send_message.assert_called_once()
    params = mock_send_message.call_args.kwargs["params"]
    assert "xpath" in params and params["xpath"] == "test-xpath"

@mock.patch("onapsdk.cps.Anchor.send_message")
def test_anchor_replace_node(mock_send_message):
    anchor = Anchor(name="test_anchor", schema_set=mock.MagicMock())
    anchor.replace_node("test-xpath", '{"test": "data"}')
    mock_send_message.assert_called_once()
    params = mock_send_message.call_args.kwargs["params"]
    assert "xpath" in params and params["xpath"] == "test-xpath"

@mock.patch("onapsdk.cps.Anchor.send_message")
def test_anchor_add_list_node(mock_send_message):
    anchor = Anchor(name="test_anchor", schema_set=mock.MagicMock())
    anchor.add_list_node("test-xpath", '{"test": "data"}')
    mock_send_message.assert_called_once()
    params = mock_send_message.call_args.kwargs["params"]
    assert "xpath" in params and params["xpath"] == "test-xpath"

@mock.patch("onapsdk.cps.Anchor.send_message_json")
def test_anchor_query_node(mock_send_message_json):
    anchor = Anchor(name="test_anchor", schema_set=mock.MagicMock())
    anchor.query_node("/test-query")
    mock_send_message_json.assert_called_once()
    params = mock_send_message_json.call_args.kwargs["params"]
    assert "cps-path" in params and params["cps-path"] == "/test-query"
    assert "include-descendants" in params and params["include-descendants"] is False

    mock_send_message_json.reset_mock()
    anchor.query_node("/test-query1", include_descendants=True)
    mock_send_message_json.assert_called_once()
    params = mock_send_message_json.call_args.kwargs["params"]
    assert "cps-path" in params and params["cps-path"] == "/test-query1"
    assert "include-descendants" in params and params["include-descendants"] is True

@mock.patch("onapsdk.cps.Anchor.send_message")
def test_anchor_delete_nodes(mock_send_message):
    anchor = Anchor(name="test_anchor", schema_set=mock.MagicMock())
    anchor.delete_nodes("test-xpath")
    mock_send_message.assert_called_once()
    params = mock_send_message.call_args.kwargs["params"]
    assert "xpath" in params and params["xpath"] == "test-xpath"

@mock.patch("onapsdk.cps.Dataspace.send_message")
def test_dataspace_create_anchor_except(mock_send_message_json):
    ds = Dataspace(name="test_creating_anchor")
    mock_send_message_json.exceptions = requests.exceptions
    mock_send_message_json.side_effect = APIError('Dataspace not found', 400)
    with pytest.raises(ResourceNotFound):
        ds.create_anchor(mock.MagicMock(), "test_creating_anchor")
    mock_send_message_json.side_effect = APIError()
    with pytest.raises(SDKException):
        ds.create_anchor(mock.MagicMock(), "test_creating_anchor")

@mock.patch("onapsdk.cps.Dataspace.send_message_json")
def test_dataspace_get_anchors_except(mock_send_message_json):
    ds = Dataspace(name="test_ds")
    mock_send_message_json.exceptions = requests.exceptions
    mock_send_message_json.side_effect = APIError('Dataspace not found', 400)
    with pytest.raises(ResourceNotFound):
        list(ds.get_anchors())
    mock_send_message_json.side_effect = APIError()
    with pytest.raises(SDKException):
        list(ds.get_anchors())

@mock.patch("onapsdk.cps.Dataspace.send_message_json")
def test_dataspace_get_anchor_except(mock_send_message_json):
    ds = Dataspace(name="test_ds")
    mock_send_message_json.exceptions = requests.exceptions
    mock_send_message_json.side_effect = APIError('Dataspace not found', 400)
    with pytest.raises(ResourceNotFound):
        ds.get_anchor(mock.MagicMock())
    mock_send_message_json.side_effect = APIError()
    with pytest.raises(SDKException):
        ds.get_anchor(mock.MagicMock())

@mock.patch("onapsdk.cps.Dataspace.send_message_json")
def test_dataspace_get_schema_set_except(mock_send_message_json):
    mock_send_message_json.return_value = DATASPACE_SCHEMA_SET
    ds = Dataspace(name="test_ds")
    mock_send_message_json.exceptions = requests.exceptions
    mock_send_message_json.side_effect = APIError('Dataspace not found', 400)
    with pytest.raises(ResourceNotFound):
        ds.get_schema_set(mock.MagicMock())
    mock_send_message_json.side_effect = APIError()
    with pytest.raises(SDKException):
        ds.get_schema_set(mock.MagicMock())


@mock.patch("onapsdk.cps.Dataspace.send_message")
@mock.patch("onapsdk.cps.Dataspace.get_schema_set")
def test_dataspace_create_schema_set_except(mock_get_chema_set, mock_send_message):
    ds = Dataspace(name="test_ds")
    _ = ds.create_schema_set("test_schema_set_name", b"fake_file")
    mock_send_message.exceptions = requests.exceptions
    mock_send_message.side_effect = APIError('Dataspace not found', 400)
    mock_get_chema_set.exceptions = requests.exceptions
    mock_get_chema_set.side_effect = APIError('Dataspace not found', 400)
    with pytest.raises(ResourceNotFound):
        ds.create_schema_set(mock.MagicMock(), 8)
    mock_send_message.side_effect = APIError()
    mock_get_chema_set.side_effect = APIError()
    with pytest.raises(SDKException):
        ds.create_schema_set(mock.MagicMock(), 9)
