"""Test Jinja module."""
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
from jinja2 import Environment

from onapsdk.utils.jinja import jinja_env

def test_jinja_env():
    """test jinja_env function."""
    test_jinja_env = jinja_env()
    assert isinstance(test_jinja_env, Environment)
    assert 'sdc_element_action.json.j2' in test_jinja_env.list_templates()
    assert 'vendor_create.json.j2' in test_jinja_env.list_templates()
    assert 'vsp_create.json.j2' in test_jinja_env.list_templates()
    assert test_jinja_env.autoescape != None
