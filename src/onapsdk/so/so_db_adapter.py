"""Database Adapter module."""
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
from abc import ABC
from dataclasses import dataclass
from typing import Dict, Any
import warnings

from onapsdk.so.so_element import SoElement
from onapsdk.onap_service import OnapService
from onapsdk.utils.headers_creator import headers_so_creator, headers_so_catelog_db_creator
from onapsdk.utils.jinja import jinja_env


@dataclass
class IdentityService:  # pylint: disable=too-many-instance-attributes
    """Class to store identity service details."""

    identity_id: str
    url: str = "http://1.2.3.4:5000/v2.0"  # NOSONAR
    mso_id: str = "onapsdk_user"
    mso_pass: str = "mso_pass_onapsdk"
    project_domain_name: str = "NULL"
    user_domain_name: str = "NULL"
    admin_tenant: str = "service"
    member_role: str = "admin"
    identity_server_type: str = "KEYSTONE"
    identity_authentication_type: str = "USERNAME_PASSWORD"
    hibernate_lazy_initializer = {}
    server_type_as_string: str = "KEYSTONE"
    tenant_metadata: bool = True


class SoDbAdapter(SoElement, ABC):
    """DB Adapter class."""

    @classmethod
    def add_cloud_site(cls,
                       cloud_region_id: str,
                       complex_id: str,
                       identity_service: IdentityService,
                       orchestrator: str = "multicloud"
                       ):
        """Add cloud_site data with identity_service to SO db.

        Args:
            cloud_region_id (str): The id of cloud region
            complex_id (str): The id of complex
            identity_service (IdentityService): Identity service related to the cloud region
            orchestrator (str, optional): Orchestrator type. Defaults to multicloud.

        Important:
            identity_services data will be overwrite, but in the same time
            cloud_sites data will not (shouldn't) be overwrite!
            SOCatalogDB REST API has some limitations reported: https://jira.onap.org/browse/SO-2727

        Return:
            response object
        """
        response = cls.send_message_json(
            "POST",
            "Create a region in SO db",
            f"{cls.base_url}/cloudSite",
            data=jinja_env().get_template("add_cloud_site_with_identity_service.json.j2").
            render(
                cloud_region_id=cloud_region_id,
                complex_id=complex_id,
                orchestrator=orchestrator,
                identity_service=identity_service
            ),
            headers=headers_so_creator(OnapService.headers)
        )
        return response

    @classmethod
    def get_service_vnf_info(cls, identifier: str) -> Dict[Any, Any]:
        """Get Service VNF and VF details.

        Returns:
            The response in a dict format

        """
        warnings.warn("That method is deprecated and it's going to be removed. Please use "
                      "onapsdk.so.ecomp.Ecomp.get_service_vnf_info instead.")
        url = f"{cls.base_url}/ecomp/mso/catalog/v2/serviceVnfs?serviceModelUuid={identifier}"
        headers = headers_so_catelog_db_creator(OnapService.headers)
        return cls.send_message_json("GET", "Get Service Details", url, headers=headers)
