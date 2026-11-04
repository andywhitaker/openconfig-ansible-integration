# Support

The Nokia OpenConfig Ansible Collection is an open-source project led by Nokia. It is published under the [nokia-steward](https://github.com/nokia-steward) organization on GitHub and is actively maintained.

The collection is a community project. There is no commercial support and no service level agreement (SLA). Help comes from the documentation, the maintainers and the community, and contributions from third parties are welcome. See the [Community Guide](guides/community-guide.md) to get involved.

## Getting help

- [Documentation](index.md) — installation, guides and the [module reference](reference/index.md)
- [GitHub Issues](https://github.com/nokia-steward/openconfig-ansible-integration/issues) — bugs and questions
- [Ansible Galaxy](https://galaxy.ansible.com/ui/repo/published/nokia/openconfig/) — released versions

## Before production

Production networks bring challenges that a lab does not show. Test your playbooks on lab routers or in a [containerlab](https://containerlab.dev) topology first:

- Idempotency: do repeated runs produce the same result?
- Check mode: does the preview of [`gnmi_set`](reference/nokia.openconfig.gnmi_set.md) match the intended change?
- Error handling: are RPC errors, timeouts and rejected commits handled?
- Scale: do message sizes, subscription durations and the number of concurrent hosts work at production scale?

## Reporting issues

- Bugs: open a [GitHub Issue](https://github.com/nokia-steward/openconfig-ansible-integration/issues) with the Ansible, collection and Python versions, the router platform and release, the connection settings without passwords, and the failing task output.
- Features: open an issue that describes the use case.
- Security: do not open a public issue. Use [GitHub Security Advisories](https://github.com/nokia-steward/openconfig-ansible-integration/security/advisories) instead.

---

Questions? Start with the [User Guide](guides/user-guide.md) or open an [issue](https://github.com/nokia-steward/openconfig-ansible-integration/issues).
