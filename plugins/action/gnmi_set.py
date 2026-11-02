# (c) 2020-2026 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.errors import AnsibleError
from ansible_collections.nokia.openconfig.plugins.plugin_utils.network import (
    ActionModule as ActionNetworkModule,
)

CONNECTIONS = ('grpc', 'gnmi')


class ActionModule(ActionNetworkModule):
    def run(self, tmp=None, task_vars=None):
        del tmp  # tmp no longer has any effect

        self._config_module = True
        if self._play_context.connection.split(".")[-1] not in CONNECTIONS:
            return {
                "failed": True,
                "msg": "Connection type %s is not valid for gnmi_set, use nokia.openconfig.grpc"
                % self._play_context.connection,
            }

        request_file = self._task.args.get("request_file")
        if request_file:
            try:
                self._task.args["request_file"] = self._find_needle("files", request_file)
            except AnsibleError as e:
                return {"failed": True, "msg": "request_file %s not found: %s" % (request_file, e), "changed": False}

        return super(ActionModule, self).run(task_vars=task_vars)
