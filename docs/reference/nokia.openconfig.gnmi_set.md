# Ansible Module: nokia.openconfig.gnmi_set

**Modify configuration using a single gNMI Set**

!!! note "Notes"

    Requires the [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md) connection.

    In check mode and with [`dry_run=true`](#param-dry-run) the request is built and returned but not sent, and `changed` is always false. No backup file is written and no gNMI Get for [`backup`](#param-backup) runs in check mode.

    Commit operations without [`update`](#param-update), [`replace`](#param-replace) or [`delete`](#param-delete) (confirm, cancel, new rollback duration) always report `changed`.

## Synopsis

* Sends a single gNMI `SetRequest`. Deletes are applied first, then replaces, then updates, as a single transaction.
* Option names are the `SetRequest` fields in snake_case, and the values follow the gNMI 0.10.0 protobuf messages.
* Confirmed commit uses the gNMI Commit extension. There is no separate commit module.
* To report `changed`, the module reads the affected paths (or the full configuration if [`backup=true`](#param-backup)) with gNMI Get before and after the Set.
* This module was called `nokia.openconfig.gnmi_config` in 1.0.0.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| prefix {#param-prefix} | str | Common prefix for all paths, `SetRequest.prefix`. |
| origin {#param-origin} | str | Origin of the paths, `Path.origin`, for example `openconfig` or `rfc7951`. Set on [`prefix`](#param-prefix) if given, otherwise on each path that does not name its own origin.<br/>With an origin, element names keep their YANG module prefix, for example `/Cisco-IOS-XE-native:native/hostname` with `rfc7951`.<br/>Also used for the gNMI Get requests of [`backup`](#param-backup) and `changed`.<br/>Defaults to the `gnmi_origin` option of the connection. An empty string sends the paths without origin. |
| target {#param-target} | str | Target name set on the prefix, `Path.target`. |
| update {#param-update} | list | Paths and values to merge, `SetRequest.update`. |
| replace {#param-replace} | list | Paths and values to replace, `SetRequest.replace`. |
| delete {#param-delete} | list | Paths to delete, `SetRequest.delete`. |
| request_file {#param-request-file} | path | JSON or YAML file with the request. Top-level keys are `updates`, `replaces` and `deletes`. Each update and replace has `path`, `value` and optionally `encoding`. This is the request file format of common gNMI clients.<br/>Go templates are not supported. Use [ansible.builtin.template](https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/template_module.html) to render the file first.<br/>Relative paths are searched like [ansible.builtin.copy](https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/copy_module.html) sources.<br/>The entries are added to [`update`](#param-update), [`replace`](#param-replace) and [`delete`](#param-delete). |
| encoding {#param-encoding} | str | Default encoding of the values in this request. Defaults to the encoding of the connection.<br/>With `JSON_IETF`, SR OS expects member names qualified with the YANG module in container values, for example `nokia-conf:location`. Use `JSON` to send plain member names. |
| commit_id {#param-commit-id} | str | ID of the confirmed commit, `Commit.id`.<br/>Required with [`commit_request`](#param-commit-request), [`commit_confirm`](#param-commit-confirm), [`commit_cancel`](#param-commit-cancel) or [`rollback_duration`](#param-rollback-duration). |
| commit_request {#param-commit-request} | bool | Starts a confirmed commit with this Set, `Commit.commit`.<br/>The device rolls back the change unless it is confirmed within [`rollback_duration`](#param-rollback-duration).<br/>**Default:** `false` |
| commit_confirm {#param-commit-confirm} | bool | Confirms the confirmed commit [`commit_id`](#param-commit-id), `Commit.confirm`.<br/>Usually sent without [`update`](#param-update), [`replace`](#param-replace) and [`delete`](#param-delete).<br/>**Default:** `false` |
| commit_cancel {#param-commit-cancel} | bool | Cancels the confirmed commit [`commit_id`](#param-commit-id) and rolls back its changes, `Commit.cancel`.<br/>**Default:** `false` |
| rollback_duration {#param-rollback-duration} | str | Rollback timer as Go duration, for example `30s` or `1m30s`.<br/>With [`commit_request`](#param-commit-request) it sets `CommitRequest.rollback_duration`. Alone, it changes the timer of the confirmed commit in progress (`Commit.set_rollback_duration`). |
| dry_run {#param-dry-run} | bool | Build the `SetRequest` and return it as R`request` without sending it. Check mode does the same.<br/>**Default:** `false` |
| backup {#param-backup} | bool | Save the full configuration, as read before the change, to a file on the controller.<br/>The file contains JSON. To restore it, replace `/` with its content, as shown in the examples.<br/>**Default:** `false` |
| backup_options {#param-backup-options} | dict | Options for [`backup`](#param-backup). Ignored if [`backup=false`](#param-backup). |

## Examples

```yaml
# SR OS expects qualified member names in JSON_IETF container values;
# JSON accepts plain names
- name: Update location and contact in one container (SR OS)
  nokia.openconfig.gnmi_set:
    prefix: /configure
    encoding: json
    update:
      - path: system
        value:
          location: Antwerp
          contact: noc@example.com

- name: Update and replace in one transaction (SR Linux)
  nokia.openconfig.gnmi_set:
    update:
      - path: /system/information
        value:
          location: Antwerp
          contact: noc@example.com
    replace:
      - path: /interface[name=ethernet-1/1]/description
        value: uplink to spine1

- name: Enable LLDP and set the hostname using OpenConfig
  nokia.openconfig.gnmi_set:
    origin: openconfig
    update:
      - path: /lldp/config/enabled
        value: true
      - path: /system/config/hostname
        value: leaf1

- name: Apply a request file
  nokia.openconfig.gnmi_set:
    request_file: set-request.yml

- name: Start a confirmed commit, rolled back after 1 minute (SR OS)
  nokia.openconfig.gnmi_set:
    update:
      - path: /configure/system/location
        value: Antwerp
    commit_id: change-42
    commit_request: true
    rollback_duration: 1m

- name: Start a confirmed commit, rolled back after 1 minute (SR Linux)
  nokia.openconfig.gnmi_set:
    update:
      - path: /system/information/location
        value: Antwerp
    commit_id: change-42
    commit_request: true
    rollback_duration: 1m

- name: Confirm it
  nokia.openconfig.gnmi_set:
    commit_id: change-42
    commit_confirm: true

- name: Show a delete request without sending it (SR OS)
  nokia.openconfig.gnmi_set:
    delete:
      - /configure/port[port-id=1/1/c1/1]/description
    dry_run: true
  register: preview

- name: Show a delete request without sending it (SR Linux)
  nokia.openconfig.gnmi_set:
    delete:
      - /interface[name=ethernet-1/1]/description
    dry_run: true
  register: preview

- name: Save the configuration to a backup file
  nokia.openconfig.gnmi_set:
    backup: true
  register: backup

# The full restore with a replace of / is validated on SR Linux
- name: Restore the backup (SR Linux)
  nokia.openconfig.gnmi_set:
    replace:
      - path: /
        value: "{{ lookup('file', backup.backup_path) | from_json }}"
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str |  - The `SetResponse` as JSON string, with paths as strings.<br/>**Returned:** when the request was sent<br/>**Sample:** `{"prefix":"configure","response":[{"op":"UPDATE","path":"system/location"}],"timestamp":"2020-02-18T00:19:30.805600"}` |
| extensions {#return-extensions} | list |  - Extensions returned in the `SetResponse`, using protobuf field names.<br/>**Returned:** when the request was sent<br/>**Sample:** `[{"commit":{"id":"change-42","commit":{"rollback_duration":"60s"}}}]` |
| request {#return-request} | dict |  - The `SetRequest` that would be sent, using protobuf field names.<br/>**Returned:** check mode or [`dry_run=true`](#param-dry-run) |
| diff {#return-diff} | dict |  - Configuration of the affected paths before and after, as JSON strings.<br/>**Returned:** when changed and diff mode is enabled |
| backup_path {#return-backup-path} | str |  - Full path of the backup file.<br/>**Returned:** when [`backup=true`](#param-backup)<br/>**Sample:** `/playbooks/backup/leaf1_config.2025-01-01@10:00:00` |
| filename {#return-filename} | str |  - Name of the backup file.<br/>**Returned:** when [`backup=true`](#param-backup) and [`backup_options.filename`](#param-backup-options) is not set |
| shortname {#return-shortname} | str |  - Full path of the backup file without extension.<br/>**Returned:** when [`backup=true`](#param-backup) and [`backup_options.filename`](#param-backup-options) is not set |
| date {#return-date} | str |  - Date of the backup.<br/>**Returned:** when [`backup=true`](#param-backup) |
| time {#return-time} | str |  - Time of the backup.<br/>**Returned:** when [`backup=true`](#param-backup) |

*New in version 1.0.0*
