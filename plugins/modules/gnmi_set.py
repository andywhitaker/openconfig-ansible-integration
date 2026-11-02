#!/usr/bin/python
# (c) 2020-2026 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
---
module: gnmi_set
author:
  - "Hans Thienpondt (@HansThienpondt)"
  - "Sven Wisotzky (@wisotzky)"
short_description: Modify configuration using a single gNMI Set
description:
  - Sends a single gNMI C(SetRequest), like C(gnmic set). Deletes are applied
    first, then replaces, then updates, as a single transaction.
  - Option names follow the gNMIc flags in snake_case, and the values follow
    the gNMI 0.10.0 protobuf messages.
  - Confirmed commit uses the gNMI Commit extension, with the same options and
    rules as gNMIc. There is no separate commit module.
  - To report C(changed), the module reads the affected paths (or the full
    configuration if O(backup=true)) with gNMI Get before and after the Set.
  - This module was called C(nokia.openconfig.gnmi_config) in 1.0.0.
version_added: 1.0.0
options:
  prefix:
    description:
      - Common prefix for all paths, gNMIc C(--prefix) and C(SetRequest.prefix).
    type: str
  target:
    description:
      - Target name set on the prefix, gNMIc C(--target) and C(Path.target).
    type: str
    version_added: 2.0.0
  update:
    description:
      - Paths and values to merge, gNMIc C(--update) and C(SetRequest.update).
    type: list
    elements: dict
    suboptions:
      path:
        description:
          - Path to update. The origin is given gNMIc style, for example
            C(openconfig:/system/config).
        type: str
        required: true
      value:
        description:
          - Value to set. Dicts and lists are sent as JSON.
          - The 1.0.0 name C(val) was removed in 2.0.0.
        type: raw
        required: true
      encoding:
        description:
          - Encoding of this value, gNMIc C(--encoding). Defaults to the
            encoding of the connection.
          - One of C(JSON), C(JSON_IETF), C(ASCII), C(STRING), C(INT), C(UINT),
            C(BOOL), C(FLOAT), C(BYTES).
        type: str
        version_added: 2.0.0
  replace:
    description:
      - Paths and values to replace, gNMIc C(--replace) and
        C(SetRequest.replace).
    type: list
    elements: dict
    suboptions:
      path:
        description:
          - Path to replace.
        type: str
        required: true
      value:
        description:
          - Value to set. Dicts and lists are sent as JSON.
          - The 1.0.0 name C(val) was removed in 2.0.0.
        type: raw
        required: true
      encoding:
        description:
          - Encoding of this value. Defaults to the encoding of the connection.
        type: str
        version_added: 2.0.0
  delete:
    description:
      - Paths to delete, gNMIc C(--delete) and C(SetRequest.delete).
    type: list
    elements: str
  request_file:
    description:
      - JSON or YAML file in the gNMIc set-request format, gNMIc
        C(--request-file). Top-level keys are C(updates), C(replaces) and
        C(deletes). Each update and replace has C(path), C(value) and
        optionally C(encoding).
      - Go templates are not supported. Use M(ansible.builtin.template) to
        render the file first.
      - Relative paths are searched like M(ansible.builtin.copy) sources.
      - The entries are added to O(update), O(replace) and O(delete).
    type: path
    version_added: 2.0.0
  encoding:
    description:
      - Default encoding of the values in this request, gNMIc C(--encoding).
        Defaults to the encoding of the connection.
    type: str
    version_added: 2.0.0
  commit_id:
    description:
      - ID of the confirmed commit, gNMIc C(--commit-id) and C(Commit.id).
      - Required with O(commit_request), O(commit_confirm), O(commit_cancel)
        or O(rollback_duration).
    type: str
    version_added: 2.0.0
  commit_request:
    description:
      - Starts a confirmed commit with this Set, gNMIc C(--commit-request).
      - The device rolls back the change unless it is confirmed within
        O(rollback_duration).
    type: bool
    default: false
    version_added: 2.0.0
  commit_confirm:
    description:
      - Confirms the confirmed commit O(commit_id), gNMIc C(--commit-confirm).
      - Usually sent without O(update), O(replace) and O(delete).
    type: bool
    default: false
    version_added: 2.0.0
  commit_cancel:
    description:
      - Cancels the confirmed commit O(commit_id) and rolls back its changes,
        gNMIc C(--commit-cancel).
    type: bool
    default: false
    version_added: 2.0.0
  rollback_duration:
    description:
      - Rollback timer as Go duration, for example C(30s) or C(1m30s), gNMIc
        C(--rollback-duration).
      - With O(commit_request) it sets C(CommitRequest.rollback_duration).
        Alone, it changes the timer of the confirmed commit in progress
        (C(Commit.set_rollback_duration)).
    type: str
    version_added: 2.0.0
  dry_run:
    description:
      - Build the C(SetRequest) and return it as RV(request) without
        sending it, gNMIc C(--dry-run). Check mode does the same.
    type: bool
    default: false
    version_added: 2.0.0
  backup:
    description:
      - Save the full configuration, as read before the change, to a file on
        the controller.
      - The file contains JSON. To restore it, replace C(/) with its content,
        as shown in the examples.
    type: bool
    default: false
  backup_options:
    description:
      - Options for O(backup). Ignored if O(backup=false).
    type: dict
    suboptions:
      filename:
        description:
          - File name of the backup. Defaults to
            C(<hostname>_config.<date>@<time>).
        type: str
      dir_path:
        description:
          - Directory of the backup. Defaults to C(backup) next to the
            playbook or role. Created if missing.
        type: path
