
from collections import namedtuple
from random import randint
from unittest.mock import patch, PropertyMock
from uuid import uuid4

from pytest import raises

from onapsdk.configuration import settings
from onapsdk.exceptions import ResourceNotFound
from onapsdk.sdc2.sdc_category import ServiceCategory, ResourceCategory, ProductCategory, SdcSubCategory


# Service categories tests
@patch("onapsdk.sdc2.sdc_category.ServiceCategory.send_message_json")
@patch("onapsdk.sdc2.sdc_category.ServiceCategory.create_from_api_response")
def test_service_category_get_all(mock_create_from_api_response, mock_send_message_json):
    mock_send_message_json.return_value = []
    assert len(list(ServiceCategory.get_all())) == 0
    mock_send_message_json.assert_called_once_with(
        "GET",
        "Get all ServiceCategory",
        f"{settings.SDC_BE_URL}/sdc2/rest/v1/categories/services"
    )

    mock_send_message_json.return_value = [{}]
    assert len(list(ServiceCategory.get_all())) == 1
    mock_create_from_api_response.assert_called_once_with({})


@patch("onapsdk.sdc2.sdc_category.ServiceCategory.get_all")
def test_service_category_get_by_unique_id(mock_get_all):
    mock_get_all.return_value = []
    with raises(ResourceNotFound):
        ServiceCategory.get_by_uniqe_id("test_unique_id")

    TestCategory = namedtuple("TestCategory", "unique_id")
    mock_get_all.return_value = [TestCategory(f"unique_id_{i}") for i in range(10**2)]
    with raises(ResourceNotFound):
        ServiceCategory.get_by_uniqe_id("test_unique_id")
    for i in range(10**2):
        assert ServiceCategory.get_by_uniqe_id(f"unique_id_{i}") is not None


@patch("onapsdk.sdc2.sdc_category.ServiceCategory.get_all")
def test_service_category_get_by_name(mock_get_all):
    mock_get_all.return_value = []
    with raises(ResourceNotFound):
        ServiceCategory.get_by_name("test_name")

    TestCategory = namedtuple("TestCategory", "name")
    mock_get_all.return_value = [TestCategory(f"name_{i}") for i in range(10**2)]
    with raises(ResourceNotFound):
        ServiceCategory.get_by_name("test_name")
    for i in range(10**2):
        assert ServiceCategory.get_by_name(f"name_{i}") is not None


def test_service_category_create_from_api_response():
    api_response = {
        "name": str(uuid4()),
        "icons": [str(uuid4())],
        "models": [str(uuid4())],
        "normalizedName": str(uuid4()),
        "uniqueId": str(uuid4()),
        "ownerId": str(uuid4()),
        "type": str(uuid4()),
        "version": str(uuid4()),
        "displayName": str(uuid4()),
        "empty": bool(randint(0, 1)),
        "useServiceSubstitutionForNestedServices": bool(randint(0, 1)),
    }
    si = ServiceCategory.create_from_api_response(api_response)
    assert si.name == api_response["name"]
    assert si.empty == api_response["empty"]
    assert si.icons == api_response["icons"]
    assert si.models == api_response["models"]
    assert si.normalized_name == api_response["normalizedName"]
    assert si.unique_id == api_response["uniqueId"]
    assert si.use_service_substitution_for_nested_services == api_response["useServiceSubstitutionForNestedServices"]
    assert si.owner_id == api_response["ownerId"]
    assert si.subcategories == None
    assert si.category_type == api_response["type"]
    assert si.version == api_response["version"]
    assert si.display_name == api_response["displayName"]


    api_response = {
        "name": str(uuid4()),
        "icons": [str(uuid4())],
        "models": [str(uuid4())],
        "normalizedName": str(uuid4()),
        "uniqueId": str(uuid4()),
        "ownerId": str(uuid4()),
        "type": str(uuid4()),
        "version": str(uuid4()),
        "displayName": str(uuid4()),
        "empty": bool(randint(0, 1)),
        "useServiceSubstitutionForNestedServices": bool(randint(0, 1)),
        "subcategories": [
            {
                "name": str(uuid4()),
                "normalizedName": str(uuid4()),
                "uniqueId": str(uuid4()),
            },
            {
                "name": str(uuid4()),
                "normalizedName": str(uuid4()),
                "uniqueId": str(uuid4()),
            }
        ]
    }
    si = ServiceCategory.create_from_api_response(api_response)
    assert si.name == api_response["name"]
    assert si.empty == api_response["empty"]
    assert si.icons == api_response["icons"]
    assert si.models == api_response["models"]
    assert si.normalized_name == api_response["normalizedName"]
    assert si.unique_id == api_response["uniqueId"]
    assert si.use_service_substitution_for_nested_services == api_response["useServiceSubstitutionForNestedServices"]
    assert si.owner_id == api_response["ownerId"]
    assert len(si.subcategories) == 2
    assert si.subcategories[0].name == api_response["subcategories"][0]["name"]
    assert si.subcategories[0].normalized_name == api_response["subcategories"][0]["normalizedName"]
    assert si.subcategories[0].unique_id == api_response["subcategories"][0]["uniqueId"]
    assert si.subcategories[1].name == api_response["subcategories"][1]["name"]
    assert si.subcategories[1].normalized_name == api_response["subcategories"][1]["normalizedName"]
    assert si.subcategories[1].unique_id == api_response["subcategories"][1]["uniqueId"]
    assert si.category_type == api_response["type"]
    assert si.version == api_response["version"]
    assert si.display_name == api_response["displayName"]


