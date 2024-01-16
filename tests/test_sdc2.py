
from urllib.parse import parse_qs

from pytest import raises

from onapsdk.sdc2.sdc import SDC, ResoureTypeEnum
from onapsdk.sdc2.sdc_resource import SDCResource


def test_resource_type_enum():
    assert len(list(ResoureTypeEnum)) == 13


def test_sdc_filter_exclude_resource_type():
    for resource_type in ResoureTypeEnum:
        resource_types_list_without_one_type = list(ResoureTypeEnum.iter_without_resource_type(resource_type))
        assert len(resource_types_list_without_one_type) == 12
        with raises(ValueError):
            resource_types_list_without_one_type.index(resource_type)
