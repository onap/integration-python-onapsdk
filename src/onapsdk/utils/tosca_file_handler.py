"""Utils class."""
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
import json
import string
import secrets
from typing import Dict, List

from onapsdk.exceptions import ValidationError

def get_parameter_from_yaml(parameter: str, config_file: str):
    """Get the value of a given parameter in file.yaml.

    Parameter must be given in string format with dots
    Example: general.openstack.image_name

    Args:
        parameter (str):
        config_file (str): configuration yaml file formtatted as string

    Raises:
        ParameterError: parameter not defined

    Returns:
        the value of the parameter

    """
    value = json.loads(config_file)

    # Workaround for the .. within the params in the yaml file
    ugly_param = parameter.replace("..", "##")
    for element in ugly_param.split("."):
        value = value.get(element.replace("##", ".."))
        if value is None:
            msg = f"{element} in the {parameter} is not in YAML config file."
            raise ValidationError(msg)

    return value

def get_vf_list_from_tosca_file(model: str) -> List:
    """Get the list of Vfs of a VNF based on the tosca file.

    Args:
        model (str): the model retrieved from the tosca file at Vnf
            instantiation

    Returns:
        list: a list of Vfs

    """
    newlist = []
    node_list = get_parameter_from_yaml(
        "topology_template.node_templates", model)

    for node in node_list:
        value = get_parameter_from_yaml(
            "topology_template.node_templates." + node + ".type",
            model)
        if "org.openecomp.resource.vf" in value:
            print(node, value)
            if node not in newlist:
                search_value = str(node).split(" ", maxsplit=1)[0]
                newlist.append(search_value)
    return newlist

def get_modules_list_from_tosca_file(model: str) -> Dict:
    """Get the list of modules from tosca file.

    Modules are stored on topology_template.groups TOSCA file section.

    Args:
        model (str): the model retrieved from the tosca file at Vnf
            instantiation.

    Returns:
        dict: a list of modules

    """
    return get_parameter_from_yaml(
        "topology_template.groups", model
    )

def random_string_generator(size=6,
                            chars=string.ascii_uppercase + string.digits) -> str:
    """Get a random String for VNF.

    Args:
        size (int): the number of alphanumerical chars for CI
        chars (str): alphanumerical characters (ASCII uppercase and digits)

    Returns:
        str: a sequence of random characters

    """
    return ''.join(secrets.choice(chars) for _ in range(size))
