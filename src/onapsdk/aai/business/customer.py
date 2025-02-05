"""AAI business module."""
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
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Iterator, Optional
from urllib.parse import urlencode, urljoin

from onapsdk.utils.jinja import jinja_env
from onapsdk.exceptions import APIError, ParameterError, ResourceNotFound

from ..aai_element import AaiResource, Relationship
from ..cloud_infrastructure.cloud_region import CloudRegion
from .service import ServiceInstance


@dataclass
class ServiceSubscriptionCloudRegionTenantData:
    """Dataclass to store cloud regions and tenants data for service subscription."""

    cloud_owner: Optional[str] = None
    cloud_region_id: Optional[str] = None
    tenant_id: Optional[str] = None


@dataclass
class ServiceSubscription(AaiResource):
    """Service subscription class."""

    service_type: str
    resource_version: str
    customer: "Customer"

    def __init__(self, customer: "Customer", service_type: str, resource_version: str) -> None:
        """Service subscription object initialization.

        Args:
            customer (Customer): Customer object
            service_type (str): Service type
            resource_version (str): Service subscription resource version
        """
        super().__init__()
        self.customer: "Customer" = customer
        self.service_type: str = service_type
        self.resource_version: str = resource_version

    def _get_service_instance_by_filter_parameter(self,
                                                  filter_parameter_name: str,
                                                  filter_parameter_value: str) -> ServiceInstance:
        """Call a request to get service instance with given filter parameter and value.

        Args:
            filter_parameter_name (str): Name of parameter to filter
            filter_parameter_value (str): Value of filter parameter

        Returns:
            ServiceInstance: ServiceInstance object

        """
        service_instance: dict = self.send_message_json(
            "GET",
            f"Get service instance with {filter_parameter_value} {filter_parameter_name}",
            f"{self.url}/service-instances?{filter_parameter_name}={filter_parameter_value}"
        )["service-instance"][0]
        return ServiceInstance(
            service_subscription=self,
            instance_id=service_instance.get("service-instance-id"),
            instance_name=service_instance.get("service-instance-name"),
            service_type=service_instance.get("service-type"),
            service_role=service_instance.get("service-role"),
            environment_context=service_instance.get("environment-context"),
            workload_context=service_instance.get("workload-context"),
            created_at=service_instance.get("created-at"),
            updated_at=service_instance.get("updated-at"),
            description=service_instance.get("description"),
            model_invariant_id=service_instance.get("model-invariant-id"),
            model_version_id=service_instance.get("model-version-id"),
            persona_model_version=service_instance.get("persona-model-version"),
            widget_model_id=service_instance.get("widget-model-id"),
            widget_model_version=service_instance.get("widget-model-version"),
            bandwith_total=service_instance.get("bandwidth-total"),
            vhn_portal_url=service_instance.get("vhn-portal-url"),
            service_instance_location_id=service_instance.get("service-instance-location-id"),
            resource_version=service_instance.get("resource-version"),
            selflink=service_instance.get("selflink"),
            orchestration_status=service_instance.get("orchestration-status"),
            input_parameters=service_instance.get("input-parameters")
        )

    @classmethod
    def get_all_url(cls, customer: "Customer") -> str:  # pylint: disable=arguments-differ
        """Return url to get all customers.

        Returns:
            str: Url to get all customers

        """
        return (f"{cls.base_url}{cls.api_version}/business/customers/"
                f"customer/{customer.global_customer_id}/service-subscriptions/")

    @classmethod
    def create_from_api_response(cls,
                                 api_response: dict,
                                 customer: "Customer") -> "ServiceSubscription":
        """Create service subscription using API response dict.

        Returns:
            ServiceSubscription: ServiceSubscription object.

        """
        return cls(
            service_type=api_response.get("service-type"),
            resource_version=api_response.get("resource-version"),
            customer=customer
        )

    @property
    def url(self) -> str:
        """Cloud region object url.

        URL used to call CloudRegion A&AI API

        Returns:
            str: CloudRegion object url

        """
        return (
            f"{self.base_url}{self.api_version}/business/customers/"
            f"customer/{self.customer.global_customer_id}/service-subscriptions/"
            f"service-subscription/{self.service_type}"
        )

    @property
    def service_instances(self) -> Iterator[ServiceInstance]:
        """Service instances.

        Yields:
            Iterator[ServiceInstance]: Service instance

        """
        for service_instance in \
            self.send_message_json("GET",
                                   (f"Get all service instances for{self.service_type} service "
                                    f"subscription"),
                                   f"{self.url}/service-instances").get("service-instance", []):
            yield ServiceInstance.create_from_api_response(self, service_instance)

    @property
    def tenant_relationships(self) -> Iterator["Relationship"]:
        """Tenant related relationships.

        Iterate through relationships and get related to tenant.

        Yields:
            Relationship: Relationship related to tenant.

        """
        for relationship in self.relationships:
            if relationship.related_to == "tenant":
                yield relationship

    @property
    def cloud_region(self) -> "CloudRegion":
        """Cloud region associated with service subscription.

        IT'S DEPRECATED! `cloud_regions` parameter SHOULD BE USED

        Raises:
            ParameterError: Service subscription has no associated cloud region.

        Returns:
            CloudRegion: CloudRegion object

        """
        try:
            return next(self.cloud_regions)
        except StopIteration as exc:
            msg = f"No cloud region for service subscription '{self.name}'"
            raise ParameterError(msg) from exc

    @property
    def tenant(self) -> "Tenant":
        """Tenant associated with service subscription.

        IT'S DEPRECATED! `tenants` parameter SHOULD BE USED

        Raises:
            ParameterError: Service subscription has no associated tenants

        Returns:
            Tenant: Tenant object

        """
        try:
            return next(self.tenants)
        except StopIteration as exc:
            msg = f"No tenants for service subscription '{self.name}'"
            raise ParameterError(msg) from exc

    @property
    def _cloud_regions_tenants_data(self) -> Iterator["ServiceSubscriptionCloudRegionTenantData"]:
        for relationship in self.tenant_relationships:
            cr_tenant_data: ServiceSubscriptionCloudRegionTenantData = \
                ServiceSubscriptionCloudRegionTenantData()
            for data in relationship.relationship_data:
                if data["relationship-key"] == "cloud-region.cloud-owner":
                    cr_tenant_data.cloud_owner = data["relationship-value"]
                if data["relationship-key"] == "cloud-region.cloud-region-id":
                    cr_tenant_data.cloud_region_id = data["relationship-value"]
                if data["relationship-key"] == "tenant.tenant-id":
                    cr_tenant_data.tenant_id = data["relationship-value"]
            if all([cr_tenant_data.cloud_owner,
                    cr_tenant_data.cloud_region_id,
                    cr_tenant_data.tenant_id]):
                yield cr_tenant_data
            else:
                self._logger.error("Invalid tenant relationship: %s", relationship)

    @property
    def cloud_regions(self) -> Iterator["CloudRegion"]:
        """Cloud regions associated with service subscription.

        Yields:
            CloudRegion: CloudRegion object

        """
        cloud_region_set: set = set()
        for cr_data in self._cloud_regions_tenants_data:
            cloud_region_set.add((cr_data.cloud_owner, cr_data.cloud_region_id))
        for cloud_region_data in cloud_region_set:
            try:
                yield CloudRegion.get_by_id(cloud_owner=cloud_region_data[0],
                                            cloud_region_id=cloud_region_data[1])
            except ResourceNotFound:
                self._logger.error("Can't get cloud region %s %s", cloud_region_data[0],
                                   cloud_region_data[1])

    @property
    def tenants(self) -> Iterator["Tenant"]:
        """Tenants associated with service subscription.

        Yields:
            Tenant: Tenant object

        """
        for cr_data in self._cloud_regions_tenants_data:
            try:
                cloud_region: CloudRegion = CloudRegion.get_by_id(cr_data.cloud_owner,
                                                                  cr_data.cloud_region_id)
                yield cloud_region.get_tenant(cr_data.tenant_id)
            except ResourceNotFound:
                self._logger.error("Can't get %s tenant", cr_data.tenant_id)

    def get_service_instance_by_id(self, service_instance_id) -> ServiceInstance:
        """Get service instance using it's ID.

        Args:
            service_instance_id (str): ID of the service instance

        Returns:
            ServiceInstance: ServiceInstance object

        """
        return self._get_service_instance_by_filter_parameter(
            "service-instance-id",
            service_instance_id
        )

    def get_service_instance_by_name(self, service_instance_name: str) -> ServiceInstance:
        """Get service instance using it's name.

        Args:
            service_instance_name (str): Name of the service instance

        Returns:
            ServiceInstance: ServiceInstance object

        """
        return self._get_service_instance_by_filter_parameter(
            "service-instance-name",
            service_instance_name
        )

    def link_to_cloud_region_and_tenant(self,
                                        cloud_region: "CloudRegion",
                                        tenant: "Tenant") -> None:
        """Create relationship between object and cloud region with tenant.

        Args:
            cloud_region (CloudRegion): Cloud region to link to
            tenant (Tenant): Cloud region tenant to link to
        """
        relationship: Relationship = Relationship(
            related_to="tenant",
            related_link=tenant.url,
            relationship_data=[
                {
                    "relationship-key": "cloud-region.cloud-owner",
                    "relationship-value": cloud_region.cloud_owner,
                },
                {
                    "relationship-key": "cloud-region.cloud-region-id",
                    "relationship-value": cloud_region.cloud_region_id,
                },
                {
                    "relationship-key": "tenant.tenant-id",
                    "relationship-value": tenant.tenant_id,
                },
            ],
            related_to_property=[
                {"property-key": "tenant.tenant-name", "property-value": tenant.name}
            ],
        )
        self.add_relationship(relationship)


