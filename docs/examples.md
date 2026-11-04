# Examples

The playbooks below are part of the integration test suite in [`tests/playbooks/`](https://github.com/nokia-steward/openconfig-ansible-integration/tree/main/tests/playbooks). Each one runs against Nokia SR OS, SR Linux or both, and can be used as a template for your own playbooks.

The Platform column names the routers a playbook runs on. Playbooks for both platforms take their native YANG paths from the group variables [`nokia_srsim.yml`](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/group_vars/nokia_srsim.yml) and [`nokia_srlinux.yml`](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/group_vars/nokia_srlinux.yml). Playbooks marked OpenConfig use the OpenConfig paths in [`model_oc.yml`](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/vars/model_oc.yml); OpenConfig must be enabled on the router.

## gNMI

| Playbook | Platform | Description |
| --- | --- | --- |
| [gNMI_Capabilities.yml](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/gNMI_Capabilities.yml) | SR OS, SR Linux | Capabilities and encoding checks |
| [gNMI_GetConfig.yml](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/gNMI_GetConfig.yml) | SR OS, SR Linux | Get of configuration |
| [gNMI_SubscribeOnce.yml](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/gNMI_SubscribeOnce.yml) | SR OS, SR Linux | Subscribe in ONCE mode |
| [gNMI_Backup.yml](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/gNMI_Backup.yml) | SR OS, SR Linux | Set with `backup: true` |
| [gNMI_Depth.yml](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/gNMI_Depth.yml) | SR OS, SR Linux | Depth extension on Get and Subscribe |
| [gNMI_CommitConfirmed.yml](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/gNMI_CommitConfirmed.yml) | SR OS, SR Linux | Confirmed commit: confirm, rollback, extend and cancel |
| [gNMI_ConfigSubscription.yml](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/gNMI_ConfigSubscription.yml) | SR OS, SR Linux | ConfigSubscription extension, in ONCE mode on SR Linux and STREAM mode on both |
| [gNMI_GetConfig_OC.yml](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/gNMI_GetConfig_OC.yml) | SR OS, SR Linux (OpenConfig) | Get of LLDP configuration and state |
| [gNMI_Config_OC.yml](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/gNMI_Config_OC.yml) | SR OS, SR Linux (OpenConfig) | Set of LLDP `config/enabled` |
| [gNMI_Subscribe_OC.yml](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/gNMI_Subscribe_OC.yml) | SR OS, SR Linux (OpenConfig) | Interface counters in SAMPLE mode |
| [gNMI_Config_SROS.yml](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/gNMI_Config_SROS.yml) | SR OS | Update, replace and delete in one transaction under `/configure` |
| [gNMI_Subscribe_SROS.yml](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/gNMI_Subscribe_SROS.yml) | SR OS | State and configuration subscriptions |
| [gNMI_SubscribeOnce_SROS.yml](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/gNMI_SubscribeOnce_SROS.yml) | SR OS | Subscribe in ONCE mode to native paths |
| [gNMI_Config_SRL.yml](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/gNMI_Config_SRL.yml) | SR Linux | Configuration changes |
| [gNMI_Subscribe_SRL.yml](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/gNMI_Subscribe_SRL.yml) | SR Linux | State and configuration subscriptions |
| [gNMI_Restore_SRL.yml](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/gNMI_Restore_SRL.yml) | SR Linux | Backup, change and full restore with `replace` on `/` |

## gNOI and gNSI

| Playbook | Platform | Description |
| --- | --- | --- |
| [gNOI_System.yml](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/gNOI_System.yml) | SR OS, SR Linux | Time, Ping and Traceroute |
| [gNOI_File.yml](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/gNOI_File.yml) | SR OS, SR Linux | Put, Stat, Get and Remove round trip |
| [gNOI_Healthz_SRL.yml](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/gNOI_Healthz_SRL.yml) | SR Linux | Healthz List and Get |
| [gNSI_Validate_SRL.yml](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks/gNSI_Validate_SRL.yml) | SR Linux | Authz, Certz, Pathz and Credentialz, including a Certz profile add and delete |

## Running the integration tests

The test runner groups the playbooks into categories, defined in [`tests/playbooks.yml`](https://github.com/nokia-steward/openconfig-ansible-integration/blob/main/tests/playbooks.yml), for example `common`, `sros`, `srlinux`, `gnoi` and `gnsi`. To run them in a containerlab topology:

```bash
cd tests
./run.sh deploy                  # deploy the containerlab topology
./run.sh run --category common   # run one category
./run.sh destroy
```

The default `tests/ansible.cfg` uses the containerlab inventory under `tests/clab-ansible/`, generated on deploy. For physical lab routers, use a private inventory, for example under `tests/clab-lab/` (gitignored), and `ANSIBLE_CONFIG=tests/ansible_lab.cfg`.

See also the [Quick Start](getting-started/quick-start.md) and the [User Guide](guides/user-guide.md).
