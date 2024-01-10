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
    responses = list(AaiBulk().single_transaction(
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
    responses = list(AaiBulk().single_transaction(
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
    responses = list(AaiBulk().single_transaction(
        [
            AaiBulkRequest(
                action="post",
                uri=f"test-uri-{i}",
                body={"blabla: blabla"}
            ) for i in range(31)
        ]
    ))
    assert mock_send_message_json.call_count == 2

    mock_send_message_json.reset_mock()
    responses = list(AaiBulk().single_transaction([]))
    assert mock_send_message_json.call_count == 0


def test_get_failed_operation_index():
    aai_bulk = AaiBulk()
    def get_formatted_response_error_with_operation(index: int) -> str:
        return ('{"requestError":{"serviceException":{"messageId":"SVC3000","text":"Invalid input performing %1 on %2 (msg=%3)'
                f' (ec=%4)","variables":["POST","v27/bulk/single-transaction","Invalid input performing %1 on %2:Error with operation {index}: '
                'Missing required property: physical-location-type,Missing required property: street1,Missing required property: city,'
                'Missing required property: postal-code,Missing required property: country,Missing required property: region","ERR.5.2.3000"]}}}')
    def get_formatted_response_not_found(index: int) -> str:
        return ('{"requestError":{"serviceException":{"messageId":"SVC3000","text":"Invalid input performing %1 on %2 (msg=%3) '
                f'(ec=%4)","variables":["POST","v27/bulk/single-transaction","Invalid input performing %1 on %2:Operation {index} with action '
                '(DELETE) on uri (/cloud-infrastructure/complexes/complex/test-parse-bulk-response) failed with status code (404), error code '
                '(ERR.5.4.6114) and msg (Node Not Found:No Node of type complex found at: /cloud-infrastructure/complexes/complex/test-parse-bulk-response)","ERR.5.2.3000"]}}}')
    assert aai_bulk._get_failed_operation_index(None) == -1
    assert aai_bulk._get_failed_operation_index("Something on what there is no index") == -1
    assert aai_bulk._get_failed_operation_index("There is an index: 0 but it's not a valid string") == -1
    for i in [pow(10, x) for x in range(6)]:
        assert aai_bulk._get_failed_operation_index(get_formatted_response_error_with_operation(i)) == i
        assert aai_bulk._get_failed_operation_index(get_formatted_response_not_found(i)) == i
