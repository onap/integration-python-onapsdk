
from urllib.parse import parse_qs

from pytest import raises

from onapsdk.sdc2.sdc import ResoureTypeEnum
from onapsdk.sdc2.sdc_resource import SDCResource

def test_build_exclude_types_query():
    for resource_type in ResoureTypeEnum:
        query = SDCResource._build_exclude_types_query(resource_type)
        assert query.count("excludeTypes=") == 12
        with raises(ValueError):
            parse_qs(query)["excludeTypes"].index(resource_type.value)
        for other_resource_type in ResoureTypeEnum:
            if other_resource_type == resource_type:
                continue
            parse_qs(query)["excludeTypes"].index(other_resource_type.value)
