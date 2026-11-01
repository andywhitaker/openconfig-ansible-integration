# -*- coding: utf-8 -*-
# (c) 2025 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause
#
"""Client and server classes corresponding to protobuf-defined gNMI services."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import grpc
from ansible_collections.nokia.openconfig.plugins.utils import gnmi_pb2 as gnmi__pb2


class gNMIStub:
    """gNMI client stub bound to a grpc.Channel."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Capabilities = channel.unary_unary(
            '/gnmi.gNMI/Capabilities',
            request_serializer=gnmi__pb2.CapabilityRequest.SerializeToString,
            response_deserializer=gnmi__pb2.CapabilityResponse.FromString,
        )
        self.Get = channel.unary_unary(
            '/gnmi.gNMI/Get',
            request_serializer=gnmi__pb2.GetRequest.SerializeToString,
            response_deserializer=gnmi__pb2.GetResponse.FromString,
        )
        self.Set = channel.unary_unary(
            '/gnmi.gNMI/Set',
            request_serializer=gnmi__pb2.SetRequest.SerializeToString,
            response_deserializer=gnmi__pb2.SetResponse.FromString,
        )
        self.Subscribe = channel.stream_stream(
            '/gnmi.gNMI/Subscribe',
            request_serializer=gnmi__pb2.SubscribeRequest.SerializeToString,
            response_deserializer=gnmi__pb2.SubscribeResponse.FromString,
        )


class gNMIServicer:
    """Base servicer class for gNMI server implementations."""

    def Capabilities(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Get(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Set(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Subscribe(self, request_iterator, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_gNMIServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'Capabilities': grpc.unary_unary_rpc_method_handler(
            servicer.Capabilities,
            request_deserializer=gnmi__pb2.CapabilityRequest.FromString,
            response_serializer=gnmi__pb2.CapabilityResponse.SerializeToString,
        ),
        'Get': grpc.unary_unary_rpc_method_handler(
            servicer.Get,
            request_deserializer=gnmi__pb2.GetRequest.FromString,
            response_serializer=gnmi__pb2.GetResponse.SerializeToString,
        ),
        'Set': grpc.unary_unary_rpc_method_handler(
            servicer.Set,
            request_deserializer=gnmi__pb2.SetRequest.FromString,
            response_serializer=gnmi__pb2.SetResponse.SerializeToString,
        ),
        'Subscribe': grpc.stream_stream_rpc_method_handler(
            servicer.Subscribe,
            request_deserializer=gnmi__pb2.SubscribeRequest.FromString,
            response_serializer=gnmi__pb2.SubscribeResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'gnmi.gNMI', rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
