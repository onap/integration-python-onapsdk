"""Test A&AI Element."""
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
import logging
import unittest

from onapsdk.nbi.nbi import Nbi
from onapsdk.utils.gui import GuiItem, GuiList
from onapsdk.exceptions import NoGuiError

class GuiTestingBase(unittest.TestCase):

    """The super class which testing classes could inherit."""
    logging.disable(logging.CRITICAL)

    def test_get_guis_request_error(self):
        nbi_element = Nbi()
        with self.assertRaises(NoGuiError):
            nbi_element.get_guis()

    def test_create_bad_gui_item(self):
        with self.assertRaises(TypeError):
            gui1 = GuiItem(184)

    def test_create_bad_gui_list(self):
        with self.assertRaises(TypeError):
            list = GuiList(1, 2, 3)

    def test_add_gui_item(self):
        gui1 = GuiItem('url1', 184)
        gui2 = GuiItem('url2', 200)
        test = GuiList([])
        test.add(gui1)
        test.add(gui2)
        assert len(test.guilist) == 2
        assert test.guilist[0].status == 184
        assert test.guilist[1].url == 'url2'

    def test_add_bad_gui_item(self):
        with self.assertRaises(AttributeError):
            test = GuiList([])
            test.add('not a gui item object')