def test_service_category_get_subcategory():
    sc = ServiceCategory(
        name=str(uuid4()),
        empty=bool(randint(0, 1)),
        icons=[str(uuid4())],
        models=[str(uuid4())],
        normalized_name=str(uuid4()),
        unique_id=str(uuid4()),
        use_service_substitution_for_nested_services=bool(randint(0, 1)),
        subcategories=None
    )
    assert sc.get_subcategory(subcategory_name="test_subc") is None
    sc.subcategories = [SdcSubCategory(
        name=f"subcategory_{i}",
        normalized_name=f"subcategory_{i}",
        unique_id=str(uuid4())
    ) for i in range(10**2)]
    assert sc.get_subcategory(subcategory_name="test_subc") is None
    for i in range(10**2):
        assert sc.get_subcategory(subcategory_name=f"subcategory_{i}") is not None


# Resource categories tests
@patch("onapsdk.sdc2.sdc_category.ResourceCategory.send_message_json")
@patch("onapsdk.sdc2.sdc_category.ResourceCategory.create_from_api_response")
def test_resource_category_get_all(mock_create_from_api_response, mock_send_message_json):
    mock_send_message_json.return_value = []
    assert len(list(ResourceCategory.get_all())) == 0
    mock_send_message_json.assert_called_once_with(
        "GET",
        "Get all ResourceCategory",
        f"{settings.SDC_BE_URL}/sdc2/rest/v1/categories/resources"
    )

    mock_send_message_json.return_value = [{}]
    assert len(list(ResourceCategory.get_all())) == 1
    mock_create_from_api_response.assert_called_once_with({})


@patch("onapsdk.sdc2.sdc_category.ResourceCategory.get_all")
def test_resource_category_get_by_unique_id(mock_get_all):
    mock_get_all.return_value = []
    with raises(ResourceNotFound):
        ResourceCategory.get_by_uniqe_id("test_unique_id")

    TestCategory = namedtuple("TestCategory", "unique_id")
    mock_get_all.return_value = [TestCategory(f"unique_id_{i}") for i in range(10**2)]
    with raises(ResourceNotFound):
        ResourceCategory.get_by_uniqe_id("test_unique_id")
    for i in range(10**2):
        assert ResourceCategory.get_by_uniqe_id(f"unique_id_{i}") is not None


@patch("onapsdk.sdc2.sdc_category.ResourceCategory.get_all")
def test_resource_category_get_by_name(mock_get_all):
    mock_get_all.return_value = []
    with raises(ResourceNotFound):
        ResourceCategory.get_by_name("test_name")

    TestCategory = namedtuple("TestCategory", "name")
    mock_get_all.return_value = [TestCategory(f"name_{i}") for i in range(10**2)]
    with raises(ResourceNotFound):
        ResourceCategory.get_by_name("test_name")
    for i in range(10**2):
        assert ResourceCategory.get_by_name(f"name_{i}") is not None


