"""Policy Framework API."""

#   Copyright Deutsche Telekom AG
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

from typing import Optional, Dict, Any
from urllib.parse import urljoin
from requests import Response
from onapsdk.configuration import settings
from onapsdk.onap_service import OnapService  # type: ignore


class Policy(OnapService):  # type: ignore
    """Base Policy class."""

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': settings.POLICY_API_AUTH
    }

    @classmethod
    def send_request(cls,  # pylint: disable=too-many-arguments
                     method: str, action: str, base_url: str, relative_url: str,
                     headers: Dict[str, str], data: Optional[Dict[Any, Any]] = None) -> \
            Optional['Response']:
        """Process policy requests.

        Args:
            method (str): HTTP method type
            action (str): Action to be performed
            base_url (str): Base url of service
            relative_url (str): Relative url
            headers (Dict[str, str]): headers
            data (Optional[Dict[Any, Any]]): Request body

        Returns:
            Optional[Response]: Response object or None if something goes wrong
        """
        full_url: str = urljoin(base_url, relative_url)
        response: Response = cls.send_message(
            method,
            action,
            full_url,
            headers=headers,
            data=data
        )
        return response

    @classmethod
    def store(cls, policy: Dict[Any, Any]) -> Optional['Response']:
        """Store the policy.

        Args:
            policy (Dict): Policy to be stored

        Returns:
            Optional[Response]: Response object or None if something goes wrong
        """
        store_url: str = "/policy/api/v1/policytypes/onap.policies.native.ToscaXacml" \
                         "/versions/1.0.0/policies"
        return cls.send_request("POST", "Store policy", settings.POLICY_API_URL,
                                store_url, cls.headers, policy)

    @classmethod
    def deploy(cls, policy: Dict[Any, Any]) -> Optional['Response']:
        """Deploy the policy.

        Args:
            policy (Dict): Policy to be deployed

        Returns:
            Optional[Response]: Response object or None if something goes wrong
        """
        deploy_url: str = "/policy/pap/v1/pdps/policies"
        return cls.send_request("POST", "Deploy policy", settings.POLICY_PAP_URL,
                                deploy_url, cls.headers, policy)

    @classmethod
    def undeploy(cls, policy_id: str) -> Optional['Response']:
        """Undeploy the policy by its ID.

        Args:
            policy_id (str): Policy id to be undeployed

        Returns:
            Optional[Response]: Response object or None if something goes wrong
        """
        undeploy_url: str = f"/policy/pap/v1/pdps/policies/{policy_id}"
        return cls.send_request("DELETE", "Undeploy policy", settings.POLICY_PAP_URL,
                                undeploy_url, cls.headers)

    @classmethod
    def delete(cls, policy_id: str, policy_version: str) -> Optional['Response']:
        """Delete the policy by its ID.

        Args:
            policy_id (str): The ID of the policy to be deleted,
            policy_version (str): The version of the policy to be deleted

        Returns:
            Optional[Response]: Response object or None if something goes wrong
        """
        delete_url: str = f"/policy/api/v1/policytypes/onap.policies.native.ToscaXacml/" \
                          f"versions/1.0.0/policies/{policy_id}/versions/{policy_version}"
        return cls.send_request("DELETE", "Delete policy", settings.POLICY_API_URL
                                , delete_url, cls.headers)

    @classmethod
    def get(cls, policy_id: str, policy_version: str) -> Optional['Response']:
        """Get the specific policy by its ID and version.

        Args:
            policy_id (str): The ID of the policy to be deleted,
            policy_version (str): The version of the policy to be deleted

        Returns:
            Optional[Response]: Response object or None if something goes wrong
        """
        get_url: str = f"/policy/api/v1/policytypes/onap.policies.native.ToscaXacml/versions" \
                       f"/1.0.0/policies/{policy_id}/versions/{policy_version}"
        return cls.send_request("GET", "Get specific policy", settings.POLICY_API_URL
                                , get_url, cls.headers)

    @classmethod
    def decision(cls, decision_request: Dict[Any, Any]) -> Optional['Response']:
        """Get decision response for request.

        Args:
            decision_request (Dict): Decision request

        Returns:
            Optional[Response]: Response object or None if something goes wrong
        """
        decision_url: str = "/policy/pdpx/v1/xacml"
        headers = {
            'Content-Type': 'application/xacml+json',
            'Accept': 'application/xacml+json',
            'Authorization': settings.POLICY_PDP_AUTH
        }
        return cls.send_request("POST", "Get decision", settings.POLICY_PDP_URL,
                                decision_url, headers, decision_request)
