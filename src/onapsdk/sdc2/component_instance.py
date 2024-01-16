"""Component instance module."""
#   Copyright 2024 Deutsche Telekom AG
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
from typing import TYPE_CHECKING, Any, Dict, Optional, Iterable
from urllib.parse import urljoin

from onapsdk.sdc2.sdc import SDC
from onapsdk.utils.jinja import jinja_env  # type: ignore

if TYPE_CHECKING:
    from onapsdk.sdc2.sdc_resource import SDCResource


class ComponentInstanceInput(SDC):  # pylint: disable=too-many-instance-attributes
    """Component instance input class."""

    SET_INPUT_VALUE_TEMPLATE = "sdc2_component_instance_input_set_value.json.j2"

    def __init__(self,  # pylint: disable=too-many-locals too-many-arguments
                 component_instance: "ComponentInstance",
                 definition: bool,
                 hidden: bool,
                 unique_id: str,
                 input_type: str,
                 required: bool,
                 password: bool,
                 name: str,
                 immutable: bool,
                 mapped_to_component_property: bool,
                 is_declared_list_input: bool,
                 user_created: bool,
                 get_input_property: bool,
                 empty: bool,
                 label: Optional[str] = None,
                 description: Optional[str] = None,
                 value: Optional[Any] = None) -> None:
        """Component instance input initialisation.

        Args:
            component_instance (ComponentInstance): Component instance
            definition (bool): Input definiton
            hidden (bool): Flag which determines if input is hidden
            unique_id (str): Input unique ID
            input_type (str): Input type
            required (bool): Flag which determies if input is required
            password (bool): Flag which determines if input is password type
            name (str): Input's name
            immutable (bool): Flag which determines if input is immutable
            mapped_to_component_property (bool): Flag which determines if input is
                mapped to component property
            is_declared_list_input (bool): Flag which determines if input is declared list
            user_created (bool): Flag which determines if was created by user
            get_input_property (bool): Flag which determines if it's get input property
            empty (bool): Flag which determines if input is empty
            label (Optional[str], optional): Input's label. Defaults to None.
            description (Optional[str], optional): Input's description. Defaults to None.
            value (Optional[Any], optional): Input's value. Defaults to None.

        """
        super().__init__(name=name)
        self.component_instance: "ComponentInstance" = component_instance
        self.definition: bool = definition
        self.hidden: bool = hidden
        self.unique_id: str = unique_id
        self.input_type: str = input_type
        self.required: bool = required
        self.password: bool = password
        self.immutable: bool = immutable
        self.mapped_to_component_property: bool = mapped_to_component_property
        self.is_declared_list_input: bool = is_declared_list_input
        self.user_created: bool = user_created
        self.get_input_property: bool = get_input_property
        self.empty: bool = empty
        self.description: Optional[str] = description
        self.label: Optional[str] = label
        self._value: Optional[Any] = value

    @classmethod
    def create_from_api_response(cls,
                                 api_response: Dict[str, Any],
                                 component_instance: "ComponentInstance"
    ) -> "ComponentInstanceInput":
        """Create instance input using values dict returned by SDC API.

        Args:
            api_response (Dict[str, Any]): Values dictionary
            component_instance (ComponentInstance): Component instance related with an input

        Returns:
            ComponentInstanceInput: Component instance input object

        """
        return cls(
            component_instance=component_instance,
            definition=api_response["definition"],
            hidden=api_response["hidden"],
            unique_id=api_response["uniqueId"],
            input_type=api_response["type"],
            required=api_response["required"],
            password=api_response["password"],
            name=api_response["name"],
            immutable=api_response["immutable"],
            mapped_to_component_property=api_response["mappedToComponentProperty"],
            is_declared_list_input=api_response["isDeclaredListInput"],
            user_created=api_response["userCreated"],
            get_input_property=api_response["getInputProperty"],
            empty=api_response["empty"],
            value=api_response.get("value"),
            label=api_response.get("label"),
            description=api_response.get("description")
        )

    @property
    def value(self) -> Optional[Any]:
        """Component instance input value.

        Returns:
            Optional[Any]: Value (if any) of input

        """
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        """Component instance's input value setter.

        Call an API to set a value of component instances' input

        Args:
            value (Any): Any value which is going to be set

        """
        self.send_message_json(
            "POST",
            f"Set value of {self.component_instance.sdc_resource.name} resource input {self.name}",
            urljoin(self.base_back_url,
                    (f"sdc2/rest/v1/catalog/{self.component_instance.sdc_resource.catalog_type()}/"
                     f"{self.component_instance.sdc_resource.unique_id}/resourceInstance/"
                     f"{self.component_instance.unique_id}/inputs")),
            data=jinja_env().get_template(self.SET_INPUT_VALUE_TEMPLATE).render(
                component_instance_input=self,
                value=value
            )
        )
        self._value = value


