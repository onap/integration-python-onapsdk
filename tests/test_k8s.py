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

from onapsdk.k8s import Definition, ConnectivityInfo, Instance, InstantiationRequest
from onapsdk.k8s import K8sPlugin, Profile, ConfigurationTemplate, Configuration
from onapsdk.k8s import CloudRegion


CONNECTIVITY_INFO = {
    "cloud-region": "test_cloud_region",
    "cloud-owner": "test_cloud_owner",
    "other-connectivity-list": {},
    "kubeconfig": "test_kubeconfig"
}


DEFINITION = {
    "rb-name": "test_rb_name_0",
    "rb-version": "test_rb_version_0"
}


DEFINITIONS = [
    DEFINITION,
    {
        "rb-name": "test_rb_name_1",
        "rb-version": "test_rb_version_1",
        "chart-name": "test_chart_name_1",
        "description": "test_description_1",
        "labels": {}
    }
]


PROFILE = {
    "rb-name": "test_rb_name",
    "rb-version": "test_rb_version",
    "profile-name": "test_profile_name",
    "namespace": "test_namespace",
    "kubernetes-version": "1.19.0",
    "labels": {
        "region": "test"
    },
    "extra-resource-types": [
        {
            "Group": "",
            "Kind": "Pod",
            "Version": "v1"
        }
    ]
}


PROFILES = [
    PROFILE,
    {
        "rb-name": "test_rb_name_1",
        "rb-version": "test_rb_version_1",
        "profile-name": "test_profile_name_1",
        "namespace": "test_namespace_1",
        "kubernetes-version": "1.19.0",
        "labels": {
            "region": "test-new"
        },
        "extra-resource-types": [
            {
                "Group": "",
                "Kind": "Pod",
                "Version": "v1"
            }
        ]
    }
]


CONFIGURATION_TEMPLATE = {
    "template-name": "test_configuration_template_name",
    "description": "test_configuration_template_description"
}


CONFIGURATION_TEMPLATES = [
    CONFIGURATION_TEMPLATE,
    {
        "template-name": "test_configuration_template_name_0"
    }
]


INSTANCE = {
  "id": "ID_GENERATED_BY_K8SPLUGIN",
  "namespace": "NAMESPACE_WHERE_INSTANCE_HAS_BEEN_DEPLOYED_AS_DERIVED_FROM_PROFILE",
  "release-name": "RELEASE_NAME_AS_COMPUTED_BASED_ON_INSTANTIATION_REQUEST_AND_PROFILE_DEFAULT",
  "request": {
    "rb-name": "test-rbdef",
    "rb-version": "v1",
    "profile-name": "p1",
    "release-name": "release-x",
    "cloud-region": "krd",
    "override-values": {
        "optionalDictOfParameters": "andTheirValues, like",
        "global.name": "dummy-name"
    },
    "labels": {
        "optionalLabelForInternalK8spluginInstancesMetadata": "dummy-value"
    },
  },
  "resources": [
        {
            "GVK": {
                "Group": "",
                "Kind": "ConfigMap",
                "Version": "v1"
            },
            "Name": "test-cm"
        },
        {
            "GVK": {
                "Group": "",
                "Kind": "Service",
                "Version": "v1"
            },
            "Name": "test-svc"
        },
        {
            "GVK": {
                "Group": "apps",
                "Kind": "Deployment",
                "Version": "v1"
            },
            "Name": "test-dep"
        }
  ]
}


INSTANCES = [
    INSTANCE
]

