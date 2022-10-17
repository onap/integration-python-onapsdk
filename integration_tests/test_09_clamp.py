"""Integration test Clamp module."""
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

from onapsdk.sdc.service import Service
from onapsdk.clamp.clamp_element import Clamp
from onapsdk.clamp.loop_instance import LoopInstance

@pytest.mark.integration
def test_Clamp_requirements():
    """Integration tests for Clamp."""
    requests.get("{}/reset".format(Clamp._base_url))
    # no add resource in clamp
    # svc already exists in mock clamp
    Clamp()
    svc = Service(name="service01")
    template_exists = Clamp.check_loop_template(service=svc)
    assert template_exists
    policy_exists = Clamp.check_policies(policy_name="MinMax",
                                         req_policies=2)
    assert policy_exists

@pytest.mark.integration
def test_Loop_creation():
    """Integration tests for Loop Instance."""
    requests.get("{}/reset".format(Clamp._base_url))
    Clamp()
    svc = Service(name="service01")
    loop_template = Clamp.check_loop_template(service=svc)
    response = requests.post("{}/reset".format(Clamp._base_url))
    response.raise_for_status()
    loop = LoopInstance(template=loop_template, name="instance01", details={})
    loop.create()

@pytest.mark.integration
def test_Loop_customization():
    """Integration tests for Loop Instance."""
    requests.get("{}/reset".format(Clamp._base_url))
    Clamp()
    svc = Service(name="service01")
    loop_template = Clamp.check_loop_template(service=svc)
    response = requests.post("{}/reset".format(Clamp._base_url))
    response.raise_for_status()
    loop = LoopInstance(template=loop_template, name="instance01", details={})
    loop.create()
    loop.update_microservice_policy()
    #add op policy FrequencyLimiter that already exists in clamp
    loop.add_operational_policy(policy_type="onap.policies.controlloop.guard.common.FrequencyLimiter",
                                policy_version="1.0.0")
    #only frequency configuration is available in mock clamp
    loop.add_op_policy_config(loop.add_frequency_limiter, limit=1)
    submit = loop.act_on_loop_policy(loop.submit)
    assert submit
    stop = loop.act_on_loop_policy(loop.stop)
    assert stop
    restart = loop.act_on_loop_policy(loop.restart)
    assert restart
    deploy = loop.deploy_microservice_to_dcae()
    assert deploy
    loop.undeploy_microservice_from_dcae()
    new_details = loop._update_loop_details()
    assert new_details["components"]["DCAE"]["componentState"]["stateName"] == "MICROSERVICE_UNINSTALLED_SUCCESSFULLY"