class Customer(AaiResource):
    """Customer class."""

    def __init__(self,
                 global_customer_id: str,
                 subscriber_name: str,
                 subscriber_type: str,
                 resource_version: str = None) -> None:
        """Initialize Customer class object.

        Args:
            global_customer_id (str): Global customer id used across ONAP to
                uniquely identify customer.
            subscriber_name (str): Subscriber name, an alternate way to retrieve a customer.
            subscriber_type (str): Subscriber type, a way to provide VID with
                only the INFRA customers.
            resource_version (str, optional): Used for optimistic concurrency.
                Must be empty on create, valid on update
                and delete. Defaults to None.

        """
        super().__init__()
        self.global_customer_id: str = global_customer_id
        self.subscriber_name: str = subscriber_name
        self.subscriber_type: str = subscriber_type
        self.resource_version: str = resource_version

    def __repr__(self) -> str:  # noqa
        """Customer description.

        Returns:
            str: Customer object description

        """
        return (f"Customer(global_customer_id={self.global_customer_id}, "
                f"subscriber_name={self.subscriber_name}, "
                f"subscriber_type={self.subscriber_type}, "
                f"resource_version={self.resource_version})")

    def get_service_subscription_by_service_type(self, service_type: str) -> ServiceSubscription:
        """Get subscribed service by service type.

        Call a request to get service subscriptions filtered by service-type parameter.

        Args:
            service_type (str): Service type

        Returns:
            ServiceSubscription: Service subscription

        """
        response: dict = self.send_message_json(
            "GET",
            f"Get service subscription with {service_type} service type",
            (f"{self.base_url}{self.api_version}/business/customers/"
             f"customer/{self.global_customer_id}/service-subscriptions"
             f"?service-type={service_type}")
        )
        return ServiceSubscription.create_from_api_response(response["service-subscription"][0],
                                                            self)

    @classmethod
    def get_all_url(cls) -> str:  # pylint: disable=arguments-differ
        """Return an url to get all customers.

        Returns:
            str: URL to get all customers

        """
        return f"{cls.base_url}{cls.api_version}/business/customers"

    @classmethod
    def get_all(cls,
                global_customer_id: str = None,
                subscriber_name: str = None,
                subscriber_type: str = None) -> Iterator["Customer"]:
        """Get all customers.

        Call an API to retrieve all customers. It can be filtered
            by global-customer-id, subscriber-name and/or subsriber-type.

        Args:
            global_customer_id (str): global-customer-id to filer customers by. Defaults to None.
            subscriber_name (str): subscriber-name to filter customers by. Defaults to None.
            subscriber_type (str): subscriber-type to filter customers by. Defaults to None.

        """
        filter_parameters: dict = cls.filter_none_key_values(
            {
                "global-customer-id": global_customer_id,
                "subscriber-name": subscriber_name,
                "subscriber-type": subscriber_type,
            }
        )
        url: str = f"{cls.get_all_url()}?{urlencode(filter_parameters)}"
        for customer in cls.send_message_json("GET", "get customers", url).get("customer", []):
            yield Customer(
                global_customer_id=customer["global-customer-id"],
                subscriber_name=customer["subscriber-name"],
                subscriber_type=customer["subscriber-type"],
                resource_version=customer["resource-version"],
            )

    @classmethod
    def get_by_global_customer_id(cls, global_customer_id: str) -> "Customer":
        """Get customer by it's global customer id.

        Args:
            global_customer_id (str): global customer ID

        Returns:
            Customer: Customer with given global_customer_id

        """
        response: dict = cls.send_message_json(
            "GET",
            f"Get {global_customer_id} customer",
            f"{cls.base_url}{cls.api_version}/business/customers/customer/{global_customer_id}"
        )
        return Customer(
            global_customer_id=response["global-customer-id"],
            subscriber_name=response["subscriber-name"],
            subscriber_type=response["subscriber-type"],
            resource_version=response["resource-version"],
        )

    @classmethod
    def create(cls,
               global_customer_id: str,
               subscriber_name: str,
               subscriber_type: str,
               service_subscriptions: Optional[Iterable[str]] = None) -> "Customer":
        """Create customer.

        Args:
            global_customer_id (str): Global customer id used across ONAP
                to uniquely identify customer.
            subscriber_name (str): Subscriber name, an alternate way
                to retrieve a customer.
            subscriber_type (str): Subscriber type, a way to provide
                VID with only the INFRA customers.
            service_subscriptions (Optional[Iterable[str]], optional): Iterable
                of service subscription names should be created for newly
                created customer. Defaults to None.

        Returns:
            Customer: Customer object.

        """
        url: str = (
            f"{cls.base_url}{cls.api_version}/business/customers/"
            f"customer/{global_customer_id}"
        )
        cls.send_message(
            "PUT",
            "declare customer",
            url,
            data=jinja_env()
            .get_template("customer_create_update.json.j2")
            .render(
                global_customer_id=global_customer_id,
                subscriber_name=subscriber_name,
                subscriber_type=subscriber_type,
                service_subscriptions=service_subscriptions
            ),
        )
        response: dict = cls.send_message_json(
            "GET", "get created customer", url
        )  # Call API one more time to get Customer's resource version
        return Customer(
            global_customer_id=response["global-customer-id"],
            subscriber_name=response["subscriber-name"],
            subscriber_type=response["subscriber-type"],
            resource_version=response["resource-version"],
        )

    @classmethod
    def update(cls,
               global_customer_id: str,
               subscriber_name: str,
               subscriber_type: str,
               service_subscriptions: Optional[Iterable[str]] = None) -> "Customer":
        """Update customer.

        Args:
            global_customer_id (str): Global customer id used across ONAP
                to uniquely identify customer.
            subscriber_name (str): Subscriber name, an alternate way
                to retrieve a customer.
            subscriber_type (str): Subscriber type, a way to provide
                VID with only the INFRA customers.
            service_subscriptions (Optional[Iterable[str]], optional): Iterable
                of service subscription names should be created for newly
                created customer. Defaults to None.

        Returns:
            Customer: Customer object.

        """
        url: str = (
            f"{cls.base_url}{cls.api_version}/business/customers/"
            f"customer/{global_customer_id}"
        )
        cls.send_message(
            "PATCH",
            "update customer",
            url,
            data=jinja_env()
            .get_template("customer_create_update.json.j2")
            .render(
                global_customer_id=global_customer_id,
                subscriber_name=subscriber_name,
                subscriber_type=subscriber_type,
                service_subscriptions=service_subscriptions
            ),
        )
        response: dict = cls.send_message_json(
            "GET", "get updated customer", url
        )  # Call API one more time to get Customer's resource version
        return Customer(
            global_customer_id=response["global-customer-id"],
            subscriber_name=response["subscriber-name"],
            subscriber_type=response["subscriber-type"],
            resource_version=response["resource-version"],
        )

    @property
    def url(self) -> str:
        """Return customer object url.

        Unique url address to get customer's data.

        Returns:
            str: Customer object url

        """
        return (
            f"{self.base_url}{self.api_version}/business/customers/customer/"
            f"{self.global_customer_id}?resource-version={self.resource_version}"
        )

    @property
    def service_subscriptions(self) -> Iterator[ServiceSubscription]:
        """Service subscriptions of customer resource.

        Yields:
            ServiceSubscription: ServiceSubscription object

        """
        try:
            response: dict = self.send_message_json(
                "GET",
                "get customer service subscriptions",
                f"{self.base_url}{self.api_version}/business/customers/"
                f"customer/{self.global_customer_id}/service-subscriptions"
            )
            for service_subscription in response.get("service-subscription", []):
                yield ServiceSubscription.create_from_api_response(
                    service_subscription,
                    self
                )
        except ResourceNotFound as exc:
            self._logger.info(
                "Subscriptions are not "
                "found for a customer: %s", exc)
        except APIError as exc:
            self._logger.error(
                "API returned an error: %s", exc)

    def subscribe_service(self, service_type: str) -> "ServiceSubscription":
        """Create SDC Service subscription.

        If service subscription with given service_type already exists it won't create
            a new resource but use the existing one.

        Args:
            service_type (str): Value defined by orchestration to identify this service
                across ONAP.
        """
        try:
            return self.get_service_subscription_by_service_type(service_type)
        except ResourceNotFound:
            self._logger.info("Create service subscription for %s customer",
                              self.global_customer_id)
        self.send_message(
            "PUT",
            "Create service subscription",
            (f"{self.base_url}{self.api_version}/business/customers/"
             f"customer/{self.global_customer_id}/service-subscriptions/"
             f"service-subscription/{service_type}")
        )
        return self.get_service_subscription_by_service_type(service_type)

    def delete_subscribed_service(self, service_sub: ServiceSubscription) -> None:
        """Delete SDC Service subscription.

        Args:
            service_sub (str): Value defined by orchestration to identify this service
                across ONAP.
        """
        self.send_message(
            "DELETE",
            "Delete service subscription",
            (f"{self.base_url}{self.api_version}/business/customers/"
             f"customer/{self.global_customer_id}/service-subscriptions/"
             f"service-subscription/{service_sub.service_type}?"
             f"resource-version={service_sub.resource_version}")
        )

    def delete(self) -> None:
        """Delete customer.

        Sends request to A&AI to delete customer object.

        """
        self.send_message(
            "DELETE",
            "Delete customer",
            self.url
        )


