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

from onapsdk.aai.bulk import AaiBulk, AaiBulkRequest, AaiBulkResponse


BULK_RESPONSES = {
    "operation-responses": [
        {
            "action": "put",
            "uri": "test-uri",
            "response-status-code": 400,
            "response-body": None
        },
        {
            "action": "post",
            "uri": "test-uri",
            "response-status-code": 201,
            "response-body": "blabla"
        }
    ]
}


@mock.patch("onapsdk.aai.bulk.AaiBulk.send_message_json")
def test_aai_bulk(mock_send_message_json):
    assert AaiBulk().url.endswith("bulk")
    mock_send_message_json.return_value = BULK_RESPONSES
    responses = list(AaiBulk.single_transaction(
        [
            AaiBulkRequest(
                action="post",
                uri="test-uri",
                body={"blabla: blabla"}
            ),
            AaiBulkRequest(
                action="get",
                uri="test-uri",
                body={}
            )
        ]
    ))
    assert len(responses) == 2
    resp_1, resp_2 = responses
    assert resp_1.action == "put"
    assert resp_1.uri == "test-uri"
    assert resp_1.status_code == 400
    assert resp_1.body is None
    assert resp_2.action == "post"
    assert resp_2.uri == "test-uri"
    assert resp_2.status_code == 201
    assert resp_2.body == "blabla"

    # Check if requests was splitted into chunks for generator
    mock_send_message_json.reset_mock()
    responses = list(AaiBulk.single_transaction(
        (
            AaiBulkRequest(
                action="post",
                uri=f"test-uri-{i}",
                body={"blabla: blabla"}
            ) for i in range(31)
        )
    ))
    assert mock_send_message_json.call_count == 2

    # Check if requests was splitted into chunks for list
    mock_send_message_json.reset_mock()
    responses = list(AaiBulk.single_transaction(
        [
            AaiBulkRequest(
                action="post",
                uri=f"test-uri-{i}",
                body={"blabla: blabla"}
            ) for i in range(31)
        ]
    ))
    assert mock_send_message_json.call_count == 2
