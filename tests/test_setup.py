"""Test the snapshot version suffix applied by the PyPI merge job."""
#   Copyright 2026 Deutsche Telekom AG
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

import setup


def test_no_suffix_outside_jenkins():
    """A local build gets the plain version from version.py."""
    assert setup.snapshot_suffix({}) == ""


def test_merge_job_gets_dev_suffix():
    """The merge job publishes a distinct snapshot per build."""
    env = {"JOB_NAME": "integration-python-onapsdk-pypi-merge-master",
           "BUILD_NUMBER": "123"}
    assert setup.snapshot_suffix(env) == ".dev123"


def test_stage_job_keeps_the_release_version():
    """The stage job must publish the version the release job asks PyPI for."""
    env = {"JOB_NAME": "integration-python-onapsdk-pypi-stage-master",
           "BUILD_NUMBER": "7"}
    assert setup.snapshot_suffix(env) == ""


def test_no_suffix_without_a_usable_build_number():
    """`.dev` on its own is not a valid PEP 440 version, so build nothing."""
    env = {"JOB_NAME": "integration-python-onapsdk-pypi-merge-master",
           "BUILD_NUMBER": ""}
    assert setup.snapshot_suffix(env) == ""
