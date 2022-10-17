#   Copyright 2022 Nokia
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
import pytest
import logging
import os

from onapsdk.dmaap.dmaap import Dmaap

logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))


@pytest.mark.integration
def test_should_get_all_topics_from_dmaap():
    # given

    # when
    response = Dmaap.get_all_topics(basic_auth={'username': 'demo', 'password': 'demo123456!'})

    # then
    assert len(response) == 9
