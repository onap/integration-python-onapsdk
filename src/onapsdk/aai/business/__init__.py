"""A&AI business package."""
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
#
# The names below are re-exported lazily through PEP 562 __getattr__ rather than
# imported eagerly. Importing them here makes an import of any single A&AI
# business submodule execute all of them, which closes an import cycle with
# onapsdk.so.instantiation and leaves that module unimportable until something
# else has been imported first.
from importlib import import_module
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .customer import Customer, FeasibilityCheckAndReservationJob, ServiceSubscription
    from .instance import Instance
    from .line_of_business import LineOfBusiness
    from .network import NetworkInstance
    from .owning_entity import OwningEntity
    from .platform import Platform
    from .pnf import PnfInstance
    from .project import Project
    from .service import ServiceInstance
    from .sp_partner import SpPartner
    from .vf_module import VfModuleInstance
    from .vnf import VnfInstance

_SUBMODULE_BY_NAME = {
    "Customer": ".customer",
    "FeasibilityCheckAndReservationJob": ".customer",
    "ServiceSubscription": ".customer",
    "Instance": ".instance",
    "LineOfBusiness": ".line_of_business",
    "NetworkInstance": ".network",
    "OwningEntity": ".owning_entity",
    "Platform": ".platform",
    "PnfInstance": ".pnf",
    "Project": ".project",
    "ServiceInstance": ".service",
    "SpPartner": ".sp_partner",
    "VfModuleInstance": ".vf_module",
    "VnfInstance": ".vnf",
}

_SUBMODULES = {submodule.lstrip(".") for submodule in _SUBMODULE_BY_NAME.values()}

# The submodule names belong in __all__ because the eager imports this replaces
# bound them as package attributes too, so both `onapsdk.aai.business.service`
# and `from onapsdk.aai.business import *` used to resolve them.
__all__ = sorted(_SUBMODULE_BY_NAME) + sorted(_SUBMODULES)


def __getattr__(name: str) -> Any:
    """Import a re-exported class, or a submodule, on first access.

    Args:
        name (str): Name of the attribute to resolve.

    Raises:
        AttributeError: The name is neither a re-export nor a submodule.

    Returns:
        Any: The re-exported class or the submodule.

    """
    if name in _SUBMODULE_BY_NAME:
        value = getattr(import_module(_SUBMODULE_BY_NAME[name], __name__), name)
    elif name in _SUBMODULES:
        value = import_module(f".{name}", __name__)
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    globals()[name] = value
    return value
