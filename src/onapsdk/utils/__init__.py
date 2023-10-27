"""ONAP SDK utils package."""
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
from datetime import datetime


def get_zulu_time_isoformat() -> str:
    """Get zulu time in accepted by ONAP modules format.

    Returns:
        str: Actual Zulu time.

    """
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def load_json_file(path_to_json_file: str) -> str:
    """
    Return json as string from selected file.

    Args:
        path_to_json_file: (str) path to file with json
    Returns:
        File content as string (str)
    """
    with open(path_to_json_file, encoding="utf-8") as json_file:
        data = json.load(json_file)
        return json.dumps(data)
