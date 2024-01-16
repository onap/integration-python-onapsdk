"""SDC PNF module."""
#   Copyright 2024 Deutsche Telekom AG
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
from onapsdk.sdc2.sdc import ResoureTypeEnum
from onapsdk.sdc2.sdc_resource import SDCResourceTypeObject, SDCResourceTypeObjectCreateMixin


class Pnf(SDCResourceTypeObject, SDCResourceTypeObjectCreateMixin):  # pylint: disable=too-many-ancestors
    """PNF class."""

    @classmethod
    def resource_type(cls) -> ResoureTypeEnum:
        """PNF resource type.

        Returns:
            ResoureTypeEnum: PNF resource type enum value

        """
        return ResoureTypeEnum.PNF

    @classmethod
    def create_payload_template(cls) -> str:
        """Get a template to create PNF creation request payload.

        Returns:
            str: PNF creation template.

        """
        return "sdc2_create_pnf.json.j2"
