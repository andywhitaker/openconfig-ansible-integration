# (c) 2026 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause
#

"""In-process gNMI 0.10.0 server used by the connection plugin unit tests."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json
import time
from concurrent import futures

import grpc

from ansible_collections.nokia.openconfig.plugins.module_utils.proto import gnmi_ext_pb2
from ansible_collections.nokia.openconfig.plugins.module_utils.proto import gnmi_pb2
from ansible_collections.nokia.openconfig.plugins.module_utils.proto import gnmi_pb2_grpc


def _json(value):
    return gnmi_pb2.TypedValue(json_ietf_val=json.dumps(value).encode())


def _path(*names, **keys):
    elems = [gnmi_pb2.PathElem(name=n) for n in names]
    if keys:
        elems[-1].key.update(keys)
    return gnmi_pb2.Path(elem=elems)


class FakeGnmi(gnmi_pb2_grpc.gNMIServicer):

    def __init__(self):
        self.requests = []
        self.metadata = []

    def _record(self, request, context):
        self.requests.append(request)
        self.metadata.append(dict(context.invocation_metadata()))

    def Capabilities(self, request, context):
        self._record(request, context)
        return gnmi_pb2.CapabilityResponse(
            supported_models=[gnmi_pb2.ModelData(name='openconfig-interfaces', organization='OpenConfig', version='3.0.0')],
            supported_encodings=[gnmi_pb2.JSON, gnmi_pb2.JSON_IETF, gnmi_pb2.ASCII],
            gNMI_version='0.10.0',
        )

    def Get(self, request, context):
        self._record(request, context)
        notification = gnmi_pb2.Notification(
            timestamp=1700000000000000000,
            update=[
                gnmi_pb2.Update(path=_path('interface', name='ethernet-1/1'),
                                val=_json({'description': 'uplink', 'admin-state': 'enable'})),
            ],
        )
        extension = [gnmi_ext_pb2.Extension(depth=e.depth) for e in request.extension if e.HasField('depth')]
        return gnmi_pb2.GetResponse(notification=[notification], extension=extension)

    def Set(self, request, context):
        self._record(request, context)
        response = gnmi_pb2.SetResponse(timestamp=1700000000000000000)
        for path in request.delete:
            response.response.add(path=path, op=gnmi_pb2.UpdateResult.DELETE)
        for upd in request.replace:
            response.response.add(path=upd.path, op=gnmi_pb2.UpdateResult.REPLACE)
        for upd in request.update:
            response.response.add(path=upd.path, op=gnmi_pb2.UpdateResult.UPDATE)
        if any(e.HasField('commit') and e.commit.id == 'reject' for e in request.extension):
            context.abort(grpc.StatusCode.FAILED_PRECONDITION, 'commit reject in progress')
        response.extension.extend(request.extension)
        return response

    def Subscribe(self, request_iterator, context):
        request = next(request_iterator, None)
        if request is None:
            return
        self._record(request, context)
        config = any(e.HasField('config_subscription') for e in request.extension)

        def update(n):
            return gnmi_pb2.SubscribeResponse(update=gnmi_pb2.Notification(
                timestamp=1700000000000000000 + n,
                prefix=_path('interface', name='ethernet-1/1'),
                update=[gnmi_pb2.Update(path=_path('description'), val=gnmi_pb2.TypedValue(string_val='uplink-%d' % n))],
            ))

        def done(commit_id, final):
            return gnmi_pb2.SubscribeResponse(extension=[gnmi_ext_pb2.Extension(
                config_subscription=gnmi_ext_pb2.ConfigSubscription(
                    sync_done=gnmi_ext_pb2.ConfigSubscriptionSyncDone(
                        commit_confirm_id=commit_id, server_commit_id='srv-1', done=final)))])

        yield update(0)
        if config:
            yield done('', True)
        yield gnmi_pb2.SubscribeResponse(sync_response=True)

        mode = request.subscribe.mode
        if mode == gnmi_pb2.SubscriptionList.POLL:
            poll = next(request_iterator, None)
            if poll is None:
                return
            self.requests.append(poll)
            yield update(1)
            yield gnmi_pb2.SubscribeResponse(sync_response=True)
        elif mode == gnmi_pb2.SubscriptionList.STREAM:
            n = 1
            while context.is_active():
                time.sleep(0.05)
                yield update(n)
                if config and n == 3:
                    yield done('c1', True)
                n += 1


class Server:

    def __init__(self, address='127.0.0.1'):
        self.servicer = FakeGnmi()
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
        gnmi_pb2_grpc.add_gNMIServicer_to_server(self.servicer, self.server)
        self.port = self.server.add_insecure_port('[%s]:0' % address if ':' in address else '%s:0' % address)

    def __enter__(self):
        self.server.start()
        return self

    def __exit__(self, *args):
        self.server.stop(0)
