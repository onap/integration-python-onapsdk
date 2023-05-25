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
from unittest import mock

from onapsdk.aai.business.project import Project


PROJECTS = {
    "project": [
        {
            "project-name": "test-name",
            "resource-version": "1234"
        },
        {
            "project-name": "test-name2",
            "resource-version": "4321"
        }
    ]
}


COUNT = {
    "results":[
        {
            "project":1
        }
    ]
}


@mock.patch("onapsdk.aai.business.project.Project.send_message_json")
def test_project_get_all(mock_send_message_json):
    mock_send_message_json.return_value = {}
    assert len(list(Project.get_all())) == 0

    mock_send_message_json.return_value = PROJECTS
    projects = list(Project.get_all())
    assert len(projects) == 2
    lob1, lob2 = projects
    assert lob1.name == "test-name"
    assert lob1.resource_version == "1234"
    assert lob2.name == "test-name2"
    assert lob2.resource_version == "4321"


@mock.patch("onapsdk.aai.business.project.Project.send_message_json")
def test_project_get_by_name(mock_send):
    Project.get_by_name(name="test-name")
    mock_send.assert_called_once_with("GET",
                                      "Get test-name project",
                                      "https://aai.api.sparky.simpledemo.onap.org:30233/aai/v27/business/projects/project/test-name")


@mock.patch("onapsdk.aai.business.project.Project.send_message")
@mock.patch("onapsdk.aai.business.project.Project.get_by_name")
def test_project_create(_, mock_send):
    Project.create(name="test-name")
    mock_send.assert_called_once_with("PUT",
                                      "Declare A&AI project",
                                      "https://aai.api.sparky.simpledemo.onap.org:30233/aai/v27/business/projects/project/test-name",
                                      data='{\n    "project-name": "test-name"\n}')


@mock.patch("onapsdk.aai.business.project.Project.send_message_json")
def test_project_count(mock_send_message_json):
    mock_send_message_json.return_value = COUNT
    assert Project.count() == 1

def test_project_url():
    project = Project(name="test-project", resource_version="123")
    assert project.name in project.url
