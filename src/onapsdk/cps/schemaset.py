"""ONAP SDK CPS schemaset module."""
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

from dataclasses import dataclass
from typing import List, Optional, TYPE_CHECKING

from .cps_element import CpsElement

if TYPE_CHECKING:
    from .dataspace import Dataspace  # pylint: disable=cyclic-import


@dataclass
class SchemaSetModuleReference:
    """Schema set module reference dataclass.

    Stores all information about module reference.
    """

    namespace: str
    revision: str
    name: Optional[str] = None


class SchemaSet(CpsElement):
    """Schema set class."""

    def __init__(self,
                 name: str,
                 dataspace: "Dataspace",
                 module_references: Optional[List[SchemaSetModuleReference]] = None) -> None:
        """Initialize schema set class object.

        Args:
            name (str): Schema set name
            dataspace (Dataspace): Dataspace on which schema set was created.
            module_references (Optional[List[SchemaSetModuleReference]], optional):
                List of module references. Defaults to None.
        """
        super().__init__()
        self.name: str = name
        self.dataspace: "Dataspace" = dataspace
        self.module_refences: List[SchemaSetModuleReference] = module_references \
            if module_references else []

    def __repr__(self) -> str:
        """Human readable representation of the object.

        Returns:
            str: Human readable string

        """
        return f"SchemaSet(name={self.name}, dataspace={self.dataspace.name})"

    def delete(self) -> None:
        """Delete schema set."""
        self.send_message(
            "DELETE",
            f"Delete {self.name} schema set",
            f"{self._url}/dataspaces/{self.dataspace.name}/schema-sets/{self.name}",
            auth=self.auth
        )
