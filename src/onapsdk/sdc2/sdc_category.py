"""SDC category module."""
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
#   limitations under the License.from onapsdk.sdc2.sdc import ResoureTypeEnum
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urljoin

from onapsdk.exceptions import ResourceNotFound  # type: ignore
from onapsdk.sdc2.sdc import SDCCatalog


@dataclass
class SdcSubCategory:
    """SDC subcategory dataclass."""

    name: str
    normalized_name: str
    unique_id: str


class SdcCategory(SDCCatalog, ABC):  # pylint: disable=too-many-instance-attributes
    """SDC category class."""

    def __init__(self,  # pylint: disable=too-many-arguments
                 name: str,
                 empty: bool,
                 icons: List[str],
                 models: List[str],
                 normalized_name: str,
                 unique_id: str,
                 use_service_substitution_for_nested_services: bool,
                 owner_id: Optional[str] = None,
                 subcategories: Optional[List[SdcSubCategory]] = None,
                 category_type: Optional[str] = None,
                 version: Optional[str] = None,
                 display_name: Optional[str] = None) -> None:
        """Initialise SDC category object.

        Args:
            empty (bool): Falg to determine if category is empty.
            icons (List[str]): List of icons.
            models (List[str]): List of models.
            normalized_name (str): Category normalized name
            unique_id (str): Category unique ID
            use_service_substitution_for_nested_services (bool): Use service substitution
                for nested services
            owner_id (Optional[str], optional): Owner ID. Defaults to None.
            subcategories (Optional[List[SdcSubCategory]], optional): Optional subcategories list.
                Defaults to None.
            category_type (Optional[str], optional): Category type. Defaults to None.
            version (Optional[str], optional): Version. Defaults to None.
            display_name (Optional[str], optional): Display name. Defaults to None.
        """
        super().__init__(name)
        self.empty: bool = empty
        self.icons: List[str] = icons
        self.models: List[str] = models
        self.normalized_name: str = normalized_name
        self.unique_id: str = unique_id
        self.use_service_substitution_for_nested_services: bool = \
            use_service_substitution_for_nested_services
        self.owner_id: Optional[str] = owner_id
        self.subcategories: Optional[List[SdcSubCategory]] = subcategories
        self.category_type: Optional[str] = category_type
        self.version: Optional[str] = version
        self.display_name: Optional[str] = display_name

    def __repr__(self) -> str:
        """SDC resource description.

        Returns:
            str: SDC resource object description

        """
        return f"{self.__class__.__name__.upper()}(name={self.name})"

    @classmethod
    def get_all(cls) -> Iterable["SdcCategory"]:
        """Get all categories objects.

        Yields:
            SdcCategory: SDC category object

        """
        yield from (cls.create_from_api_response(response_obj) \
                    for response_obj in cls.send_message_json(
            "GET",
            f"Get all {cls.__name__}",
            cls.get_all_endpoint()
        ))

    @classmethod
    def get_by_uniqe_id(cls, unique_id: str) -> "SdcCategory":
        """Get category by it's unique ID.

        Args:
            unique_id (str): Unique ID of a category

        Raises:
            ResourceNotFound: Category with given unique ID does not exist.

        Returns:
            SdcCategory: SDC category with given ID

        """
        for category in cls.get_all():
            if category.unique_id == unique_id:
                return category
        raise ResourceNotFound(f"{cls.__name__} with unique id {unique_id} not found")

    @classmethod
    def get_by_name(cls, name: str) -> "SdcCategory":
        """Get category by name.

        Args:
            name (str): Category name

        Raises:
            ResourceNotFound: Category with given name does not exist.

        Returns:
            SdcCategory: SDC category with given name

        """
        for category in cls.get_all():
            if category.name == name:
                return category
        raise ResourceNotFound(f"{cls.__name__} with name {name} not found")

    @classmethod
    def get_all_endpoint(cls) -> str:
        """Get an endpoint which is going to be used to get all categories.

        It's going to be created using `_endpoint_suffix` and common part for all categories

        Returns:
            str: Endpoint to be used to get all categories.

        """
        return urljoin(cls.base_back_url,
                       urljoin("sdc2/rest/v1/categories/",
                               cls._endpoint_suffix()))

    @classmethod
    @abstractmethod
    def _endpoint_suffix(cls) -> str:
        """Category endpoint suffix.

        Abstract classmethod

        Returns:
            str: Category API endpoint suffix.

        """

    @classmethod
    def create_from_api_response(cls, api_response: Dict[str, Any]) -> "SdcCategory":
        """Create category object using an API response dictionary.

        Args:
            api_response (Dict[str, Any]): API response dictionary with values

        Returns:
            SdcCategory: SDC category object

        """
        return cls(
            name=api_response["name"],
            empty=api_response["empty"],
            icons=api_response["icons"],
            models=api_response["models"],
            normalized_name=api_response["normalizedName"],
            unique_id=api_response["uniqueId"],
            use_service_substitution_for_nested_services=\
                api_response["useServiceSubstitutionForNestedServices"],
            owner_id=api_response["ownerId"],
            subcategories=[SdcSubCategory(name=subcategory["name"],
                                          normalized_name=subcategory["normalizedName"],
                                          unique_id=subcategory["uniqueId"]) for subcategory
                                            in api_response["subcategories"]]
                                          if api_response.get("subcategories") else None,
            category_type=api_response["type"],
            version=api_response["version"],
            display_name=api_response["displayName"],
        )

    def get_subcategory(self, subcategory_name: str) -> Optional[SdcSubCategory]:
        """Get category's subcategory by it's name.

        Args:
            subcategory_name (str): Subcategory name

        Returns:
            SdcSubCategory|None: Subcategory object or None if no subcategory
                with given name was found

        """
        if not self.subcategories:
            return None
        for subcategory in self.subcategories:
            if subcategory.name == subcategory_name:
                return subcategory
        return None


class ServiceCategory(SdcCategory):
    """Service category class."""

    @classmethod
    def _endpoint_suffix(cls) -> str:
        """Service category endpoint suffix.

        Returns:
            str: Product category endpoint suffix "services".

        """
        return "services"


class ResourceCategory(SdcCategory):
    """Resource category class."""

    @classmethod
    def _endpoint_suffix(cls) -> str:
        """Resource category endpoint suffix.

        Returns:
            str: Product category endpoint suffix "resources".

        """
        return "resources"


class ProductCategory(SdcCategory):
    """Product category class."""

    @classmethod
    def _endpoint_suffix(cls) -> str:
        """Product category endpoint suffix.

        Returns:
            str: Product category endpoint suffix "products".

        """
        return "products"
