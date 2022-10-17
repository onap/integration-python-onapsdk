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
import os

import pytest

import requests

from onapsdk.sdc import SDC
from onapsdk.sdc.vendor import Vendor
from onapsdk.sdc.vsp import Vsp
import onapsdk.constants as const


@pytest.mark.integration
def test_vsp_unknown():
    """Integration tests for Vsp."""
    response = requests.post("{}/reset".format(Vendor.base_front_url))
    response.raise_for_status()
    vendor = Vendor(name="test")
    vendor.onboard()
    vsp = Vsp(name="test")
    vsp.vendor = vendor
    vsp.create()
    assert vsp.identifier is not None
    assert vsp.status == const.DRAFT
    vsp.upload_package(open("{}/ubuntu16.zip".format(
        os.path.dirname(os.path.abspath(__file__))), 'rb'))
    assert vsp.status == const.UPLOADED
    vsp.validate()
    assert vsp.status == const.VALIDATED
    vsp.commit()
    assert vsp.status == const.COMMITED
    vsp.submit()
    assert vsp.status == const.CERTIFIED
    vsp.create_csar()
    assert vsp.csar_uuid is not None

@pytest.mark.integration
def test_vsp_onboard_unknown():
    """Integration tests for Vsp."""
    response = requests.post("{}/reset".format(Vendor.base_front_url))
    response.raise_for_status()
    vendor = Vendor(name="test")
    vendor.onboard()
    vsp = Vsp(name="test", package=open("{}/ubuntu16.zip".format(
        os.path.dirname(os.path.abspath(__file__))), 'rb'))
    vsp.vendor = vendor
    vsp.onboard()
    assert vsp.status == const.CERTIFIED
    assert vsp.csar_uuid is not None
