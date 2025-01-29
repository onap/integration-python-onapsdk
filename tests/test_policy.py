import json
from unittest.mock import patch, MagicMock, Mock

from requests import Response

from onapsdk.configuration import settings
from onapsdk.policy.policy import Policy

decision_req = json.dumps({
    "Request": {
        "ReturnPolicyIdList": True,
        "CombinedDecision": False,
        "Action": [
            {
                "Attribute": [
                    {
                        "IncludeInResult": False,
                        "AttributeId": "action-id",
                        "Value": "capacity-check-policy-soaktest"

                    }
                ]

            }

        ],
        "Resource": [
            {
                "Attribute": [

                    {
                        "IncludeInResult": False,
                        "AttributeId": "sliceData.sliceOrder.cells.cellTotalResourceUsageUl",
                        "Value": 23
                    }
                ]
            }

        ]

    }
})


@patch("onapsdk.policy.policy.Policy.send_message")
def test_store_success(mock_send_message):
    mock_response = MagicMock(spec=Response)
    mock_response.json.return_value = {"status": "success"}
    mock_send_message.return_value = mock_response
    policy = {"policy_id": "123", "name": "Sample Policy"}
    response = Policy.store(policy)
    assert response.json() == {"status": "success"}
    mock_send_message.assert_called_once_with(
        "POST", "Store policy",
        settings.POLICY_API_URL + "/policy/api/v1/policytypes/onap.policies.native.ToscaXacml/versions/1.0.0/policies",
        headers=Policy.headers, data=policy
    )


@patch("onapsdk.policy.policy.Policy.send_message")
def test_deploy_success(mock_send_message):
    mock_response = MagicMock(spec=Response)
    mock_response.json.return_value = {"status": "success"}
    mock_send_message.return_value = mock_response
    policy = {"policy_id": "123", "name": "Sample Policy"}
    response = Policy.deploy(policy)
    assert response.json() == {"status": "success"}
    mock_send_message.assert_called_once_with(
        "POST", "Deploy policy",
        settings.POLICY_PAP_URL + "/policy/pap/v1/pdps/policies",
        headers=Policy.headers, data=policy
    )


@patch("onapsdk.policy.policy.Policy.send_message")
def test_decision_success(mock_send_message):
    mock_response = MagicMock(spec=Response)
    mock_response.json.return_value = {"status": "success"}
    mock_send_message.return_value = mock_response
    response = Policy.decision(decision_req)
    headers = {
        'Content-Type': 'application/xacml+json',
        'Accept': 'application/xacml+json',
        'Authorization': 'Basic aGVhbHRoY2hlY2s6emIhWHp0RzM0'
    }
    assert response.json() == {"status": "success"}
    mock_send_message.assert_called_once_with(
        "POST", "Get decision",
        settings.POLICY_PDP_URL + "/policy/pdpx/v1/xacml",
        headers=headers, data=decision_req
    )


@patch("onapsdk.policy.policy.Policy.send_message")
def test_get_success(mock_send_message):
    mock_response = MagicMock(spec=Response)
    mock_response.json.return_value = {"status": "success"}
    mock_send_message.return_value = mock_response
    response = Policy.get("policy-123", "1.0.0")
    assert response.json() == {"status": "success"}
    mock_send_message.assert_called_once_with(
        "GET", "Get specific policy",
        settings.POLICY_API_URL + f"/policy/api/v1/policytypes/onap.policies.native.ToscaXacml/versions/1.0.0/policies/policy-123/versions/1.0.0",
        headers=Policy.headers, data=None
    )


@patch("onapsdk.policy.policy.Policy.send_message")
def test_delete_success(mock_send_message):
    mock_response = MagicMock(spec=Response)
    mock_response.json.return_value = {"status": "success"}
    mock_send_message.return_value = mock_response
    response = Policy.delete("policy-123", "1.0.0")
    assert response.json() == {"status": "success"}
    mock_send_message.assert_called_once_with(
        "DELETE", "Delete policy",
        settings.POLICY_API_URL + f"/policy/api/v1/policytypes/onap.policies.native.ToscaXacml/versions/1.0.0/policies/policy-123/versions/1.0.0",
        headers=Policy.headers, data=None
    )


@patch("onapsdk.policy.policy.Policy.send_message")
def test_undeploy_success(mock_send_message):
    mock_response = MagicMock(spec=Response)
    mock_response.json.return_value = {"status": "success"}
    mock_send_message.return_value = mock_response
    response = Policy.undeploy("policy-123")
    assert response.json() == {"status": "success"}
    mock_send_message.assert_called_once_with(
        "DELETE", "Undeploy policy",
        settings.POLICY_PAP_URL + "/policy/pap/v1/pdps/policies/policy-123",
        headers=Policy.headers, data=None
    )
