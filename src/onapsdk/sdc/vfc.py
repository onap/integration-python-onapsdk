"""VFC module."""
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
from typing import Dict

from onapsdk.exceptions import ResourceNotFound

from .sdc_resource import SdcResource


class Vfc(SdcResource):
    """ONAP VFC Object used for SDC operations."""

    def __init__(self, name: str, version: str = None, sdc_values: Dict[str, str] = None):
        """Initialize VFC object.

        Vfc has to exist in SDC.

        Args:
            name (str): Vfc name
            version (str): Vfc version
            sdc_values (Dict[str, str], optional): Sdc values of existing Vfc. Defaults to None.

        Raises:
            ResourceNotFound: Vfc doesn't exist in SDC

        """
        super().__init__(name=name, version=version, sdc_values=sdc_values)
        if not sdc_values and not self.exists():
            raise ResourceNotFound(
                "This Vfc has to exist prior to object initialization.")

    def _really_submit(self) -> None:
        """Really submit the SDC in order to enable it."""
        raise NotImplementedError("Vfc doesn't need _really_submit")
