# (c) 2026 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause
#

"""Shared helpers for gNSI Ansible modules."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.nokia.openconfig.plugins.module_utils import gnxi_module

METHOD = 'invokeGnsi'


def run(module, **spec):
    gnxi_module.run(module, METHOD, **spec)