STATUS = {
    "request": {
        "rb-name": "apache-7.6.0",
        "rb-version": "test",
        "profile-name": "test-k8s",
        "release-name": "",
        "cloud-region": "test",
        "labels": {},
        "override-values": {
            "global.normal": "value",
            "global.second.last": "value",
            "service.type": "LoadBalancer",
            "vnf_name": "test-vnf-first"
        }
    },
    "ready": False,
    "resourceCount": 1,
    "resourcesStatus": [
        {
            "name": "test-k8s-apache",
            "GVK": {
                "Group": "",
                "Version": "v1",
                "Kind": "Service"
            },
            "status": {
                "apiVersion": "v1",
                "kind": "Service",
                "metadata": {
                    "annotations": {
                        "loadbalancer.openstack.org/load-balancer-id": "4eb4e8e4-d4b7-4dd8-a0df-d2a949513dd4"
                    },
                    "creationTimestamp": "2023-02-27T14:16:59Z",
                    "finalizers": [
                        "service.kubernetes.io/load-balancer-cleanup"
                    ],
                    "labels": {
                        "app.kubernetes.io/instance": "test-k8s",
                        "app.kubernetes.io/managed-by": "Helm",
                        "app.kubernetes.io/name": "apache",
                        "helm.sh/chart": "apache-7.6.0",
                        "k8splugin.io/rb-instance-id": "serene_mcnulty"
                    },
                    "name": "test-k8s-apache",
                    "namespace": "test-k8s",
                    "resourceVersion": "3983718",
                    "uid": "7904a5c5-9732-4581-8ef7-60d5bf5d399b"
                },
                "spec": {
                    "allocateLoadBalancerNodePorts": True,
                    "clusterIP": "10.1.44.85",
                    "clusterIPs": [
                        "10.1.44.85"
                    ],
                    "externalTrafficPolicy": "Cluster",
                    "internalTrafficPolicy": "Cluster",
                    "ipFamilies": [
                        "IPv4"
                    ],
                    "ipFamilyPolicy": "SingleStack",
                    "ports": [
                        {
                            "name": "http",
                            "nodePort": 32350,
                            "port": 80,
                            "protocol": "TCP",
                            "targetPort": "http"
                        },
                        {
                            "name": "https",
                            "nodePort": 32514,
                            "port": 443,
                            "protocol": "TCP",
                            "targetPort": "https"
                        }
                    ],
                    "selector": {
                        "app.kubernetes.io/instance": "test-k8s",
                        "app.kubernetes.io/name": "apache"
                    },
                    "sessionAffinity": "None",
                    "type": "LoadBalancer"
                },
                "status": {
                    "loadBalancer": {
                        "ingress": [
                            {
                                "ip": "10.0.0.0"
                            }
                        ]
                    }
                }
            }
        }
    ]
}

REGION_STATUS = {
    "resourceCount": 1,
    "resourcesStatus": STATUS["resourcesStatus"]
}

CONFIG = {
    "config-name": "conf",
    "template-name": "conf",
    "description": "",
    "values": {
        "replicaCount": 2
    },
    "config-version": 1,
    "config-tag": "two-replicas"
}

CONFIG_THREE = {
    "config-name": "conf",
    "template-name": "conf",
    "description": "",
    "values": {
        "replicaCount": 3
    },
    "config-version": 2,
    "config-tag": ""
}

CONFIGS = [
    CONFIG
]

CONFIG_TAGS = [
    {
        "config-version": 1,
        "config-tag": "two-replicas"
    }
]

@mock.patch.object(ConnectivityInfo, "send_message_json")
def test_get_connectivity_info_by_region_id(mock_send_message_json):
    mock_send_message_json.return_value = CONNECTIVITY_INFO
    conn_info: ConnectivityInfo = ConnectivityInfo.get_connectivity_info_by_region_id("test_cloud_region")
    assert conn_info.cloud_region_id == "test_cloud_region"
    assert conn_info.cloud_owner == "test_cloud_owner"
    assert conn_info.other_connectivity_list == {}
    assert conn_info.kubeconfig == "test_kubeconfig"


@mock.patch.object(ConnectivityInfo, "send_message")
@mock.patch.object(ConnectivityInfo, "send_message_json")
def test_connectivity_info_create_delete(mock_send_message_json, mock_send_message):
    mock_send_message_json.return_value = CONNECTIVITY_INFO
    conn_info: ConnectivityInfo = ConnectivityInfo.create("test_cloud_region", "test_cloud_owner", b"kubeconfig")
    assert conn_info.cloud_region_id == "test_cloud_region"
    assert conn_info.cloud_owner == "test_cloud_owner"
    assert conn_info.other_connectivity_list == {}
    assert conn_info.kubeconfig == "test_kubeconfig"
    assert conn_info.url == f"{K8sPlugin.base_url_and_version()}/connectivity-info/test_cloud_region"
    conn_info.delete()


