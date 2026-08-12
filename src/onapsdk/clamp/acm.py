"""ONAP SDK ACM (Automation Composition Management) module."""
#   Copyright 2026 Deutsche Telekom AG
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
from typing import Any, Dict

from requests import Response

from onapsdk.configuration import settings
from onapsdk.onap_service import OnapService  # type: ignore


class Acm(OnapService):  # type: ignore
    """Automation Composition Management runtime class."""

    name: str = "ACM"

    # The runtime-acm openapi.yaml declares servers[0] as onap/acm/v3, but the
    # OOM deployment sets server.servlet.context-path to /onap/policy/clamp/acm
    # and AbstractRestController maps /v2, so this is the deployed prefix.
    ACM_BASE_PATH: str = "/onap/policy/clamp/acm/v2"

    @classmethod
    def base_url(cls) -> str:
        """Automation composition runtime base url.

        Returns:
            str: Base url of the ACM runtime API
        """
        return f"{settings.CLAMP_ACM_URL}{cls.ACM_BASE_PATH}"

    @classmethod
    def commission(cls, service_template: Dict[str, Any],
                   basic_auth: Dict[str, str]) -> Response:
        """Commission an automation composition definition.

        A body without metadata.compositionId creates a new definition and
        the runtime answers 201; with one it updates and answers 200.

        Args:
            service_template (Dict[str, Any]): Tosca service template
            basic_auth (Dict[str, str]): ACM runtime credentials

        Returns:
            Response: Commissioning response with the compositionId
        """
        return cls.send_message(
            "POST",
            "Commission automation composition definition",
            f"{cls.base_url()}/compositions",
            basic_auth=basic_auth,
            json=service_template)

    @classmethod
    def get_composition(cls, composition_id: str,
                        basic_auth: Dict[str, str]) -> Response:
        """Get an automation composition definition.

        Args:
            composition_id (str): Composition definition id
            basic_auth (Dict[str, str]): ACM runtime credentials

        Returns:
            Response: The automation composition definition
        """
        return cls.send_message(
            "GET",
            "Get automation composition definition",
            f"{cls.base_url()}/compositions/{composition_id}",
            basic_auth=basic_auth)

    @classmethod
    def set_composition_state(cls, composition_id: str, prime_order: str,
                              basic_auth: Dict[str, str]) -> Response:
        """Prime or deprime an automation composition definition.

        The runtime answers 202 and performs the state change over Kafka, so
        the caller has to poll get_composition until a terminal state.

        Args:
            composition_id (str): Composition definition id
            prime_order (str): PRIME, DEPRIME or NONE
            basic_auth (Dict[str, str]): ACM runtime credentials

        Returns:
            Response: Accepted response
        """
        return cls.send_message(
            "PUT",
            "Set automation composition definition state",
            f"{cls.base_url()}/compositions/{composition_id}",
            basic_auth=basic_auth,
            json={"primeOrder": prime_order})

    @classmethod
    def delete_composition(cls, composition_id: str,
                           basic_auth: Dict[str, str]) -> Response:
        """Delete an automation composition definition.

        Fails with 400 unless the definition is in COMMISSIONED state.

        Args:
            composition_id (str): Composition definition id
            basic_auth (Dict[str, str]): ACM runtime credentials

        Returns:
            Response: Commissioning response
        """
        return cls.send_message(
            "DELETE",
            "Delete automation composition definition",
            f"{cls.base_url()}/compositions/{composition_id}",
            basic_auth=basic_auth)

    @classmethod
    def create_instance(cls, composition_id: str, instance: Dict[str, Any],
                        basic_auth: Dict[str, str]) -> Response:
        """Create an automation composition instance.

        A body without instanceId creates a new instance and the runtime
        answers 201; with one it updates and answers 200.

        Args:
            composition_id (str): Composition definition id
            instance (Dict[str, Any]): Automation composition instance
            basic_auth (Dict[str, str]): ACM runtime credentials

        Returns:
            Response: Instantiation response with the instanceId
        """
        return cls.send_message(
            "POST",
            "Create automation composition instance",
            f"{cls.base_url()}/compositions/{composition_id}/instances",
            basic_auth=basic_auth,
            json=instance)

    @classmethod
    def get_instance(cls, composition_id: str, instance_id: str,
                     basic_auth: Dict[str, str]) -> Response:
        """Get an automation composition instance.

        Args:
            composition_id (str): Composition definition id
            instance_id (str): Automation composition instance id
            basic_auth (Dict[str, str]): ACM runtime credentials

        Returns:
            Response: The automation composition instance
        """
        return cls.send_message(
            "GET",
            "Get automation composition instance",
            f"{cls.base_url()}/compositions/{composition_id}"
            f"/instances/{instance_id}",
            basic_auth=basic_auth)

    @classmethod
    def set_instance_state(cls, composition_id: str, instance_id: str,
                           deploy_order: str,
                           basic_auth: Dict[str, str]) -> Response:
        """Deploy or undeploy an automation composition instance.

        The runtime answers 202 and performs the state change over Kafka, so
        the caller has to poll get_instance until a terminal state.

        Args:
            composition_id (str): Composition definition id
            instance_id (str): Automation composition instance id
            deploy_order (str): DEPLOY, UNDEPLOY, DELETE, UPDATE or NONE
            basic_auth (Dict[str, str]): ACM runtime credentials

        Returns:
            Response: Accepted response
        """
        return cls.send_message(
            "PUT",
            "Set automation composition instance state",
            f"{cls.base_url()}/compositions/{composition_id}"
            f"/instances/{instance_id}",
            basic_auth=basic_auth,
            json={"deployOrder": deploy_order})

    @classmethod
    def delete_instance(cls, composition_id: str, instance_id: str,
                        basic_auth: Dict[str, str]) -> Response:
        """Delete an automation composition instance.

        Args:
            composition_id (str): Composition definition id
            instance_id (str): Automation composition instance id
            basic_auth (Dict[str, str]): ACM runtime credentials

        Returns:
            Response: Instantiation response
        """
        return cls.send_message(
            "DELETE",
            "Delete automation composition instance",
            f"{cls.base_url()}/compositions/{composition_id}"
            f"/instances/{instance_id}",
            basic_auth=basic_auth)
