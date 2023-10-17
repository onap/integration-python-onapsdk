"""Modification of the PNF module."""

from abc import ABC
from typing import TYPE_CHECKING
from onapsdk.aai.business.owning_entity import OwningEntity
from onapsdk.onap_service import OnapService
from onapsdk.so.so_element import OrchestrationRequest
from onapsdk.utils.headers_creator import headers_so_creator
from onapsdk.utils.jinja import jinja_env
from onapsdk.configuration import settings

if TYPE_CHECKING:
    from onapsdk.aai.business.service import ServiceInstance
    from onapsdk.aai.business import PnfInstance as Pnf


class PnfModificationRequest(OrchestrationRequest, ABC):
    """PNF Modification class."""

    @classmethod
    def send_request(cls,
                     pnf_object: "Pnf",
                     sdc_service: "Service",
                     aai_service_instance: "ServiceInstance") -> "PnfModificationRequest":
        """Send request to SO to modify PNF instance.

        Args:
            pnf_object: pnf object for pnf id
            sdc_service: service for modify pnf
            aai_service_instance: Service object from aai sdc

        Returns:
            PnfModificationRequest: modify request object

        """
        owning_entity_id = None
        project = settings.PROJECT
        line_of_business = settings.LOB
        platform = settings.PLATFORM

        for rel in aai_service_instance.relationships:
            if rel.related_to == "owning-entity":
                owning_entity_id = rel.relationship_data.pop().get("relationship-value")
            if rel.related_to == "project":
                project = rel.relationship_data.pop().get("relationship-value")

        owning_entity = OwningEntity.get_by_owning_entity_id(
            owning_entity_id=owning_entity_id)

        cls._logger.debug("PNF %s modify request", pnf_object.pnf_id)
        response = cls.send_message_json("PUT",
                                         f"Create {pnf_object.pnf_id} PNF modification request",
                                         (f"{cls.base_url}/onap/so/infra/"
                                          f"serviceInstantiation/{cls.api_version}/"
                                          "serviceInstances/"
                                          f"{aai_service_instance.instance_id}/"
                                          f"pnfs/{pnf_object.pnf_id}"),
                                         data=jinja_env().
                                         get_template("modify_pnf.json.j2").
                                         render(
                                             platform_name=platform,
                                             service=sdc_service,
                                             project=project,
                                             owning_entity=owning_entity,
                                             line_of_business=line_of_business,
                                             service_instance=aai_service_instance
                                         ),
                                         headers=headers_so_creator(OnapService.headers))

        return cls(request_id=response["requestReferences"]["requestId"])
