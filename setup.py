#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# -*- coding: utf-8 -*-

import os

from setuptools import setup


def snapshot_suffix(env):
    """Return the PEP 440 pre-release suffix for a snapshot build, or "".

    Only the PyPI merge job publishes snapshots, and it publishes one per merge.
    An index rejects a version it already holds, so every one of its builds needs
    a version of its own. Every other job keeps the version declared in
    version.py -- above all pypi-stage, which builds the artifact the release job
    later downloads from the staging index by exact version.
    """
    if "-pypi-merge-" not in env.get("JOB_NAME", ""):
        return ""
    build_number = env.get("BUILD_NUMBER", "")
    return f".dev{build_number}" if build_number.isdigit() else ""


if __name__ == "__main__":
    # setup() is called under a guard so the tests can import snapshot_suffix;
    # `setup.py <command>` and PEP 517 builds both run this file as __main__.
    SUFFIX = snapshot_suffix(os.environ)
    if SUFFIX:
        from src.onapsdk.version import __version__
        setup(version=f"{__version__}{SUFFIX}")
    else:
        setup()
