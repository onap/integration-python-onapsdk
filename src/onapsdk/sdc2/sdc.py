"""Base SDC module."""
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
#   limitations under the License.from onapsdk.sdc2.sdc import ResoureTypeEnum
from abc import abstractmethod, ABC
from enum import Enum
from typing import Any, Iterator, List

from onapsdk.configuration import settings  # type: ignore
from onapsdk.onap_service import OnapService  # type: ignore
from onapsdk.utils.headers_creator import headers_sdc_creator  # type: ignore


class ResoureTypeEnum(Enum):  # pylint: disable=too-few-public-methods
    """Resource types enumerator."""

    PRODUCT = "PRODUCT"
    SERVICE = "SERVICE"
    VF = "VF"
    VFC = "VFC"
    CP = "CP"
    VL = "VL"
    CONFIGURATION = "Configuration"
    VFCMT = "VFCMT"
    CVFC = "CVFC"
    PNF = "PNF"
    CR = "CR"
    SERVICE_PROXY = "ServiceProxy"
    SERVICE_SUBSTITUTION = "ServiceSubstitution"

    @classmethod
    def iter_without_resource_type(
        cls,
        resource_type_to_exclude: "ResoureTypeEnum"
    ) -> Iterator["ResoureTypeEnum"]:
        """Return an iterator with resource types but one given as a parameter.

        Yields:
            ResoureTypeEnum: Resource types without a one given as a parameter

        """
        resources_type_list: List[ResoureTypeEnum] = list(cls)
        resources_type_list.pop(resources_type_list.index(resource_type_to_exclude))
        yield from resources_type_list


class SDC(OnapService, ABC):
    """Base SDC abstracl class."""

    base_back_url = settings.SDC_BE_URL
    SCREEN_ENDPOINT = "sdc2/rest/v1/screen"
    ARCHIVE_ENDPOINT = "sdc2/rest/v1/catalog/archive"
    headers = headers_sdc_creator(OnapService.headers)

    def __init__(self, name: str) -> None:
        """Init SDC object.

        Each SDC object has a name.

        Args:
            name (str): Name

        """
        self.name = name

    def __eq__(self, other: Any) -> bool:
        """
        Check equality for SDC and children.

        Args:
            other: another object

        Returns:
            bool: True if same object, False if not

        """
        if isinstance(other, type(self)):
            return self.name == other.name
        return False


class SDCCatalog(SDC, ABC):
    """SDC Catalog abstract class."""

    @classmethod
    @abstractmethod
    def get_all(cls) -> List["SDCCatalog"]:
        """Get all SDCCatalog objects.

        That's abstract class for each class which would implement SDC catalog API
            (VF, Service etc.)

        """