notes:
  - Requires the P(nokia.openconfig.grpc#connection) connection.
  - In check mode and with O(dry_run=true) the request is built and returned
    but not sent, and C(changed) is always false.
  - Commit operations without O(update), O(replace) or O(delete) (confirm,
    cancel, new rollback duration) always report C(changed).
requirements:
  - grpcio
  - protobuf
"""

EXAMPLES = """
# gnmic set --prefix /configure --update-path system/location --update-value Melbourne ...
- name: Update, replace and delete in one transaction
  nokia.openconfig.gnmi_set:
    prefix: /configure
    update:
      - path: system/location
        value: Melbourne
      - path: system/contact
        value: nokia
    replace:
      - path: service/md-auto-id
        value:
          service-id-range:
            start: 10000
            end: 99999
    delete:
      - system/cron

# gnmic set --request-file set-request.yml
- name: Apply a gNMIc request file
  nokia.openconfig.gnmi_set:
    request_file: set-request.yml

- name: Start a confirmed commit, rolled back after 1 minute
  nokia.openconfig.gnmi_set:
    update:
      - path: /system/name/host-name
        value: leaf1
    commit_id: change-42
    commit_request: true
    rollback_duration: 1m

- name: Confirm it
  nokia.openconfig.gnmi_set:
    commit_id: change-42
    commit_confirm: true

- name: Show the request without sending it
  nokia.openconfig.gnmi_set:
    delete:
      - /interface[name=ethernet-1/1]/description
    dry_run: true
  register: preview

- name: Backup, then restore
  nokia.openconfig.gnmi_set:
    backup: true
  register: backup

- name: Restore the backup
  nokia.openconfig.gnmi_set:
    replace:
      - path: /
        value: "{{ lookup('file', backup.backup_path) | from_json }}"
"""

RETURN = """
output:
  description:
    - The C(SetResponse) as JSON string, with paths as strings.
  returned: when the request was sent
  type: str
  sample: '{"prefix": "configure", "response": [{"op": "UPDATE", "path": "system/location"}], "timestamp": "2020-02-18T00:19:30.805600"}'
extensions:
  description:
    - Extensions returned in the C(SetResponse), using protobuf field names.
  returned: when the request was sent
  type: list
  elements: dict
  sample: [{"commit": {"id": "change-42", "commit": {"rollback_duration": "60s"}}}]
request:
  description:
    - The C(SetRequest) that would be sent, using protobuf field names.
  returned: check mode or O(dry_run=true)
  type: dict
diff:
  description:
    - Configuration of the affected paths before and after, as JSON strings.
  returned: when changed and diff mode is enabled
  type: dict
backup_path:
  description:
    - Full path of the backup file.
  returned: when O(backup=true)
  type: str
  sample: /playbooks/backup/leaf1_config.2025-01-01@10:00:00
filename:
  description:
    - Name of the backup file.
  returned: when O(backup=true) and O(backup_options.filename) is not set
  type: str
shortname:
  description:
    - Full path of the backup file without extension.
  returned: when O(backup=true) and O(backup_options.filename) is not set
  type: str
date:
  description:
    - Date of the backup.
  returned: when O(backup=true)
  type: str
time:
  description:
    - Time of the backup.
  returned: when O(backup=true)
  type: str
"""

import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.nokia.openconfig.plugins.module_utils.gnmi import (
    ENCODINGS,
    GnmiError,
    load_set_request,
)
from ansible_collections.nokia.openconfig.plugins.module_utils.gnmi_ext import commit_extension
from ansible_collections.nokia.openconfig.plugins.module_utils.gnmi_module import (
    Rpc,
    normalize_enum,
    to_json,
)

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def _entries(module, name):
    result = []
    for entry in module.params[name] or []:
        item = dict(path=entry['path'], value=entry['value'])
        if entry.get('encoding'):
            item['encoding'] = normalize_enum(module, '%s.encoding' % name, ENCODINGS, entry['encoding'])
        result.append(item)
    return result


def _load_request_file(module, path):
    try:
        with open(path) as f:
            text = f.read()
    except (IOError, OSError) as exc:
        module.fail_json(msg="Unable to read request_file %s: %s" % (path, to_text(exc)))
    try:
        data = yaml.safe_load(text) if HAS_YAML else json.loads(text)
    except Exception as exc:
        module.fail_json(msg="Unable to parse request_file %s: %s" % (path, to_text(exc)))
    try:
        return load_set_request(data)
    except GnmiError as exc:
        module.fail_json(msg=to_text(exc))


_UNKNOWN = object()


def _snapshot(module, rpc, paths, prefix, target):
    """Reads the affected configuration. Some targets reject a Get of a path
    that does not exist (yet), so a failed read does not fail the task."""
    if not paths:
        return None
    response = rpc.call('gnmiGet', dict(type='CONFIG', prefix=prefix, target=target, path=paths), fail=False)
    if response is None:
        module.warn("Could not read the affected paths, changed is reported as true")
        return _UNKNOWN
    return response['output']


def main():
    entry_spec = dict(
        path=dict(type='str', required=True),
        value=dict(type='raw', required=True),
        encoding=dict(type='str'),
    )
    backup_spec = dict(filename=dict(type='str'), dir_path=dict(type='path'))
    argument_spec = dict(
        prefix=dict(type='str'),
        target=dict(type='str'),
        update=dict(type='list', elements='dict', options=entry_spec),
        replace=dict(type='list', elements='dict', options=entry_spec),
        delete=dict(type='list', elements='str'),
        request_file=dict(type='path'),
        encoding=dict(type='str'),
        commit_id=dict(type='str'),
        commit_request=dict(type='bool', default=False),
        commit_confirm=dict(type='bool', default=False),
        commit_cancel=dict(type='bool', default=False),
        rollback_duration=dict(type='str'),
        dry_run=dict(type='bool', default=False),
        backup=dict(type='bool', default=False),
        backup_options=dict(type='dict', options=backup_spec),
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    p = module.params

    update = _entries(module, 'update')
    replace = _entries(module, 'replace')
    delete = list(p['delete'] or [])
    if p['request_file']:
        loaded = _load_request_file(module, p['request_file'])
        update.extend(loaded['update'])
        replace.extend(loaded['replace'])
        delete.extend(loaded['delete'])

    commit = dict(commit_id=p['commit_id'], commit_request=p['commit_request'], commit_confirm=p['commit_confirm'],
                  commit_cancel=p['commit_cancel'], rollback_duration=p['rollback_duration'])
    try:
        has_commit = commit_extension(p['commit_id'], p['commit_request'], p['commit_confirm'],
                                      p['commit_cancel'], p['rollback_duration']) is not None
    except GnmiError as exc:
        module.fail_json(msg=to_text(exc))

    has_changes = bool(update or replace or delete)
    if not has_changes and not has_commit and not p['backup']:
        module.fail_json(msg="Nothing to do: one of update, replace, delete, request_file, "
                             "a commit operation or backup is required")

    request = dict(prefix=p['prefix'], target=p['target'], update=update, replace=replace, delete=delete,
                   encoding=normalize_enum(module, 'encoding', ('JSON', 'JSON_IETF')), **commit)
    rpc = Rpc(module)
    result = dict(changed=False)

    if module.check_mode or p['dry_run']:
        if has_changes or has_commit:
            result['request'] = rpc('gnmiSet', dry_run=True, **request)['request']
        module.exit_json(**result)

    paths = [e['path'] for e in update] + [e['path'] for e in replace] + delete
    full = None
    if p['backup']:
        full = rpc('gnmiGet', type='CONFIG', target=p['target'], path=['/'])['output']
        result['__backup__'] = to_json(full)

    if has_changes or has_commit:
        if full is not None:
            before = full
        else:
            before = _snapshot(module, rpc, paths, p['prefix'], p['target'])

        response = rpc('gnmiSet', **request)
        result['output'] = to_json(response['output'])
        result['extensions'] = response['extensions']

        if full is not None:
            after = rpc('gnmiGet', type='CONFIG', target=p['target'], path=['/'])['output']
        else:
            after = _snapshot(module, rpc, paths, p['prefix'], p['target'])

        known = before is not _UNKNOWN and after is not _UNKNOWN
        if has_changes and known:
            result['changed'] = before != after
        else:
            result['changed'] = True
        if result['changed'] and module._diff and has_changes and known:
            result['diff'] = dict(before=to_json(before), after=to_json(after))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