class FeasibilityCheckAndReservationJob(AaiResource):  # pylint: disable=too-many-instance-attributes
    """An instance of FeasibilityCheckAndReservationJob class."""

    def __init__(self,  # NOSONAR  # pylint: disable=too-many-arguments, too-many-locals
                 service_subscription: "ServiceSubscription",
                 feasibility_check_and_reservation_job_id: str,
                 job_name: str,
                 feasibility_result: str,
                 resource_version: str = None,
                 resource_reservation: bool = None,
                 creation_time: str = None,
                 recommendation_request: bool = None,
                 requested_reservation_expiration: str = None,
                 infeasible_reason: str = None,
                 resource_reservation_status: str = None,
                 reservation_failure_reason: str = None,
                 reservation_expiration: str = None,
                 recommended_requirements: str = None,
                 feasibility_details: str = None,
                 data_owner: str = None,
                 data_source: str = None,
                 data_source_version: str = None,
                 feasibility_time_windows: list = None,
                 slice_profiles: list = None,
                 service_profiles: list = None,
                 relationship_list: dict = None) -> None:
        """Initialize FeasibilityCheckAndReservationJob class object.

        Args:
            service_subscription (ServiceSubscription): Service subscription
            feasibility_check_and_reservation_job_id (str): Unique identifier of the job.
            job_name (str): Name of the feasibility service job.
            feasibility_result (str): Result of the feasibility check (FEASIBLE or INFEASIBLE).
            resource_version (str, optional): Used for optimistic concurrency.
            resource_reservation (bool, optional): Represents resource reservation requirement.
            creation_time (str, optional): The time when the job is created.
            recommendation_request (bool, optional): Represents request for
            recommended network slice requirements.
            requested_reservation_expiration (str, optional): Validity period of
             the resource reservation.
            infeasible_reason (str, optional): Additional reason if the feasibility
             check result is infeasible.
            resource_reservation_status (str, optional): Resource reservation result
             for the feasibility check job.
            reservation_failure_reason (str, optional): Additional reason if the reservation fails.
            reservation_expiration (str, optional): Actual validity period of the
             resource reservation.
            recommended_requirements (str, optional): Recommended network slicing
             related requirements.
            feasibility_details (str, optional): Additional details about the feasibility check.
            data_owner (str, optional): Entity responsible for managing this inventory object.
            data_source (str, optional): Upstream source of the data.
            data_source_version (str, optional): Version of the upstream source.
            feasibility_time_windows (list, optional): Feasibility time windows.
            slice_profiles (list, optional): Slice profiles.
            service_profiles (list, optional): Service profiles.
            relationship_list (dict, optional): Relationship list.
        """
        super().__init__()
        self.service_subscription: "ServiceSubscription" = service_subscription
        self.feasibility_check_and_reservation_job_id = feasibility_check_and_reservation_job_id
        self.job_name = job_name
        self.feasibility_result = feasibility_result
        self.resource_version = resource_version
        self.resource_reservation = resource_reservation
        self.creation_time = creation_time
        self.recommendation_request = recommendation_request
        self.requested_reservation_expiration = requested_reservation_expiration
        self.infeasible_reason = infeasible_reason
        self.resource_reservation_status = resource_reservation_status
        self.reservation_failure_reason = reservation_failure_reason
        self.reservation_expiration = reservation_expiration
        self.recommended_requirements = recommended_requirements
        self.feasibility_details = feasibility_details
        self.data_owner = data_owner
        self.data_source = data_source
        self.data_source_version = data_source_version
        self.feasibility_time_windows = feasibility_time_windows or []
        self.slice_profiles = slice_profiles or []
        self.service_profiles = service_profiles or []
        self.relationship_list = relationship_list or {}

    def __repr__(self) -> str:
        """Feasibility check and reservation job object representation.

        Returns:
            str: FeasibilityCheckAndReservationJob object representation

        """
        return ("FeasibilityCheckAndReservationJob(feasibility_check_and_reservation_job_id"
                f"={self.feasibility_check_and_reservation_job_id})")

    @classmethod
    def single_url(cls,
                   service_subscription: ServiceSubscription,
                   feasibility_check_and_reservation_job_id: str,
                   depth: bool = False) -> str:
        """Get an url to fetch single feasibility check and reservation job.

        Args:
            service_subscription (ServiceSubscription): Service subscription object
            feasibility_check_and_reservation_job_id (str): ID of feasibility check
                and reservation job object
            depth (bool, optional): Flag to determine if all object's information
                should be returned. Defaults to False.

        Returns:
            str: Feasibility check and reservation object

        """
        url: str =  urljoin(f"{service_subscription.url.rstrip('/')}/",
                            ("feasibility-check-and-reservation-jobs/"
                             "feasibility-check-and-reservation-job/"
                             f"{feasibility_check_and_reservation_job_id}"))
        if depth:
            return urljoin(url, "?" + urlencode({"depth": "all"}))
        return url

    @property
    def url(self) -> str:
        """Feasibility check and reservation job's url.

        Returns:
            str: Resource's url

        """
        return self.single_url(self.service_subscription,
                               self.feasibility_check_and_reservation_job_id)

    @classmethod
    def get_all_url(cls,  # pylint: disable=arguments-differ
                    service_subscription: ServiceSubscription,
                    depth: bool = False) -> str:
        """Return url to get all feasibility check and reservation jobs.

        Returns:
            str: Url to get all feasibility check and reservation jobs

        """
        url = urljoin(f"{service_subscription.url.rstrip('/')}/",
                      "feasibility-check-and-reservation-jobs/")
        if depth:
            return urljoin(url, "?" + urlencode({"depth": "all"}))
        return url

    @classmethod
    def create_from_api_response(cls,
                                 service_subscription: ServiceSubscription,
                                 response: Dict[str, Any]) -> "FeasibilityCheckAndReservationJob":
        """Create feasibility check and reservation job object from it's api response dictionary.

        Args:
            service_subscription (ServiceSubscription): Service subscription object
            response (Dict[str, Any]): API response dictionary

        Returns:
            FeasibilityCheckAndReservationJob: Feasibility check and reservation job object
        """
        return cls(
                service_subscription=service_subscription,
                feasibility_check_and_reservation_job_id=response.get(
                    "feasibility-check-and-reservation-job-id"),
                job_name=response.get("job-name"),
                feasibility_result=response.get("feasibility-result"),
                resource_version=response.get("resource-version"),
                resource_reservation=response.get("resource-reservation"),
                creation_time=response.get("creation-time"),
                recommendation_request=response.get("recommendation-request"),
                requested_reservation_expiration=response.get("requested-reservation-expiration"),
                infeasible_reason=response.get("infeasible-reason"),
                resource_reservation_status=response.get("resource-reservation-status"),
                reservation_failure_reason=response.get("reservation-failure-reason"),
                reservation_expiration=response.get("reservation-expiration"),
                recommended_requirements=response.get("recommended-requirements"),
                feasibility_details=response.get("feasibility-details"),
                data_owner=response.get("data-owner"),
                data_source=response.get("data-source"),
                data_source_version=response.get("data-source-version"),
                feasibility_time_windows=response.get("feasibility-time-windows"),
                slice_profiles=response.get("slice-profiles"),
                service_profiles=response.get("service-profiles"),
                relationship_list=response.get("relationship-list")
        )

    @classmethod
    def get_reservation_job(cls, service_subscription: ServiceSubscription,
                            feasibility_check_and_reservation_job_id: str
                            ) -> "FeasibilityCheckAndReservationJob":
        """
        Get a specific reservation job by ID from the AAI.

        Args:
            global_customer_id(str): ID of the customer
            service_subscription(str): Type of service subscription
            feasibility_check_and_reservation_job_id(str): ID of the reservation job

        Returns:
            FeasibilityCheckAndReservationJob: An instance of the
            FeasibilityCheckAndReservationJob class
            representing the specific FeasibilityCheckAndReservationJob.

        """
        try:
            response = cls.send_message_json("GET",
                                             "Get FeasibilityCheckAndReservationJob from AAI",
                                             cls.single_url(
                                                 service_subscription,
                                                 feasibility_check_and_reservation_job_id,
                                                 depth=True))
            return cls.create_from_api_response(service_subscription, response)
        except ResourceNotFound as e:
            cls._logger.error("Error retrieving reservation job %s:", e)
            return None

    @classmethod
    def get_all(cls,
                service_subscription: "ServiceSubscription"
                ) -> Iterator["FeasibilityCheckAndReservationJob"]:
        """Get all feasibility check and reservation jobs.

        Yields:
            FeasibilityCheckAndReservationJob: FeasibilityCheckAndReservationJob object

        """
        for resource in cls.send_message_json("GET",
                                              "Get A&AI feasibility check and reservation jobs",
                                              cls.get_all_url(service_subscription))\
                                                .get("feasibility-check-and-reservation-job", []):
            yield cls.create_from_api_response(service_subscription, resource)

    def delete(self) -> None:
        """Delete reservation job."""
        self.send_message("DELETE",
                          f"Delete reservation job {self.feasibility_check_and_reservation_job_id}",
                          f"{self.url}?resource-version={self.resource_version}")