@mock.patch.object(ConnectivityInfo, "send_message_json")
def test_get_cloud_region_by_region_id(mock_send_message_json):
    mock_send_message_json.return_value = CONNECTIVITY_INFO
    cloud_region: CloudRegion = CloudRegion.get_by_region_id("test_cloud_region")
    assert cloud_region.cloud_region_id == "test_cloud_region"
    assert cloud_region.connectivity_info.cloud_owner == "test_cloud_owner"
    assert cloud_region.connectivity_info.other_connectivity_list == {}
    assert cloud_region.connectivity_info.kubeconfig == "test_kubeconfig"


@mock.patch.object(ConnectivityInfo, "send_message")
@mock.patch.object(ConnectivityInfo, "send_message_json")
def test_cloud_region_create_delete(mock_send_message_json, mock_send_message):
    mock_send_message_json.return_value = CONNECTIVITY_INFO
    cloud_region: CloudRegion = CloudRegion.create("test_cloud_region", "test_cloud_owner", b"kubeconfig")
    assert cloud_region.cloud_region_id == "test_cloud_region"
    assert cloud_region.connectivity_info.cloud_owner == "test_cloud_owner"
    assert cloud_region.connectivity_info.other_connectivity_list == {}
    assert cloud_region.connectivity_info.kubeconfig == "test_kubeconfig"
    assert cloud_region.connectivity_info.url == f"{K8sPlugin.base_url_and_version()}/connectivity-info/test_cloud_region"
    cloud_region.delete()


@mock.patch.object(CloudRegion, "send_message_json")
def test_region_query_resources(mock_send_message_json):
    mock_send_message_json.return_value = REGION_STATUS
    region = CloudRegion(
        "test_cloud_region",
        None
    )
    status = region.query_resources("Service", "v1", "default", "name", {"label_one": "two"})
    assert status.resource_count == 1
    assert status.resources_status[0].name == "test-k8s-apache"
    assert status.resources_status[0].gvk.kind == "Service"
    assert status.resources_status[0].gvk.version == "v1"


@mock.patch.object(Definition, "send_message_json")
def test_definition_get_all(mock_send_message_json):
    mock_send_message_json.return_value = []
    assert len(list(Definition.get_all())) == 0

    mock_send_message_json.return_value = DEFINITIONS
    definitions = list(Definition.get_all())
    assert len(definitions) == 2

    def_0, def_1 = definitions
    assert def_0.rb_name == "test_rb_name_0"
    assert def_0.rb_version == "test_rb_version_0"
    assert def_0.chart_name is None
    assert def_0.description is None
    assert def_0.labels is None

    assert def_1.rb_name == "test_rb_name_1"
    assert def_1.rb_version == "test_rb_version_1"
    assert def_1.chart_name == "test_chart_name_1"
    assert def_1.description == "test_description_1"
    assert def_1.labels == {}


@mock.patch.object(Definition, "send_message_json")
def test_get_definition_by_name_version(mock_send_message_json):
    mock_send_message_json.return_value = DEFINITION
    def_0 = Definition.get_definition_by_name_version("rb_name", "rb_version")
    assert def_0.rb_name == "test_rb_name_0"
    assert def_0.rb_version == "test_rb_version_0"
    assert def_0.chart_name is None
    assert def_0.description is None
    assert def_0.labels is None


@mock.patch.object(Definition, "send_message_json")
@mock.patch.object(Definition, "send_message")
def test_create_delete_definition(mock_send_message, mock_send_message_json):
    mock_send_message_json.return_value = DEFINITION
    def_0 = Definition.create(
        rb_name="test_rb_name_0",
        rb_version="test_rb_version_0"
    )
    assert def_0.rb_name == "test_rb_name_0"
    assert def_0.rb_version == "test_rb_version_0"
    assert def_0.chart_name is None
    assert def_0.description is None
    assert def_0.labels is None
    assert def_0.url == f"{K8sPlugin.base_url_and_version()}/rb/definition/test_rb_name_0/test_rb_version_0"
    def_0.delete()


