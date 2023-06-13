#   Copyright 2023 Deutsche Telekom AG
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

from onapsdk.so.catalog_db_adapter import CatalogDbAdapter


SERVICE_RESPONSE = {
    "serviceResources"    : {
        "modelInfo"       : {
                "modelName"          : "test_service",
                "modelUuid"          : "4631a8c6-b432-4a15-a2ef-74d616377371",
                "modelInvariantUuid" : "bb6a88a7-2030-4f66-93c3-b9d713d2f511",
                "modelVersion"       : "1.0"
        },
        "serviceCategory"    : "Network Service",
        "serviceType"        : "",
        "serviceRole"        : "",
        "environmentContext" : "General_Revenue-Bearing",
        "resourceOrder"      : "test_service",
        "workloadContext"    : "Production",
        "serviceVnfs": [

                { "modelInfo"                    : {
                        "modelName"              : "test_service",
                        "modelUuid"              : "d94c326a-bb0f-4896-bc17-69e544f46f82",
                        "modelInvariantUuid"     : "15916c82-46b9-4c39-b9e1-6bd6a2d24e4a",
                        "modelVersion"           : "1.0",
                        "modelCustomizationUuid" : "46680890-2886-45ea-84dd-a3720a4c3e84",
                        "modelInstanceName"      : "test_service 0"
                        },
                "toscaNodeType"            : "org.openecomp.resource.vf.BasicOnboardNxtypj",
                "nfFunction"            : None,
                "nfType"                        : None,
                "nfRole"                        : None,
                "nfNamingCode"          : None,
                "multiStageDesign"         : "false",
                "vnfcInstGroupOrder"       : None,
                "resourceInput"            : "{\"skip_post_instantiation_configuration\":\"true\"}",
                        "vfModules": [
                                {
                                        "modelInfo"               : {
                                                "modelName"              : "TestService..base_ubuntu18..module-0",
                                                "modelUuid"              : "ebee8e31-c892-4260-b82a-082c515dc138",
                                                "modelInvariantUuid"     : "9e650a3e-70f2-4e51-959d-c5dbe12bb614",
                                                "modelVersion"           : "1",
                                                "modelCustomizationUuid" : "63b7dd74-b4bd-4e20-bce7-828e46c16e8d",
                                        },              "isBase"                 : True,
                                        "vfModuleLabel"          : "base_ubuntu18",
                                        "initialCount"           : 1,
                                        "hasVolumeGroup"           : False,
                                }
                        ],
                        "groups": [],
                },
        ],
        "serviceNetworks": [],
        "serviceInfo":

                {               "id"              : 10,
                        "serviceInput"     : "[{\"default\":\"\",\"name\":\"default_software_version\",\"type\":\"string\",\"required\":false}]",
                "serviceProperties"            : "[]",
                        "serviceArtifact": [],
        },
        "serviceProxy": [],
        "serviceAllottedResources": [],
        }
}


SERVICE_VNF_RESPONSE = {
    'serviceVnfs': [
        {
            'modelInfo': {
                'modelName': 'test_vnf_01',
                'modelUuid': 'd2779cc5-fb01-449f-a355-7e5d911dca93',
                'modelInvariantUuid': '027cb696-f68f-47db-9b0e-585ea3eaa512',
                'modelVersion': '1.0',
                'modelCustomizationUuid': 'b8740912-e0fc-426f-af97-7657caf57847',
                'modelInstanceName': 'test_vnf_01 0'
            },
            'toscaNodeType': 'org.openecomp.resource.vf.Mvnr5gCucpVfT003',
            'nfFunction': None,
            'nfType': None,
            'nfRole': None,
            'nfNamingCode': None,
            'multiStageDesign': 'false',
            'vnfcInstGroupOrder': None,
            'resourceInput': None,
            'vfModules': [{'modelInfo':
            {
                'modelName': 'test_vf_01',
                'modelUuid': '153464b8-4f47-4140-8b92-9614c4578d91',
                'modelInvariantUuid': '753deff5-99a2-4154-8c1d-3e956cb96f32',
                'modelVersion': '1',
                'modelCustomizationUuid': '7ca564f3-b908-499c-b086-ae77ad270d8c'
            },
            'isBase': False,
            'vfModuleLabel': 'vf_mod_label',
            'initialCount': 0,
            'hasVolumeGroup': False
            }
        ],
        'groups': []
    }
  ]
}


@mock.patch.object(CatalogDbAdapter, "send_message_json")
def test_get_service_info(mock_send_message_json):
    mock_send_message_json.return_value = SERVICE_RESPONSE

    response = CatalogDbAdapter.get_service_info(service_model_uuid="4631a8c6-b432-4a15-a2ef-74d616377371")
    assert "serviceResources" in response
    assert response['serviceResources']["modelInfo"]["modelName"] == "test_service"


@mock.patch.object(CatalogDbAdapter, "send_message_json")
def test_get_service_vnf_info(mock_send_message_json):
    mock_send_message_json.return_value = SERVICE_VNF_RESPONSE

    response = CatalogDbAdapter.get_service_vnf_info(service_model_uuid="test_id_0")
    assert "serviceVnfs" in response
    assert response['serviceVnfs'][0]["modelInfo"]["modelName"] == "test_vnf_01"
