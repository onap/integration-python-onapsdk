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

from onapsdk.utils.headers_creator import (
    headers_aai_creator,
    headers_sdc_creator,
    headers_sdc_tester,
    headers_sdc_governor,
    headers_sdc_operator,
    headers_sdnc_creator,
    headers_so_creator,
    headers_so_catelog_db_creator,
)

def test_headers_sdc_creator():
    base_header = {}
    sdc_headers_creator = headers_sdc_creator(base_header)
    assert base_header != sdc_headers_creator
    assert sdc_headers_creator["USER_ID"] == "cs0008"
    assert sdc_headers_creator["Authorization"]

def test_headers_sdc_tester():
    base_header = {}
    sdc_headers_tester = headers_sdc_tester(base_header)
    assert base_header != sdc_headers_tester
    assert sdc_headers_tester["USER_ID"] == "jm0007"
    assert sdc_headers_tester["Authorization"]

def test_headers_sdc_governor():
    base_header = {}
    sdc_headers_governor = headers_sdc_governor(base_header)
    assert base_header != sdc_headers_governor
    assert sdc_headers_governor["USER_ID"] == "gv0001"
    assert sdc_headers_governor["Authorization"]

def test_headers_sdc_operator():
    base_header = {}
    sdc_headers_operator = headers_sdc_operator(base_header)
    assert base_header != sdc_headers_operator
    assert sdc_headers_operator["USER_ID"] == "op0001"
    assert sdc_headers_operator["Authorization"]

def test_headers_aai_creator():
    base_header = {}
    aai_headers_creator = headers_aai_creator(base_header)
    assert base_header != aai_headers_creator
    assert aai_headers_creator["x-fromappid"] == "AAI"
    assert aai_headers_creator["authorization"]
    assert aai_headers_creator["x-transactionid"]

def test_headers_so_creator():
    base_header = {}
    so_headers_creator = headers_so_creator(base_header)
    assert base_header != so_headers_creator
    assert so_headers_creator["x-fromappid"] == "AAI"
    assert so_headers_creator["authorization"]
    assert so_headers_creator["x-transactionid"]

def test_headers_so_catelog_db_creator():
    base_header = {}
    so_headers_creator = headers_so_catelog_db_creator(base_header)
    assert base_header != so_headers_creator
    assert so_headers_creator["x-fromappid"] == "AAI"
    assert so_headers_creator["authorization"]
    assert so_headers_creator["x-transactionid"]

def test_headers_sdnc_creator():
    base_header = {}
    so_headers_creator = headers_sdnc_creator(base_header)
    assert base_header != so_headers_creator
    assert so_headers_creator["x-fromappid"] == "API client"
    assert so_headers_creator["authorization"]
    assert so_headers_creator["x-transactionid"]