@mock.patch.object(Definition, "send_message_json")
@mock.patch.object(Definition, "send_message")
def test_update_definition(mock_send_message, mock_send_message_json):
    mock_send_message_json.return_value = DEFINITION
    def_0 = Definition(
        rb_name="test_rb_name_0",
        rb_version="test_rb_version_0",
        chart_name=None,
        description=None,
        labels=None
    )
    def_0 = def_0.update()
    assert def_0.rb_name == "test_rb_name_0"
    assert def_0.rb_version == "test_rb_version_0"
    assert def_0.chart_name is None
    assert def_0.description is None
    assert def_0.labels is None
    assert def_0.url == f"{K8sPlugin.base_url_and_version()}/rb/definition/test_rb_name_0/test_rb_version_0"



@mock.patch.object(Definition, "send_message_json")
@mock.patch.object(Definition, "send_message")
@mock.patch.object(Profile, "send_message")
def test_definition_create_delete_profile(mock_send_message_profile, mock_send_message, mock_send_message_json):
    mock_send_message_json.return_value = PROFILE
    deff = Definition(
        rb_name="test_rb_name",
        rb_version="test_rb_version",
        chart_name="test_chart_name",
        description="test_description",
        labels={}
    )
    profile = deff.create_profile(
        profile_name="test_profile_name",
        namespace="test_namespace",
        kubernetes_version="1.19.0",
        labels={
            "region": "test"
        },
        extra_resource_types=[{
            "Group": "",
            "Version": "v1",
            "Kind": "Pod"
        }]
    )
    assert profile.rb_name == "test_rb_name"
    assert profile.rb_version == "test_rb_version"
    assert profile.profile_name == "test_profile_name"
    assert profile.namespace == "test_namespace"
    assert profile.kubernetes_version == "1.19.0"
    assert profile.labels == {
        "region": "test"
    }
    assert profile.extra_resource_types[0].kind == "Pod"
    assert profile.extra_resource_types[0].version == "v1"
    assert profile.release_name == "test_profile_name"
    assert profile.url == f"{deff.url}/profile/test_profile_name"
    profile.delete()


@mock.patch.object(Profile, "send_message_json")
def test_definition_update_profile(mock_send_message_json):
    mock_send_message_json.return_value = PROFILE
    old_profile = Profile(
        rb_name="test_rb_name",
        rb_version="test_rb_version",
        profile_name="test_profile_name",
        namespace="test_namespace",
        labels={
            "region": "test"
        },
        kubernetes_version="1.19.0"
    )
    profile = old_profile.update()
    assert profile.rb_name == "test_rb_name"
    assert profile.rb_version == "test_rb_version"
    assert profile.profile_name == "test_profile_name"
    assert profile.namespace == "test_namespace"
    assert profile.kubernetes_version == "1.19.0"
    assert profile.labels == {
        "region": "test"
    }
    assert profile.release_name == "test_profile_name"
    assert profile.url == old_profile.url


@mock.patch.object(Definition, "send_message_json")
def test_definition_get_profile_by_name(mock_send_message_json):
    mock_send_message_json.return_value = PROFILE
    deff = Definition(
        rb_name="test_rb_name",
        rb_version="test_rb_version",
        chart_name="test_chart_name",
        description="test_description",
        labels={}
    )
    profile = deff.get_profile_by_name("test_profile_name")
    assert profile.rb_name == "test_rb_name"
    assert profile.rb_version == "test_rb_version"
    assert profile.profile_name == "test_profile_name"
    assert profile.namespace == "test_namespace"
    assert profile.kubernetes_version == "1.19.0"
    assert profile.labels == {
        "region": "test"
    }
    assert profile.release_name == "test_profile_name"


