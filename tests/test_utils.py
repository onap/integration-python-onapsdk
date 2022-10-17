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
import time

from onapsdk.onap_service import OnapService
from onapsdk.utils.mixins import WaitForFinishMixin
from onapsdk.utils import load_json_file


class TestWaitForFinish(WaitForFinishMixin, OnapService):

    @property
    def completed(self):
        return True

    @property
    def finished(self):
        time.sleep(0.1)
        return True


def test_wait_for_finish_timeout():
    t = TestWaitForFinish()
    with pytest.raises(TimeoutError):
        t.wait_for_finish(timeout=0.01)
    t.wait_for_finish()


def test_load_json_file():
    path_to_event: str = os.path.join(os.getcwd(), "tests/data/utils_load_json_file_test.json")
    test_json: str = load_json_file(path_to_event)
    assert test_json == '{"event": {"test1": "val1"}}'
