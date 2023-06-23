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
from onapsdk.aai.business.owning_entity import OwningEntity
from typing import Iterable
from onapsdk.utils.headers_creator import headers_so_creator
from onapsdk.utils.jinja import jinja_env

from onapsdk.so.so_element import OrchestrationRequest


class DeletionRequest(OrchestrationRequest, ABC):
    """Deletion request base class."""

    @classmethod
    def send_request(cls, instance: "AaiResource", a_la_carte: bool = True) -> "Deletion":
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
                     a_la_carte: bool = True) -> "VfModuleDeletion":
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
                     a_la_carte: bool = True) -> "VnfDeletionRequest":
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
                     a_la_carte: bool = True) -> "PnfDeletionRequest":
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

    def __init__(self,  # pylint: disable=too-many-arguments
                 name: str,
                 request_id: str,
                 instance_id: str,
                 sdc_service: "SdcService",
                 cloud_region: "CloudRegion",
                 tenant: "Tenant",
                 customer: "Customer",
                 owning_entity: OwningEntity,
                 project: str) -> None:
        """Class ServiceDeletionRequest object initialization.

        Args:
            name (str): service instance name
            request_id (str): service instantiation request ID
            instance_id (str): service instantiation ID
            sdc_service (SdcService): SdcService class object
            cloud_region (CloudRegion): CloudRegion class object
            tenant (Tenant): Tenant class object
            customer (Customer): Customer class object
            owning_entity (OwningEntity): OwningEntity class object
            project (str): Project name

        """
        self.sdc_service = sdc_service
        self.cloud_region = cloud_region
        self.tenant = tenant
        self.customer = customer
        self.owning_entity = owning_entity
        self.project = project



    # pylint: disable=too-many-arguments, too-many-locals
    @classmethod
    def send_request(cls,
                          instance: "ServiceInstance",
                          sdc_service: "SdcService",
                          sdc_recursive_service: "SdcService",
                          customer: "Customer",
                          owning_entity: OwningEntity,
                          project: str,
                          line_of_business: str,
                          platform: str,
                          aai_service: "AaiService" = None,
                          cloud_region: "CloudRegion" = None,
                          tenant: "Tenant" = None,
                          service_instance_name: str = None,
						  parent_service_instance_name: str = None,
                          vnf_parameters: Iterable["VnfParameters"] = None,
                          enable_multicloud: bool = False,
                          recursive_service: bool = False,
                          so_service: "SoService" = None,
                          service_subscription: "ServiceSubscription" = None,
                          a_la_carte: bool = True,
                          ) -> "ServiceDeletionRequest":
        """Send request to SO to delete service instance.

        Args:
            instance (ServiceInstance): service instance to delete
            a_la_carte (boolean): deletion mode

        Returns:
            ServiceDeletionRequest: Deletion request object

        """
        template_file = "deletion_service.json.j2"
        if recursive_service:
            template_file = "instantiate_recursive_service_macro.json.j2"
        cls._logger.debug("Service %s deletion request", instance.instance_id)
        response = cls.send_message_json("DELETE",
                                         f"Create {instance.instance_id} Service deletion request",
										 (f"{cls.base_url}/onap/so/infra/"
                                          f"serviceInstantiation/{cls.api_version}/"
                                          f"serviceInstances/{instance.instance_id}"),
                                         data=jinja_env().
                                         get_template(template_file).
                                         render(service_instance=instance,
                                                a_la_carte=a_la_carte,
                                                so_service=so_service,
                                                sdc_service=sdc_service,
                                                sdc_recursive_service=sdc_recursive_service,
                                                cloud_region=cloud_region,
                                                tenant=tenant,
                                                customer=customer,
                                                owning_entity=owning_entity,
                                                project=project,
                                                aai_service=aai_service,
                                                line_of_business=line_of_business,
                                                platform=platform,
                                                service_instance_name=service_instance_name,
												parent_service_instance_name=parent_service_instance_name,
                                                vnf_parameters=vnf_parameters,
                                                enable_multicloud=enable_multicloud,
                                                service_subscription=service_subscription
                                                ),
                                         headers=headers_so_creator(OnapService.headers))
        return cls(
            name=service_instance_name,
            request_id=response["requestReferences"].get("requestId"),
            instance_id=response["requestReferences"].get("instanceId"),
            sdc_service=sdc_service,
            cloud_region=cloud_region,
            tenant=tenant,
            customer=customer,
            owning_entity=owning_entity,
            project=project
        )


class NetworkDeletionRequest(DeletionRequest):  # pylint: disable=too-many-ancestors
    """Network deletion request class."""

    @classmethod
    def send_request(cls,
                     instance: "NetworkInstance",
                     a_la_carte: bool = True) -> "VnfDeletionRequest":
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