@mock.patch.object(Definition, "send_message_json")
def test_definition_get_all_profiles(mock_send_message_json):
    mock_send_message_json.return_value = []
    deff = Definition(
        rb_name="test_rb_name",
        rb_version="test_rb_version",
        chart_name="test_chart_name",
        description="test_description",
        labels={}
    )
    assert len(list(deff.get_all_profiles())) == 0

    mock_send_message_json.return_value = PROFILES
    profiles = list(deff.get_all_profiles())
    assert len(profiles) == 2
    prof_0, prof_1 = profiles

    assert prof_0.rb_name == "test_rb_name"
    assert prof_0.rb_version == "test_rb_version"
    assert prof_0.profile_name == "test_profile_name"
    assert prof_0.namespace == "test_namespace"
    assert prof_0.kubernetes_version == "1.19.0"
    assert prof_0.labels == {
        "region": "test"
    }
    assert prof_0.release_name == "test_profile_name"

    assert prof_1.rb_name == "test_rb_name_1"
    assert prof_1.rb_version == "test_rb_version_1"
    assert prof_1.profile_name == "test_profile_name_1"
    assert prof_1.namespace == "test_namespace_1"
    assert prof_1.kubernetes_version == "1.19.0"
    assert prof_1.labels == {
        "region": "test-new"
    }
    assert prof_1.release_name == "test_profile_name_1"


@mock.patch.object(Definition, "send_message_json")
def test_definition_get_configuration_template_by_name(mock_send_message_json):
    mock_send_message_json.return_value = CONFIGURATION_TEMPLATE
    deff = Definition(
        rb_name="test_rb_name",
        rb_version="test_rb_version",
        chart_name="test_chart_name",
        description="test_description",
        labels={}
    )
    configuration_tmpl = deff.get_configuration_template_by_name(
        template_name="test_configuration_template_name"
    )
    assert configuration_tmpl.rb_name == deff.rb_name
    assert configuration_tmpl.rb_version == deff.rb_version
    assert configuration_tmpl.template_name == "test_configuration_template_name"
    assert configuration_tmpl.description == "test_configuration_template_description"


@mock.patch.object(Definition, "send_message_json")
@mock.patch.object(Definition, "send_message")
@mock.patch.object(ConfigurationTemplate, "send_message")
def test_definition_create_delete_configuration_template(mock_send_message_config, mock_send_message, mock_send_message_json):
    mock_send_message_json.return_value = CONFIGURATION_TEMPLATE
    deff = Definition(
        rb_name="test_rb_name",
        rb_version="test_rb_version",
        chart_name="test_chart_name",
        description="test_description",
        labels={}
    )
    configuration_tmpl = deff.create_configuration_template(
        template_name="test_configuration_template_name",
        description="test_configuration_template_description"
    )
    assert configuration_tmpl.rb_name == deff.rb_name
    assert configuration_tmpl.rb_version == deff.rb_version
    assert configuration_tmpl.template_name == "test_configuration_template_name"
    assert configuration_tmpl.description == "test_configuration_template_description"
    assert configuration_tmpl.url == f"{deff.url}/config-template/test_configuration_template_name"
    configuration_tmpl.delete()


@mock.patch.object(ConfigurationTemplate, "send_message_json")
def test_definition_update_configuration_template(mock_send_message_json):
    mock_send_message_json.return_value = CONFIGURATION_TEMPLATE
    old_configuration_template = ConfigurationTemplate(
        rb_name="test_rb_name",
        rb_version="test_rb_version",
        template_name="test_configuration_template_name",
        description="test_configuration_template_description"
    )
    configuration_tmpl = old_configuration_template.update()
    assert configuration_tmpl.rb_name == old_configuration_template.rb_name
    assert configuration_tmpl.rb_version == old_configuration_template.rb_version
    assert configuration_tmpl.template_name == old_configuration_template.template_name
    assert configuration_tmpl.description == old_configuration_template.description
    assert configuration_tmpl.url == old_configuration_template.url


