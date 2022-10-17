"""Multicloud module."""
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

from .msb_service import MSB


class Multicloud(MSB):
    """MSB subclass to register/unregister instance to ONAP."""

    base_url = f"{MSB.base_url}/api/multicloud/v1"

    @classmethod
    def register_vim(cls,
                     cloud_owner: str,
                     cloud_region_id: str,
                     default_tenant: str = None) -> None:
        """Register a VIM instance to ONAP.

        Args:
            cloud_owner (str): Cloud owner name
            cloud_region_id (str): Cloud region ID
            default_tenant (str, optional): Default tenant name. Defaults to None.
        """
        cls.send_message(
            "POST",
            "Register VIM instance to ONAP",
            f"{cls.base_url}/{cloud_owner}/{cloud_region_id}/registry",
            data={"defaultTenant": default_tenant} if default_tenant else None
        )

    @classmethod
    def unregister_vim(cls, cloud_owner: str, cloud_region_id: str) -> None:
        """Unregister a VIM instance from ONAP.

        Args:
            cloud_owner (str): Cloud owner name
            cloud_region_id (str): Cloud region ID
        """
        cls.send_message(
            "DELETE",
            "Unregister VIM instance from ONAP",
            f"{cls.base_url}/{cloud_owner}/{cloud_region_id}"
        )
