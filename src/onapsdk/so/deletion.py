"""Deletion module."""
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
from abc import ABC

from onapsdk.onap_service import OnapService
from onapsdk.utils.headers_creator import headers_so_creator
from onapsdk.utils.jinja import jinja_env

from onapsdk.so.so_element import OrchestrationRequest


class DeletionRequest(OrchestrationRequest, ABC):
    """Deletion request base class."""

    @classmethod
    def send_request(cls, instance: "AaiResource", instance_parent: "ServiceInstance" = None, a_la_carte: bool = True, recursive_service: bool = False) -> "Deletion":
        """Abstract method to send instance deletion request.

        Raises:
            NotImplementedError: Needs to be implemented in inheriting classes

        """
        raise NotImplementedError


class VfModuleDeletionRequest(DeletionRequest):  # pytest: disable=too-many-ancestors
    """VF module deletion class."""

    @classmethod
    def send_request(cls,
                     instance: "VfModuleInstance",
                     instance_parent: "ServiceInstance" = None,
                     a_la_carte: bool = True,
                     recursive_service: bool = False) -> "VfModuleDeletion":
        """Send request to SO to delete VNF instance.

        Args:
            instance (VfModuleInstance): Vf Module instance to delete
            a_la_carte (boolean): deletion mode

        Returns:
            VnfDeletionRequest: Deletion request object

        """
        cls._logger.debug("VF module %s deletion request", instance.vf_module_id)
        response = cls.send_message_json("DELETE",
                                         (f"Create {instance.vf_module_id} VF module"
                                          "deletion request"),
                                         (f"{cls.base_url}/onap/so/infra/"
                                          f"serviceInstantiation/{cls.api_version}/"
                                          "serviceInstances/"
                                          f"{instance.vnf_instance.service_instance.instance_id}/"
                                          f"vnfs/{instance.vnf_instance.vnf_id}/"
                                          f"vfModules/{instance.vf_module_id}"),
                                         data=jinja_env().
                                         get_template("deletion_vf_module.json.j2").
                                         render(vf_module_instance=instance,
                                                a_la_carte=a_la_carte),
                                         headers=headers_so_creator(OnapService.headers))
        return cls(request_id=response["requestReferences"]["requestId"])


class VnfDeletionRequest(DeletionRequest):  # pytest: disable=too-many-ancestors
    """VNF deletion class."""

    @classmethod
    def send_request(cls,
                     instance: "VnfInstance",
                     instance_parent: "ServiceInstance" = None,
                     a_la_carte: bool = True,
                     recursive_service: bool = False) -> "VnfDeletionRequest":
        """Send request to SO to delete VNF instance.

        Args:
            instance (VnfInstance): VNF instance to delete
            a_la_carte (boolean): deletion mode

        Returns:
            VnfDeletionRequest: Deletion request object

        """
        cls._logger.debug("VNF %s deletion request", instance.vnf_id)
        response = cls.send_message_json("DELETE",
                                         f"Create {instance.vnf_id} VNF deletion request",
                                         (f"{cls.base_url}/onap/so/infra/"
                                          f"serviceInstantiation/{cls.api_version}/"
                                          "serviceInstances/"
                                          f"{instance.service_instance.instance_id}/"
                                          f"vnfs/{instance.vnf_id}"),
                                         data=jinja_env().
                                         get_template("deletion_vnf.json.j2").
                                         render(vnf_instance=instance,
                                                a_la_carte=a_la_carte),
                                         headers=headers_so_creator(OnapService.headers))
        return cls(request_id=response["requestReferences"]["requestId"])

class PnfDeletionRequest(DeletionRequest):  # pytest: disable=too-many-ancestors
    """PNF deletion class."""

    @classmethod
    def send_request(cls,
                     instance: "PnfInstance",
                     instance_parent: "ServiceInstance" = None,
                     a_la_carte: bool = True,
                     recursive_service: bool = False) -> "PnfDeletionRequest":
        """Send request to SO to delete PNF instance.

        Args:
            instance (PnfInstance): PNF instance to delete
            a_la_carte (boolean): deletion mode

        Returns:
            PnfDeletionRequest: Deletion request object

        """
        cls._logger.debug("PNF %s deletion request", instance.pnf_id)
        response = cls.send_message_json("DELETE",
                                         f"Create {instance.pnf_id} PNF deletion request",
                                         (f"{cls.base_url}/onap/so/infra/"
                                          f"serviceInstantiation/{cls.api_version}/"
                                          "serviceInstances/"
                                          f"{instance.service_instance.instance_id}/"
                                          f"pnfs/{instance.pnf_id}"),
                                         data=jinja_env().
                                         get_template("deletion_pnf.json.j2").
                                         render(pnf_instance=instance,
                                                a_la_carte=a_la_carte),
                                         headers=headers_so_creator(OnapService.headers))
        return cls(request_id=response["requestReferences"]["requestId"])

class ServiceDeletionRequest(DeletionRequest):  # pytest: disable=too-many-ancestors
    """Service deletion request class."""

    @classmethod
    def send_request(cls,
                     instance: "ServiceInstance",
                     instance_parent: "ServiceInstance" = None,
                     a_la_carte: bool = True,
                     recursive_service: bool = False) -> "ServiceDeletionRequest":
        """Send request to SO to delete service instance.

        Args:
            instance (ServiceInstance): service instance to delete
            a_la_carte (boolean): deletion mode

        Returns:
            ServiceDeletionRequest: Deletion request object

        """
        instance_id = instance.instance_id
        if recursive_service:
            instance_id = instance_parent.instance_id
        cls._logger.debug("Service %s deletion request", instance_id)
        response = cls.send_message_json("DELETE",
                                         f"Create {instance_id} Service deletion request",
                                         (f"{cls.base_url}/onap/so/infra/"
                                          f"serviceInstantiation/{cls.api_version}/"
                                          f"serviceInstances/{instance_id}"),
                                         data=jinja_env().
                                         get_template("deletion_service.json.j2").
                                         render(service_instance=instance,
                                                parent_service_instance=instance_parent,
                                                a_la_carte=a_la_carte,
                                                recursive_service=recursive_service),
                                         headers=headers_so_creator(OnapService.headers))
        return cls(request_id=response["requestReferences"]["requestId"])


class NetworkDeletionRequest(DeletionRequest):  # pylint: disable=too-many-ancestors
    """Network deletion request class."""

    @classmethod
    def send_request(cls,
                     instance: "NetworkInstance",
                     instance_parent: "ServiceInstance" = None,
                     a_la_carte: bool = True,
                     recursive_service: bool = False) -> "VnfDeletionRequest":
        """Send request to SO to delete Network instance.

        Args:
            instance (NetworkInstance): Network instance to delete
            a_la_carte (boolean): deletion mode

        Returns:
            NetworkDeletionRequest: Deletion request object

        """
        cls._logger.debug("Network %s deletion request", instance.network_id)
        response = cls.send_message_json("DELETE",
                                         f"Create {instance.network_id} Network deletion request",
                                         (f"{cls.base_url}/onap/so/infra/"
                                          f"serviceInstantiation/{cls.api_version}/"
                                          "serviceInstances/"
                                          f"{instance.service_instance.instance_id}/"
                                          f"networks/{instance.network_id}"),
                                         data=jinja_env().
                                         get_template("deletion_network.json.j2").
                                         render(network_instance=instance,
                                                a_la_carte=a_la_carte),
                                         headers=headers_so_creator(OnapService.headers))
        return cls(request_id=response["requestReferences"]["requestId"])
