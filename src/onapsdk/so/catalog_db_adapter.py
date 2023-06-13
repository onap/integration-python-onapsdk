#   Copyright 2023 Deutsche Telekom AG
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
"""SO ecomp module."""
from abc import ABC
from typing import Any, Dict

from onapsdk.configuration import settings
from onapsdk.onap_service import OnapService
from onapsdk.so.so_element import SoElement
from onapsdk.utils.headers_creator import headers_so_catelog_db_creator


class CatalogDbAdapter(SoElement, ABC):
    """SO catalog db adapter service class."""

    base_url = settings.SO_CATALOG_DB_ADAPTER_URL
    headers = headers_so_catelog_db_creator(OnapService.headers)

    @classmethod
    def get_service_info(cls, service_model_uuid: str) -> Dict[Any, Any]:
        """Get Service VNF and VF details.

        Returns:
            The response in a dict format

        """
        url = (f"{cls.base_url}/ecomp/mso/catalog/v2/serviceResources?"
               f"serviceModelUuid={service_model_uuid}")
        return cls.send_message_json("GET", "Get Service Details", url, headers=cls.headers)

    @classmethod
    def get_service_vnf_info(cls, service_model_uuid: str) -> Dict[Any, Any]:
        """Get Service VNF and VF details.

        Returns:
            The response in a dict format

        """
        url = (f"{cls.base_url}/ecomp/mso/catalog/v2/serviceVnfs?"
               f"serviceModelUuid={service_model_uuid}")
        return cls.send_message_json("GET", "Get Service Details", url, headers=cls.headers)