def test_resource_category_create_from_api_response():
    api_response = {
        "name": str(uuid4()),
        "icons": [str(uuid4())],
        "models": [str(uuid4())],
        "normalizedName": str(uuid4()),
        "uniqueId": str(uuid4()),
        "ownerId": str(uuid4()),
        "type": str(uuid4()),
        "version": str(uuid4()),
        "displayName": str(uuid4()),
        "empty": bool(randint(0, 1)),
        "useServiceSubstitutionForNestedServices": bool(randint(0, 1)),
    }
    rc = ResourceCategory.create_from_api_response(api_response)
    assert rc.name == api_response["name"]
    assert rc.empty == api_response["empty"]
    assert rc.icons == api_response["icons"]
    assert rc.models == api_response["models"]
    assert rc.normalized_name == api_response["normalizedName"]
    assert rc.unique_id == api_response["uniqueId"]
    assert rc.use_service_substitution_for_nested_services == api_response["useServiceSubstitutionForNestedServices"]
    assert rc.owner_id == api_response["ownerId"]
    assert rc.subcategories == None
    assert rc.category_type == api_response["type"]
    assert rc.version == api_response["version"]
    assert rc.display_name == api_response["displayName"]


    api_response = {
        "name": str(uuid4()),
        "icons": [str(uuid4())],
        "models": [str(uuid4())],
        "normalizedName": str(uuid4()),
        "uniqueId": str(uuid4()),
        "ownerId": str(uuid4()),
        "type": str(uuid4()),
        "version": str(uuid4()),
        "displayName": str(uuid4()),
        "empty": bool(randint(0, 1)),
        "useServiceSubstitutionForNestedServices": bool(randint(0, 1)),
        "subcategories": [
            {
                "name": str(uuid4()),
                "normalizedName": str(uuid4()),
                "uniqueId": str(uuid4()),
            },
            {
                "name": str(uuid4()),
                "normalizedName": str(uuid4()),
                "uniqueId": str(uuid4()),
            }
        ]
    }
    rc = ResourceCategory.create_from_api_response(api_response)
    assert rc.name == api_response["name"]
    assert rc.empty == api_response["empty"]
    assert rc.icons == api_response["icons"]
    assert rc.models == api_response["models"]
    assert rc.normalized_name == api_response["normalizedName"]
    assert rc.unique_id == api_response["uniqueId"]
    assert rc.use_service_substitution_for_nested_services == api_response["useServiceSubstitutionForNestedServices"]
    assert rc.owner_id == api_response["ownerId"]
    assert len(rc.subcategories) == 2
    assert rc.subcategories[0].name == api_response["subcategories"][0]["name"]
    assert rc.subcategories[0].normalized_name == api_response["subcategories"][0]["normalizedName"]
    assert rc.subcategories[0].unique_id == api_response["subcategories"][0]["uniqueId"]
    assert rc.subcategories[1].name == api_response["subcategories"][1]["name"]
    assert rc.subcategories[1].normalized_name == api_response["subcategories"][1]["normalizedName"]
    assert rc.subcategories[1].unique_id == api_response["subcategories"][1]["uniqueId"]
    assert rc.category_type == api_response["type"]
    assert rc.version == api_response["version"]
    assert rc.display_name == api_response["displayName"]


def test_resource_category_get_subcategory():
    rc = ResourceCategory(
        name=str(uuid4()),
        empty=bool(randint(0, 1)),
        icons=[str(uuid4())],
        models=[str(uuid4())],
        normalized_name=str(uuid4()),
        unique_id=str(uuid4()),
        use_service_substitution_for_nested_services=bool(randint(0, 1)),
        subcategories=None
    )
    assert rc.get_subcategory(subcategory_name="test_subc") is None
    rc.subcategories = [SdcSubCategory(
        name=f"subcategory_{i}",
        normalized_name=f"subcategory_{i}",
        unique_id=str(uuid4())
    ) for i in range(10**2)]
    assert rc.get_subcategory(subcategory_name="test_subc") is None
    for i in range(10**2):
        assert rc.get_subcategory(subcategory_name=f"subcategory_{i}") is not None


# Product categories tests
@patch("onapsdk.sdc2.sdc_category.ProductCategory.send_message_json")
@patch("onapsdk.sdc2.sdc_category.ProductCategory.create_from_api_response")
def test_product_category_get_all(mock_create_from_api_response, mock_send_message_json):
    mock_send_message_json.return_value = []
    assert len(list(ProductCategory.get_all())) == 0
    mock_send_message_json.assert_called_once_with(
        "GET",
        "Get all ProductCategory",
        f"{settings.SDC_BE_URL}/sdc2/rest/v1/categories/products"
    )

    mock_send_message_json.return_value = [{}]
    assert len(list(ProductCategory.get_all())) == 1
    mock_create_from_api_response.assert_called_once_with({})


@patch("onapsdk.sdc2.sdc_category.ProductCategory.get_all")
def test_product_category_get_by_unique_id(mock_get_all):
    mock_get_all.return_value = []
    with raises(ResourceNotFound):
        ProductCategory.get_by_uniqe_id("test_unique_id")

    TestCategory = namedtuple("TestCategory", "unique_id")
    mock_get_all.return_value = [TestCategory(f"unique_id_{i}") for i in range(10**2)]
    with raises(ResourceNotFound):
        ProductCategory.get_by_uniqe_id("test_unique_id")
    for i in range(10**2):
        assert ProductCategory.get_by_uniqe_id(f"unique_id_{i}") is not None


