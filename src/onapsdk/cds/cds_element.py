"""Base CDS module."""
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

from onapsdk.configuration import settings
from onapsdk.onap_service import OnapService
from onapsdk.utils.gui import GuiItem, GuiList

class CdsElement(OnapService, ABC):
    """Base CDS class.

    Stores url to CDS API (edit if you want to use other) and authentication tuple
    (username, password).
    """

    # These should be stored in configuration. There is even a task in Orange repo.
    _url: str = settings.CDS_URL
    auth: tuple = settings.CDS_AUTH

    @classmethod
    def get_guis(cls) -> GuiList:
        """Retrieve the status of the CDS GUIs.

        Only one GUI is referenced for CDS: CDS UI

        Return the list of GUIs
        """
        gui_url = settings.CDS_GUI_SERVICE
        cds_gui_response = cls.send_message(
            "GET", "Get CDS GUI Status", gui_url)
        guilist = GuiList([])
        guilist.add(GuiItem(
            gui_url,
            cds_gui_response.status_code))
        return guilist