@mock.patch.object(Definition, "send_message_json")
def test_definition_get_all_configuration_templates(mock_send_message_json):
    mock_send_message_json.return_value = []
    deff = Definition(
        rb_name="test_rb_name",
        rb_version="test_rb_version",
        chart_name="test_chart_name",
        description="test_description",
        labels={}
    )
    assert len(list(deff.get_all_configuration_templates())) == 0

    mock_send_message_json.return_value = CONFIGURATION_TEMPLATES
    configuration_tmplts = list(deff.get_all_configuration_templates())
    assert len(configuration_tmplts) == 2

    tmpl_0, tmpl_1 = configuration_tmplts
    assert tmpl_0.rb_name == deff.rb_name
    assert tmpl_0.rb_version == deff.rb_version
    assert tmpl_0.template_name == "test_configuration_template_name"
    assert tmpl_0.description == "test_configuration_template_description"

    assert tmpl_1.rb_name == deff.rb_name
    assert tmpl_1.rb_version == deff.rb_version
    assert tmpl_1.template_name == "test_configuration_template_name_0"
    assert tmpl_1.description is None


@mock.patch.object(Instance, "send_message_json")
def test_instance_get_all(mock_send_message_json):
    mock_send_message_json.return_value = []
    assert len(list(Instance.get_all())) == 0

    mock_send_message_json.return_value = INSTANCES
    assert len(list(Instance.get_all())) == 1


@mock.patch.object(Instance, "send_message_json")
@mock.patch.object(Instance, "send_message")
def test_instance_create_delete(mock_send_message, mock_send_message_json):
    mock_send_message_json.return_value = INSTANCE
    instance = Instance.create(
        "test_cloud_region_id",
        "test_profile_name",
        "test_rb_name",
        "test_rb_version"
    )
    assert instance.instance_id == "ID_GENERATED_BY_K8SPLUGIN"
    assert instance.namespace == "NAMESPACE_WHERE_INSTANCE_HAS_BEEN_DEPLOYED_AS_DERIVED_FROM_PROFILE"
    assert instance.url == f"{K8sPlugin.base_url_and_version()}/instance/ID_GENERATED_BY_K8SPLUGIN"
    instance.delete()


@mock.patch.object(Instance, "send_message_json")
def test_instance_upgrade(mock_send_message_json):
    mock_send_message_json.return_value = INSTANCE
    old_instance = Instance(
        "ID_GENERATED_BY_K8SPLUGIN",
        "test-k8s",
        STATUS["request"]
    )
    instance = old_instance.upgrade(
        "test_cloud_region_id",
        "test_profile_name",
        "test_rb_name",
        "test_rb_version"
    )
    assert instance.instance_id == "ID_GENERATED_BY_K8SPLUGIN"
    assert instance.namespace == "NAMESPACE_WHERE_INSTANCE_HAS_BEEN_DEPLOYED_AS_DERIVED_FROM_PROFILE"
    assert instance.url == f"{K8sPlugin.base_url_and_version()}/instance/ID_GENERATED_BY_K8SPLUGIN"


@mock.patch.object(Instance, "send_message_json")
def test_instance_get_by_id(mock_send_message_json):
    mock_send_message_json.return_value = INSTANCE
    instance = Instance.get_by_id("ID_GENERATED_BY_K8SPLUGIN")
    assert instance.instance_id == "ID_GENERATED_BY_K8SPLUGIN"
    assert instance.namespace == "NAMESPACE_WHERE_INSTANCE_HAS_BEEN_DEPLOYED_AS_DERIVED_FROM_PROFILE"


@mock.patch.object(Instance, "send_message_json")
def test_instance_get_status(mock_send_message_json):
    mock_send_message_json.return_value = STATUS
    instance = Instance(
        "ID_GENERATED_BY_K8SPLUGIN",
        "test-k8s",
        STATUS["request"]
    )
    status = instance.get_status()
    assert status.instance_id == "ID_GENERATED_BY_K8SPLUGIN"
    assert status.resource_count == 1
    assert status.ready == False
    assert status.request.rb_name == "apache-7.6.0"
    assert status.request.rb_version == "test"
    assert status.request.profile_name == "test-k8s"
    assert status.resources_status[0].name == "test-k8s-apache"
    assert status.resources_status[0].gvk.kind == "Service"
    assert status.resources_status[0].gvk.version == "v1"