@patch("onapsdk.sdc2.sdc_category.ProductCategory.get_all")
def test_product_category_get_by_name(mock_get_all):
    mock_get_all.return_value = []
    with raises(ResourceNotFound):
        ProductCategory.get_by_name("test_name")

    TestCategory = namedtuple("TestCategory", "name")
    mock_get_all.return_value = [TestCategory(f"name_{i}") for i in range(10**2)]
    with raises(ResourceNotFound):
        ProductCategory.get_by_name("test_name")
    for i in range(10**2):
        assert ProductCategory.get_by_name(f"name_{i}") is not None


def test_product_category_create_from_api_response():
    api_response = {
        "name": str(uuid4()),
        "icons": [str(uuid4())],
        "models": [str(uuid4())],
        "normalizedName": str(uuid4()),
        "uniqueId": str(uuid4()),
        "ownerId": str(uuid4()),
        "type": str(uuid4()),
        "version": str(uuid4()),
        "displayName": str(uuid4()),
        "empty": bool(randint(0, 1)),
        "useServiceSubstitutionForNestedServices": bool(randint(0, 1)),
    }
    pc = ProductCategory.create_from_api_response(api_response)
    assert pc.name == api_response["name"]
    assert pc.empty == api_response["empty"]
    assert pc.icons == api_response["icons"]
    assert pc.models == api_response["models"]
    assert pc.normalized_name == api_response["normalizedName"]
    assert pc.unique_id == api_response["uniqueId"]
    assert pc.use_service_substitution_for_nested_services == api_response["useServiceSubstitutionForNestedServices"]
    assert pc.owner_id == api_response["ownerId"]
    assert pc.subcategories == None
    assert pc.category_type == api_response["type"]
    assert pc.version == api_response["version"]
    assert pc.display_name == api_response["displayName"]


    api_response = {
        "name": str(uuid4()),
        "icons": [str(uuid4())],
        "models": [str(uuid4())],
        "normalizedName": str(uuid4()),
        "uniqueId": str(uuid4()),
        "ownerId": str(uuid4()),
        "type": str(uuid4()),
        "version": str(uuid4()),
        "displayName": str(uuid4()),
        "empty": bool(randint(0, 1)),
        "useServiceSubstitutionForNestedServices": bool(randint(0, 1)),
        "subcategories": [
            {
                "name": str(uuid4()),
                "normalizedName": str(uuid4()),
                "uniqueId": str(uuid4()),
            },
            {
                "name": str(uuid4()),
                "normalizedName": str(uuid4()),
                "uniqueId": str(uuid4()),
            }
        ]
    }
    pc = ProductCategory.create_from_api_response(api_response)
    assert pc.name == api_response["name"]
    assert pc.empty == api_response["empty"]
    assert pc.icons == api_response["icons"]
    assert pc.models == api_response["models"]
    assert pc.normalized_name == api_response["normalizedName"]
    assert pc.unique_id == api_response["uniqueId"]
    assert pc.use_service_substitution_for_nested_services == api_response["useServiceSubstitutionForNestedServices"]
    assert pc.owner_id == api_response["ownerId"]
    assert len(pc.subcategories) == 2
    assert pc.subcategories[0].name == api_response["subcategories"][0]["name"]
    assert pc.subcategories[0].normalized_name == api_response["subcategories"][0]["normalizedName"]
    assert pc.subcategories[0].unique_id == api_response["subcategories"][0]["uniqueId"]
    assert pc.subcategories[1].name == api_response["subcategories"][1]["name"]
    assert pc.subcategories[1].normalized_name == api_response["subcategories"][1]["normalizedName"]
    assert pc.subcategories[1].unique_id == api_response["subcategories"][1]["uniqueId"]
    assert pc.category_type == api_response["type"]
    assert pc.version == api_response["version"]
    assert pc.display_name == api_response["displayName"]


def test_product_category_get_subcategory():
    pc = ProductCategory(
        name=str(uuid4()),
        empty=bool(randint(0, 1)),
        icons=[str(uuid4())],
        models=[str(uuid4())],
        normalized_name=str(uuid4()),
        unique_id=str(uuid4()),
        use_service_substitution_for_nested_services=bool(randint(0, 1)),
        subcategories=None
    )
    assert pc.get_subcategory(subcategory_name="test_subc") is None
    pc.subcategories = [SdcSubCategory(
        name=f"subcategory_{i}",
        normalized_name=f"subcategory_{i}",
        unique_id=str(uuid4())
    ) for i in range(10**2)]
    assert pc.get_subcategory(subcategory_name="test_subc") is None
    for i in range(10**2):
        assert pc.get_subcategory(subcategory_name=f"subcategory_{i}") is not None
