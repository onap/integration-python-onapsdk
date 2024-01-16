"""SDC user module."""
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
from enum import Enum
from typing import Any, Dict, Iterator
from urllib.parse import urljoin

from onapsdk.exceptions import ResourceNotFound  # type: ignore
from onapsdk.sdc2.sdc import SDCCatalog


class SdcUser(SDCCatalog):  # pylint: disable=too-many-instance-attributes
    """SDC user class."""

    GET_ALL_ENDPOINT = "sdc2/rest/v1/user/users"

    class SdcUserStatus(Enum):  # pylint: disable=too-few-public-methods
        """SDC user status enum."""

        ACTIVE = "ACTIVE"
        INACTIVE = "INACTIVE"

    def __init__(self,  # pylint: disable=too-many-arguments too-many-instance-attributes
                 user_id: str,
                 role: str,
                 email: str,
                 first_name: str,
                 full_name: str,
                 last_login_time: int,
                 last_name: str,
                 status: str) -> None:
        """Initialise SDC user class object.

        Args:
            user_id (str): User ID. Would be used as name as well (as each SDC object has name).
            role (str): User role
            email (str): User email
            first_name (str): User first name
            full_name (str): User full name
            last_login_time (int): User last login timestamp
            last_name (str): User last name
            status (str): User status
        """
        super().__init__(name=user_id)
        self.user_id: str = user_id
        self.role: str = role
        self.email: str = email
        self.first_name: str = first_name
        self.full_name: str = full_name
        self.last_login_time: int = last_login_time
        self.last_name: str = last_name
        self.status: str = status

    @classmethod
    def get_all(cls) -> Iterator["SdcUser"]:
        """Get all users.

        Returns:
            Iterator["SdcUser"]: SDC users iterator

        """
        return (cls.create_from_api_response(response_obj) for
                response_obj in cls.send_message_json(
            "GET",
            f"Get all {cls.__name__}",
            urljoin(cls.base_back_url, cls.GET_ALL_ENDPOINT)
        ))

    @classmethod
    def get_by_user_id(cls, user_id: str) -> "SdcUser":
        """Get an user by it's ID.

        Args:
            user_id (str): ID of user to get

        Raises:
            ResourceNotFound: User with given ID not found

        Returns:
            SdcUser: SDC user with given ID.

        """
        for user in cls.get_all():
            if user.user_id == user_id:
                return user
        raise ResourceNotFound(f"{cls.__name__} with name {user_id} user ID not found")

    @classmethod
    def create_from_api_response(cls, api_response: Dict[str, Any]) -> "SdcUser":
        """Create sdc user using values returned by API.

        Args:
            api_response (Dict[str, Any]): API response values dictionary.

        Returns:
            SdcUser: SDC user created using values from API response.

        """
        return cls(
            user_id=api_response["userId"],
            role=api_response["role"],
            email=api_response["email"],
            first_name=api_response["firstName"],
            full_name=api_response["fullName"],
            last_login_time=api_response["lastLoginTime"],
            last_name=api_response["lastName"],
            status=cls.SdcUserStatus(api_response["status"]),
        )