@mock.patch.object(Instance, "send_message_json")
def test_instance_query_status(mock_send_message_json):
    mock_send_message_json.return_value = STATUS
    instance = Instance(
        "ID_GENERATED_BY_K8SPLUGIN",
        "default",
        InstantiationRequest(STATUS["request"])
    )
    status = instance.query_status("Service", "v1")
    assert status.instance_id == "ID_GENERATED_BY_K8SPLUGIN"
    assert status.resource_count == 1
    assert status.ready == False
    assert status.request.rb_name == "apache-7.6.0"
    assert status.request.rb_version == "test"
    assert status.request.profile_name == "test-k8s"
    assert status.resources_status[0].name == "test-k8s-apache"
    assert status.resources_status[0].gvk.kind == "Service"
    assert status.resources_status[0].gvk.version == "v1"


@mock.patch.object(Instance, "send_message_json")
@mock.patch.object(Instance, "send_message")
@mock.patch.object(Configuration, "send_message")
def test_instance_create_delete_configuration(mock_send_message_delete, mock_send_message, mock_send_message_json):
    mock_send_message_json.return_value = CONFIG
    instance = Instance(
        "ID_GENERATED_BY_K8SPLUGIN",
        "default",
        InstantiationRequest(STATUS["request"])
    )
    config = instance.create_configuration("conf", "conf", {"replicaCount": 2})
    assert config.name == "conf"
    assert config.template_name == "conf"
    assert config.config_version == "1"
    config.delete()


@mock.patch.object(Instance, "send_message_json")
def test_instance_get_configuration_by_name(mock_send_message_json):
    mock_send_message_json.return_value = CONFIG
    instance = Instance(
        "ID_GENERATED_BY_K8SPLUGIN",
        "default",
        InstantiationRequest(STATUS["request"])
    )
    config = instance.get_configuration_by_name("conf")
    assert config.instance_id == "ID_GENERATED_BY_K8SPLUGIN"
    assert config.name == "conf"
    assert config.template_name == "conf"
    assert config.config_version == "1"
    assert config.config_tag == "two-replicas"


@mock.patch.object(Instance, "send_message_json")
def test_instance_get_all_configurations(mock_send_message_json):
    mock_send_message_json.return_value = CONFIGS
    instance = Instance(
        "ID_GENERATED_BY_K8SPLUGIN",
        "default",
        InstantiationRequest(STATUS["request"])
    )
    configs = instance.get_all_configurations()
    for conf in configs:
        assert conf.instance_id == "ID_GENERATED_BY_K8SPLUGIN"
        assert conf.name == "conf"
        assert conf.template_name == "conf"
        assert conf.config_version == "1"
        assert conf.config_tag == "two-replicas"


@mock.patch.object(Configuration, "send_message_json")
def test_instance_config_get_all_versions(mock_send_message_json):
    mock_send_message_json.return_value = CONFIGS
    config = Configuration(
        instance_id="ID_GENERATED_BY_K8SPLUGIN",
        config_name="conf",
        template_name="conf",
        description="",
        config_version="1",
        config_tag="two-replicas",
        values={
            "replicaCount": 2
        }
    )
    configs = config.get_config_versions()
    for conf in configs:
        assert conf.instance_id == "ID_GENERATED_BY_K8SPLUGIN"
        assert conf.name == "conf"
        assert conf.template_name == "conf"
        assert conf.config_version == "1"
        assert conf.config_tag == "two-replicas"


