"""SDNC base module."""
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
from onapsdk.configuration import settings
from onapsdk.onap_service import OnapService
from onapsdk.utils.gui import GuiItem, GuiList


class SdncElement(OnapService):
    """SDNC base class."""

    base_url = settings.SDNC_URL

    @classmethod
    def get_guis(cls) -> GuiList:
        """Retrieve the status of the SDNC GUIs.

        There are 2 GUIS
        - SDNC DG Builder
        - SDNC ODL

        Return the list of GUIs
        """
        guilist = GuiList([])
        url = settings.SDNC_DG_GUI_SERVICE
        response = cls.send_message(
            "GET", "Get SDNC GUI DG Status", url)
        guilist.add(GuiItem(
            url,
            response.status_code))
        url = settings.SDNC_ODL_GUI_SERVICE
        response = cls.send_message(
            "GET", "Get SDNC ODL GUI Status", url)
        guilist.add(GuiItem(
            url,
            response.status_code))
        return guilist
