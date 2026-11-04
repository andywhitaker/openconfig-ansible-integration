# nokia.openconfig.grpc plugin

**Persistent gRPC connection for OpenConfig gRPC services**

## Synopsis

* Provides a persistent gRPC channel, including TLS, to devices that implement OpenConfig gRPC services.
* Binds the gNMI service (Capabilities, Get, Set, Subscribe) as defined by gNMI specification 0.10.0, including the Depth, Commit (commit confirmed) and ConfigSubscription extensions.
* Binds OpenConfig gNOI services supported on Nokia SR OS and SR Linux (System, File, OS, FactoryReset, Healthz, BGP and Packet Link Qualification).
* Binds OpenConfig gNSI services supported on Nokia SR Linux (Authz, Certz, Pathz and Credentialz).
* OpenConfig gNMI specification <https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-specification.md>
* Option names follow [`ansible.netcommon.grpc`](https://docs.ansible.com/projects/ansible/latest/collections/ansible/netcommon/index.html) and the persistent connection conventions of `ansible.netcommon`.

## Connection Options

| Parameter | Type | Comments |
| --- | --- | --- |
| certificate_chain_file {#param-certificate-chain-file} | path | PEM encoded client certificate chain used for mutual TLS.<br/>**Variable:** `ansible_certificate_chain_file`<br/>**ini:** `[grpc_connection] certificate_chain_file`<br/>**Environment:** `ANSIBLE_CERTIFICATE_CHAIN_FILE` |
| gnmi_encoding {#param-gnmi-encoding} | any | Default gNMI encoding for Get, Set and Subscribe requests, either `JSON` or `JSON_IETF` (case-insensitive).<br/>If not set, a Capabilities request is sent when the connection is established and JSON_IETF is preferred over JSON.<br/>**Variable:** `ansible_gnmi_encoding`<br/>**ini:** `[grpc_connection] gnmi_encoding`<br/>**Environment:** `ANSIBLE_GNMI_ENCODING` |
| grpc_channel_options {#param-grpc-channel-options} | any | Key/value pairs (dict) of gRPC channel options.<br/>gRPC reference <https://grpc.github.io/grpc/core/group__grpc__arg__keys.html><br/>A string is parsed as YAML/JSON, so the value can be set in ansible.cfg.<br/>**Variable:** `ansible_grpc_channel_options`<br/>**ini:** `[grpc_connection] grpc_channel_options` |
| grpc_environment {#param-grpc-environment} | any | Key/value pairs (dict) of environment variables to set for the process that holds the gRPC channel. A value of `0`, `null` or empty string removes the variable.<br/>The standard Ansible `environment` keyword cannot be used, because it is not passed to the persistent connection process.<br/>Use `GRPC_VERBOSITY` and `GRPC_TRACE` for gRPC logging, `HTTPS_PROXY` for proxy settings, and `GRPC_SSL_CIPHER_SUITES` if the default TLS ciphers do not match the server.<br/>A string is parsed as YAML/JSON, so the value can be set in ansible.cfg.<br/>**Variable:** `ansible_grpc_environment`<br/>**ini:** `[grpc_connection] grpc_environment` |
| host {#param-host} | any | Target host FQDN or IP address to establish gRPC connection.<br/>IPv6 addresses can be given with or without brackets, for example `2001:db8::1` or `[2001:db8::1]`.<br/>**Default:** `inventory_hostname`<br/>**Variable:** `inventory_hostname`, `ansible_host` |
| password {#param-password} | any | Password used for gRPC authentication (metadata `password`).<br/>**Variable:** `ansible_password`, `ansible_ssh_pass` |
| persistent_command_timeout {#param-persistent-command-timeout} | int | Time in seconds to wait for a gRPC response. Also used as gRPC deadline for Capabilities, Get and Set.<br/>**Default:** `300`<br/>**Variable:** `ansible_command_timeout`<br/>**ini:** `[persistent_connection] command_timeout`<br/>**Environment:** `ANSIBLE_PERSISTENT_COMMAND_TIMEOUT` |
| persistent_connect_timeout {#param-persistent-connect-timeout} | int | Time in seconds to wait for the persistent connection to be established.<br/>**Default:** `5`<br/>**Variable:** `ansible_connect_timeout`<br/>**ini:** `[persistent_connection] connect_timeout`<br/>**Environment:** `ANSIBLE_PERSISTENT_CONNECT_TIMEOUT` |
| persistent_log_messages {#param-persistent-log-messages} | boolean | Log gRPC requests and responses to the Ansible `log_path`.<br/>Messages are not redacted.<br/>**Default:** `false`<br/>**Variable:** `ansible_persistent_log_messages`<br/>**ini:** `[persistent_connection] log_messages`<br/>**Environment:** `ANSIBLE_PERSISTENT_LOG_MESSAGES` |
| port {#param-port} | int | TCP port of the gRPC server on the remote device.<br/>**Default:** `57400`<br/>**Variable:** `ansible_port`<br/>**ini:** `[defaults] remote_port`<br/>**Environment:** `ANSIBLE_REMOTE_PORT` |
| private_key_file {#param-private-key-file} | path | PEM encoded private key used for mutual TLS client authentication.<br/>**Variable:** `ansible_private_key_file`<br/>**ini:** `[grpc_connection] private_key_file`<br/>**Environment:** `ANSIBLE_PRIVATE_KEY_FILE` |
| remote_user {#param-remote-user} | any | Username used for gRPC authentication (metadata `username`).<br/>Can be configured from the CLI via the `--user` or `-u` options.<br/>**Variable:** `ansible_user`<br/>**ini:** `[defaults] remote_user`<br/>**Environment:** `ANSIBLE_REMOTE_USER` |
| root_certificates_file {#param-root-certificates-file} | path | PEM encoded root certificates used to verify the server certificate.<br/>If no certificate option is set, an insecure (plain text) channel is used.<br/>**Variable:** `ansible_root_certificates_file`<br/>**ini:** `[grpc_connection] root_certificates_file`<br/>**Environment:** `ANSIBLE_ROOT_CERTIFICATES_FILE` |
| ssl_target_name_override {#param-ssl-target-name-override} | any | Overrides the host name used to verify the server certificate (gRPC channel option `grpc.ssl_target_name_override`).<br/>Needed when the address used to connect differs from the subject or subjectAltName in the device certificate.<br/>**Variable:** `ansible_grpc_ssl_target_name_override`<br/>**ini:** `[grpc_connection] ssl_target_name_override`<br/>**Environment:** `ANSIBLE_GRPC_SSL_TARGET_NAME_OVERRIDE` |
| validate_certs {#param-validate-certs} | boolean | When `false`, the server TLS certificate is trusted without a local CA (certificate pinning at connect time). A secure channel is still used.<br/>Use only in lab environments. When `true` (default), set `root_certificates_file` to your CA bundle for production.<br/>**Default:** `true`<br/>**Variable:** `ansible_grpc_validate_certs`<br/>**ini:** `[grpc_connection] validate_certs`<br/>**Environment:** `ANSIBLE_GRPC_VALIDATE_CERTS` |

*New in version 2.0.0*
