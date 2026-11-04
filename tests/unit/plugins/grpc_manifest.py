# (c) 2026 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause
#

"""Access to tools/nokia_grpc_modules.yaml and its generator for unit tests."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import importlib.util
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
GENERATOR = os.path.join(ROOT, 'tools', 'generate_grpc_modules.py')


def generator():
    spec = importlib.util.spec_from_file_location('generate_grpc_modules', GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def entries():
    return generator().load_manifest()


def services(protocol):
    return {e['service'] for e in entries() if e['protocol'] == protocol}


def rpcs(protocol, service):
    return {e['rpc'] for e in entries() if e['protocol'] == protocol and e['service'] == service}