class ComponentInstance(SDC):  # pylint: disable=too-many-instance-attributes
    """Component instance class."""

    def __init__(self,  # pylint: disable=too-many-locals too-many-arguments
                 actual_component_uid: str,
                 component_name: str,
                 component_uid: str,
                 component_version: str,
                 creation_time: int,
                 customization_uuid: str,
                 icon: str,
                 invariant_name: str,
                 is_proxy: bool,
                 modification_time: int,
                 name: str,
                 normalized_name: str,
                 origin_type: str,
                 tosca_component_name: str,
                 unique_id: str,
                 sdc_resource: "SDCResource") -> None:
        """Component instance initialise.

        Args:
            actual_component_uid (str): Component actual UID
            component_name (str): Component name
            component_uid (str): Component UID
            component_version (str): Component version
            creation_time (int): Creation timestamp
            customization_uuid (str): Customization UUID
            icon (str): Icon
            invariant_name (str): Invariant name
            is_proxy (bool): Flag determines if component is proxy
            modification_time (int): Modification timestamp
            name (str): Component name
            normalized_name (str): Component normalized name
            origin_type (str): Component origin type
            tosca_component_name (str): Component's TOSCA name
            unique_id (str): Unique ID
            sdc_resource (SDCResource): Components SDC resource

        """
        super().__init__(name=name)
        self.actual_component_uid: str = actual_component_uid
        self.component_name: str = component_name
        self.component_uid: str = component_uid
        self.component_version: str = component_version
        self.creation_time: int = creation_time
        self.customization_uuid: str = customization_uuid
        self.icon: str = icon
        self.invariant_name: str = invariant_name
        self.is_proxy: bool = is_proxy
        self.modification_time: int = modification_time
        self.normalized_name: str = normalized_name
        self.origin_type: str = origin_type
        self.tosca_component_name: str = tosca_component_name
        self.unique_id: str = unique_id
        self.sdc_resource: "SDCResource" = sdc_resource

    @classmethod
    def create_from_api_response(cls,
                                 data: Dict[str, Any],
                                 sdc_resource: "SDCResource") -> "ComponentInstance":
        """Create components insance from API response.

        Args:
            data (Dict[str, Any]): API response values dictionary
            sdc_resource (SDCResource): SDC resource with which component instance is related with

        Returns:
            ComponentInstance: Component instance object

        """
        return cls(
            sdc_resource=sdc_resource,
            actual_component_uid=data["actualComponentUid"],
            component_name=data["componentName"],
            component_uid=data["componentUid"],
            component_version=data["componentVersion"],
            creation_time=data["creationTime"],
            customization_uuid=data["customizationUUID"],
            icon=data["icon"],
            invariant_name=data["invariantName"],
            is_proxy=data["isProxy"],
            modification_time=data["modificationTime"],
            name=data["name"],
            normalized_name=data["normalizedName"],
            origin_type=data["originType"],
            tosca_component_name=data["toscaComponentName"],
            unique_id=data["uniqueId"]
        )

    @property
    def inputs(self) -> Iterable[ComponentInstanceInput]:
        """Component instance's inputs iterator.

        Yields:
            ComponentInstanceInput: Component's instance input object

        """
        for input_data in self.send_message_json(
            "GET",
            "Get inputs",
            urljoin(self.base_back_url,
                    (f"sdc2/rest/v1/catalog/{self.sdc_resource.catalog_type()}/"
                     f"{self.sdc_resource.unique_id}/componentInstances/{self.unique_id}/"
                     f"{self.actual_component_uid}/inputs"))
        ):
            yield ComponentInstanceInput.create_from_api_response(input_data, self)

    def get_input_by_name(self, input_name: str) -> Optional[ComponentInstanceInput]:
        """Get component's input by it's name.

        Args:
            input_name (str): Input name

        Returns:
            Optional[ComponentInstanceInput]: Input with given name,
                None if no input with given name found

        """
        for component_instance_input in self.inputs:
            if component_instance_input.name == input_name:
                return component_instance_input
        return None
