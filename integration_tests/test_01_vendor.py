"""Integration test Vendor module."""
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
import pytest

import requests

from onapsdk.sdc import SDC
from onapsdk.sdc.vendor import Vendor
import onapsdk.constants as const


@pytest.mark.integration
def test_vendor_unknown():
    """Integration tests for Vendor."""
    response = requests.post("{}/reset".format(SDC.base_front_url))
    response.raise_for_status()
    vendor = Vendor(name="test")
    vendor.create()
    assert vendor.created()
    vendor.submit()
    assert vendor.status == const.CERTIFIED

@pytest.mark.integration
def test_vendor_onboard_unknown():
    """Integration tests for Vendor."""
    response = requests.post("{}/reset".format(SDC.base_front_url))
    response.raise_for_status()
    vendor = Vendor(name="test")
    vendor.onboard()
    assert vendor.status == const.CERTIFIED
