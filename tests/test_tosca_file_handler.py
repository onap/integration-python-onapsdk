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
import json
import oyaml as yaml
import os
import os.path
import unittest

from onapsdk.exceptions import ValidationError
import onapsdk.utils.tosca_file_handler as tosca_file_handler


__author__ = "Morgan Richomme <morgan.richomme@orange.com>"


class ToscaFileHandlerTestingBase(unittest.TestCase):

    """The super class which testing classes could inherit."""

    logging.disable(logging.CRITICAL)

    _root_path = os.getcwd().rsplit('/onapsdk')[0]
    _foo_path = _root_path +"/tests/data/service-Ubuntu16-template.yml"


    def setUp(self):
        pass

    def test_get_parameter_from_yaml(self):
        with open(self._foo_path) as f:
            model = json.dumps(yaml.safe_load(f))
        param = tosca_file_handler.get_parameter_from_yaml(
            "metadata", model)
        self.assertEqual(param['name'], "ubuntu16")

    def test_get_wrong_parameter_from_yaml(self):
        with open(self._foo_path) as f:
            model = json.dumps(yaml.safe_load(f))
        with self.assertRaises(ValidationError):
            tosca_file_handler.get_parameter_from_yaml(
                "wrong_parameter", model)

    def test_get_parameter_from_wrong_yaml(self):
        with self.assertRaises(FileNotFoundError):
            with open("wrong_path") as f:
                model = json.dumps(yaml.safe_load(f))
                tosca_file_handler.get_parameter_from_yaml(
                    "metadata", model)

    def test_get_random_string_generator(self):
        self.assertEqual(
            len(tosca_file_handler.random_string_generator()), 6)

    def test_get_vf_list_from_tosca_file(self):
        with open(self._foo_path) as f:
            model = json.dumps(yaml.safe_load(f))
        vf_list = tosca_file_handler.get_vf_list_from_tosca_file(model)
        self.assertEqual(vf_list[0], 'ubuntu16_VF')

    def test_get_modules_list_from_tosca_file(self):
        with open(self._foo_path) as f:
            model = json.dumps(yaml.safe_load(f))
        vf_modules = tosca_file_handler.get_modules_list_from_tosca_file(model)
        self.assertEqual(len(vf_modules), 1)

    # def get_vf_list_from_tosca_file_wrong_model(self):
    #     with self.assertRaises(FileNotFoundError):
    #         tosca_file_handler.get_vf_list_from_tosca_file(
    #             self._root_path + "wrong_path")

if __name__ == "__main__":
    # logging must be disabled else it calls time.time()
    # what will break these unit tests.
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