@mock.patch.object(Configuration, "send_message_json")
def test_instance_config_get_by_version(mock_send_message_json):
    mock_send_message_json.return_value = CONFIG
    config = Configuration(
        instance_id="ID_GENERATED_BY_K8SPLUGIN",
        config_name="conf",
        template_name="conf",
        description="",
        config_version="1",
        config_tag="two-replicas",
        values={
            "replicaCount": 2
        }
    )
    conf = config.get_config_by_version("1")
    assert conf.instance_id == "ID_GENERATED_BY_K8SPLUGIN"
    assert conf.name == "conf"
    assert conf.template_name == "conf"
    assert conf.config_version == "1"
    assert conf.config_tag == "two-replicas"


@mock.patch.object(Configuration, "send_message_json")
def test_instance_config_get_all_tags(mock_send_message_json):
    mock_send_message_json.return_value = CONFIG_TAGS
    config = Configuration(
        instance_id="ID_GENERATED_BY_K8SPLUGIN",
        config_name="conf",
        template_name="conf",
        description="",
        config_version="1",
        config_tag="two-replicas",
        values={
            "replicaCount": 2
        }
    )
    configs = config.get_config_tags()
    for tag in configs:
        assert tag.config_tag == "two-replicas"
        assert tag.config_version == "1"


@mock.patch.object(Configuration, "send_message_json")
def test_instance_config_get_by_tag(mock_send_message_json):
    mock_send_message_json.return_value = CONFIG
    config = Configuration(
        instance_id="ID_GENERATED_BY_K8SPLUGIN",
        config_name="conf",
        template_name="conf",
        description="",
        config_version="1",
        config_tag="two-replicas",
        values={
            "replicaCount": 2
        }
    )
    conf = config.get_config_by_tag("two-replicas")
    assert conf.instance_id == "ID_GENERATED_BY_K8SPLUGIN"
    assert conf.name == "conf"
    assert conf.template_name == "conf"
    assert conf.config_version == "1"
    assert conf.config_tag == "two-replicas"


@mock.patch.object(Configuration, "send_message")
def test_instance_config_tag_version(mock_send_message):
    config = Configuration(
        instance_id="ID_GENERATED_BY_K8SPLUGIN",
        config_name="conf",
        template_name="conf",
        description="",
        config_version="1",
        config_tag="",
        values={
            "replicaCount": 2
        }
    )
    conf = config.tag_config_version("two-replicas")


@mock.patch.object(Configuration, "send_message_json")
def test_instance_config_update(mock_send_message_json):
    mock_send_message_json.return_value = CONFIG_THREE
    config = Configuration(
        instance_id="ID_GENERATED_BY_K8SPLUGIN",
        config_name="conf",
        template_name="conf",
        description="",
        config_version="1",
        config_tag="two-replicas",
        values={
            "replicaCount": 2
        }
    )
    conf = config.update({
        "replicaCount": 3
    })
    assert conf.instance_id == "ID_GENERATED_BY_K8SPLUGIN"
    assert conf.name == "conf"
    assert conf.template_name == "conf"
    assert conf.config_version == "2"
    assert conf.config_tag == ""
    assert conf.values == {
        "replicaCount": 3
    }


@mock.patch.object(Configuration, "send_message_json")
def test_instance_config_delete_version(mock_send_message_json):
    mock_send_message_json.return_value = CONFIG_THREE
    config = Configuration(
        instance_id="ID_GENERATED_BY_K8SPLUGIN",
        config_name="conf",
        template_name="conf",
        description="",
        config_version="1",
        config_tag="",
        values={
            "replicaCount": 2
        }
    )
    conf = config.create_delete_version()
    assert conf.instance_id == "ID_GENERATED_BY_K8SPLUGIN"
    assert conf.name == "conf"
    assert conf.template_name == "conf"
    assert conf.config_version == "2"
    assert conf.config_tag == ""


@mock.patch.object(Configuration, "send_message_json")
def test_instance_config_rollback(mock_send_message_json):
    mock_send_message_json.return_value = CONFIG
    config = Configuration(
        instance_id="ID_GENERATED_BY_K8SPLUGIN",
        config_name="conf",
        template_name="conf",
        description="",
        config_version="2",
        config_tag="",
        values={
            "replicaCount": 3
        }
    )
    config.rollback_to(config_version="1", config_tag=None)

