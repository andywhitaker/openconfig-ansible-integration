# (c) 2026 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause
#

"""
Builders and parsers for the well-known gNMI extensions (gnmi_ext.proto,
gNMI 0.10.0): Depth, Commit (commit confirmed) and ConfigSubscription.

Builders return the dict form of gnmi_ext.Extension using protobuf field
names, ready for google.protobuf.json_format.ParseDict.
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re

from ansible_collections.nokia.openconfig.plugins.module_utils.gnmi import (
    GnmiError,
    duration_to_proto,
    parse_duration,
)


def depth(level):
    """Depth extension. Level 0 means no limit, so no extension is sent."""
    if level is None or int(level) == 0:
        return None
    if int(level) < 0:
        raise GnmiError("depth must be zero or positive")
    return {'depth': {'level': int(level)}}


def _commit(commit_id, action, payload):
    if not commit_id:
        raise GnmiError("commit_id is required for commit confirmed operations")
    return {'commit': {'id': str(commit_id), action: payload}}


def commit_request(commit_id, duration=None):
    """Starts a confirmed commit, optionally with a rollback duration."""
    payload = {}
    if duration is not None:
        payload['rollback_duration'] = duration_to_proto(parse_duration(duration))
    return _commit(commit_id, 'commit', payload)


def commit_confirm(commit_id):
    """Confirms an in-progress confirmed commit."""
    return _commit(commit_id, 'confirm', {})


def commit_cancel(commit_id):
    """Cancels (rolls back) an in-progress confirmed commit."""
    return _commit(commit_id, 'cancel', {})


def set_rollback_duration(commit_id, duration):
    """Changes the rollback duration of an in-progress confirmed commit."""
    return _commit(commit_id, 'set_rollback_duration',
                   {'rollback_duration': duration_to_proto(parse_duration(duration))})


def commit_extension(commit_id=None, commit_request_=False, commit_confirm_=False,
                     commit_cancel_=False, rollback_duration=None):
    """
    Maps the commit options (commit_id, commit_request, commit_confirm,
    commit_cancel, rollback_duration) to a single Commit extension.
    """
    actions = [a for a in (commit_request_, commit_confirm_, commit_cancel_) if a]
    if len(actions) > 1:
        raise GnmiError("commit_request, commit_confirm and commit_cancel are mutually exclusive")
    if commit_request_:
        return commit_request(commit_id, rollback_duration)
    if commit_confirm_:
        return commit_confirm(commit_id)
    if commit_cancel_:
        return commit_cancel(commit_id)
    if rollback_duration is not None:
        return set_rollback_duration(commit_id, rollback_duration)
    if commit_id:
        raise GnmiError("commit_id needs one of commit_request, commit_confirm, commit_cancel or rollback_duration")
    return None


def config_subscription_start():
    """ConfigSubscription extension to subscribe to config nodes only."""
    return {'config_subscription': {'start': {}}}


_CAMEL = re.compile(r'(?<!^)(?=[A-Z])')


def _snake(data):
    if isinstance(data, dict):
        return dict((_CAMEL.sub('_', k).lower(), _snake(v)) for k, v in data.items())
    if isinstance(data, list):
        return [_snake(v) for v in data]
    return data


def parse_extensions(extensions):
    """
    Normalizes response extensions (dict form, camelCase or snake_case) to
    protobuf field names, e.g. config_subscription.sync_done.commit_confirm_id.
    """
    return [_snake(ext) for ext in extensions or []]


def sync_done(extensions):
    """Returns the ConfigSubscriptionSyncDone payload if present, else None."""
    for ext in parse_extensions(extensions):
        done = ext.get('config_subscription', {}).get('sync_done')
        if done is not None:
            return done
    return None
