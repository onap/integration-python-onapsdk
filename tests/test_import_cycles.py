"""Test that every module can be imported before any other onapsdk module."""
#   Copyright 2026 Deutsche Telekom AG
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
import importlib
import sys
from pathlib import Path

import pytest

import onapsdk
import onapsdk.aai.business as business

SRC = Path(onapsdk.__file__).parent.parent


def _module_names():
    for path in sorted(SRC.rglob("*.py")):
        parts = list(path.relative_to(SRC).parts)
        parts[-1] = parts[-1][:-len(".py")]
        if parts[-1] == "__init__":
            parts.pop()
        if parts:
            yield ".".join(parts)


def test_every_module_imports_first():
    """Check each module imports when it is the first onapsdk module imported.

    A module reachable only after something else has been imported is caught in
    an import cycle, and a consumer that imports it first gets an ImportError.
    Purging onapsdk from sys.modules before each attempt is what makes this
    meaningful: within a test session most of the SDK is already imported, which
    hides the cycle.
    """
    original = {name: module for name, module in sys.modules.items()
                if name == "onapsdk" or name.startswith("onapsdk.")}
    failures = {}
    try:
        for module_name in _module_names():
            for name in list(original):
                sys.modules.pop(name, None)
            try:
                importlib.import_module(module_name)
            except ImportError as exc:
                failures[module_name] = str(exc)
    finally:
        # Restore the objects the rest of the session already holds references
        # to; the re-imports above created new, unrelated class objects.
        for name in [name for name in sys.modules
                     if name == "onapsdk" or name.startswith("onapsdk.")]:
            del sys.modules[name]
        sys.modules.update(original)
    assert not failures, f"modules that cannot be imported first: {failures}"


def test_business_getattr_resolves_reexport_and_submodule():
    """Check the lazy A&AI business re-exports resolve to the real objects."""
    from onapsdk.aai.business.service import ServiceInstance
    assert business.ServiceInstance is ServiceInstance
    # Importing a submodule anywhere makes Python bind it on the parent package,
    # so the cached binding has to be dropped for __getattr__ to be reached.
    business.__dict__.pop("service", None)
    assert business.service is sys.modules["onapsdk.aai.business.service"]


def test_business_getattr_raises_for_unknown_name():
    """Check an unknown A&AI business attribute still raises AttributeError."""
    with pytest.raises(AttributeError):
        business.NoSuchName  # pylint: disable=pointless-statement
