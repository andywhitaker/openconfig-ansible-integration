# Ansible Module: nokia.openconfig.gnoi_healthz_artifact

**Download a health artifact over gNOI**

!!! note "Notes"

    Requires [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md).

    Supported on Nokia SR Linux.

    Read-only RPC. Runs in check mode and always reports `changed=false`.

    Server-streaming RPC. The task sends one request and collects every response message until the device ends the stream, then returns them in R`output`. The task fails if the stream does not end within the command timeout of the connection (`ansible_command_timeout`).

    Not exercised by the collection integration tests on Nokia devices; covered by unit tests against the gNOI/gNSI mock server.

## Synopsis

* Invokes gNOI `Healthz.Artifact` and returns the streamed artifact messages.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| id {#param-id} | str | Artifact ID from a `Healthz.Get` or `Healthz.List` response.<br/>**Required:** always |

## Examples

```yaml
- name: Get the health of control module A (SR Linux)
  nokia.openconfig.gnoi_healthz_get:
    path: /platform/control[slot=A]
  register: health

- name: Download the first artifact (SR Linux)
  nokia.openconfig.gnoi_healthz_artifact:
    id: "{{ (health.output | from_json).component.artifacts[0].id }}"
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str | Response messages as a JSON list in stream order (protobuf JSON names).<br/>**Returned:** success |

*New in version 2.0.0*
