# Playbooks

Workflow playbooks shipped with `nokia.openconfig`. Run them by name from any directory once the collection is installed:

```bash
ansible-playbook -i inventory.yml nokia.openconfig.<name> [-e variable=value ...]
```

They read the connection settings from your inventory, so they work for every router your inventory describes. Each playbook lists its variables in the comment at the top; `target` limits it to a host pattern. Reports, snapshots and backups are written below the directory you run `ansible-playbook` from.

| Playbook | What it does | Main variables | Output |
| --- | --- | --- | --- |
| `safe_config_change` | Backup, preview, optional approval, apply, verify; optionally as confirmed commit that is rolled back when the verification fails | `changes`, `verify`, `origin`, `use_confirmed_commit`, `approve` | `backup/` |
| `config_snapshot` | Saves the configuration and reports drift against the previous run; keeps a history per router | `snapshot_paths`, `origin`, `keep`, `fail_on_drift` | `snapshots/<host>/` |
| `lldp_neighbors` | Topology report from OpenConfig LLDP; checks the cabling against `expected_neighbors` | `expected_neighbors`, `fail_on_mismatch` | `reports/lldp_neighbors.{csv,json}` |
| `interface_health` | Reports interfaces that are admin up but oper down or have errors or discards | `interface_names`, `max_errors`, `max_discards`, `fail_on_issues` | `reports/interface_health.{csv,json}` |
| `reachability_check` | gNOI ping from every router to a list of destinations, with loss and round-trip times | `ping_destinations`, `ping_network_instance`, `max_loss_percent` | `reports/reachability.{csv,json}` |
| `os_upgrade` | gNOI OS install and activate, one router at a time, with configuration backup and version check | `os_image`, `os_version`, `batch_size` | `backup/` |
| `device_inventory` | Hardware and software inventory with gNMI version, encodings and models | — | `reports/device_inventory.{csv,json}` |

The read playbooks use the OpenConfig models with the origin `openconfig`. For routers that expect OpenConfig paths without origin, set `lldp_origin`, `interfaces_origin` or `inventory_origin` to `""`.

## Examples

`examples/` contains an inventory with group variables for Nokia SR Linux, Nokia SR OS, Cisco IOS XE, Cisco IOS XR and a generic gNMI router, and an example change for `safe_config_change`. Copy the directory to start:

```bash
cp -r ~/.ansible/collections/ansible_collections/nokia/openconfig/playbooks/examples my-network
cd my-network
ansible-playbook -i inventory.yml nokia.openconfig.device_inventory
ansible-playbook -i inventory.yml nokia.openconfig.safe_config_change -e @change.yml -e target=leaf1
```

See [Inventory Patterns](https://nokia-steward.github.io/openconfig-ansible-integration/getting-started/inventory-patterns/) for the group variables and [Examples](https://nokia-steward.github.io/openconfig-ansible-integration/examples/#shipped-playbooks) for more usage.
