from __future__ import annotations
import gzip
import math

import ujson as json
import time
from collections import deque
from typing import Iterator, Optional, TextIO

import numpy as np
import pandas as pd

from . import event_names, frame_types
from .packet import Packet
from .event import Event
from .frame import Frame, MaxStreamDataFrame, StreamFrame
from .recovery import MetricsUpdated


def read_qlog(filepath: str, max_ms: float = math.inf) -> Connection:
    start = time.time()
    if filepath.endswith('.gz'):
        with gzip.open(filepath) as file:
            conn = parse_qlog(file, max_ms)
    else:
        with open(filepath) as file:
            conn = parse_qlog(file, max_ms)
    print(f'loaded {filepath} in {time.time() - start}s')
    return conn


def parse_qlog(reader: TextIO, max_ms: float = math.inf) -> Connection:
    qlog_info = json.loads(next(reader))
    raw_events = []
    sent_packet_numbers: dict[int, int] = {}  # packet_number, index in events
    received_packet_numbers: dict[int, int] = {}  # packet_number, index in events
    for index, line in enumerate(reader):
        event = json.loads(line)
        if event['time'] > max_ms:
            break
        raw_events.append(event)
        match event['name']:
            case event_names.TRANSPORT_PACKET_SENT:
                sent_packet_numbers[event['data']['header']['packet_number']] = index
            case event_names.TRANSPORT_PACKET_RECEIVED:
                received_packet_numbers[event['data']['header']['packet_number']] = index
            # for frame in p.frames:
            #     if frame.type == "ack":
            #         ack_frame = AckFrame(frame)
            #         for ack in ack_frame.acked_packet_numbers:
            #             ''
            # if ack not in self.received_acks:  # if not already marked as acked
            #     self.received_acks[ack] = event.index
    conn = Connection(qlog_info, raw_events, sent_packet_numbers, received_packet_numbers)
    return conn


class Connection:
    """A QLOG QUIC Connection"""
    qlog_info: dict
    raw_events: list[dict]
    sent_packet_numbers: dict[int, int] = {}  # packet_number, index in events
    received_packet_numbers: dict[int, int] = {}  # packet_number, index in events

    # received_acks: dict[int, int] = {}  # acked packet_number, index in events

    def __init__(self, qlog_info: dict, raw_events: list[dict], sent_packet_numbers: dict[int, int],
                 received_packet_numbers: dict[int, int]):
        self.qlog_info: qlog_info
        self.raw_events = raw_events
        self.sent_packet_numbers = sent_packet_numbers
        self.received_packet_numbers = received_packet_numbers

    @property
    def events(self) -> Iterator[Event]:
        for raw_event in self.raw_events:
            yield Event(raw_event, self)

    def events_of_type(self, name: str) -> Iterator[Event]:
        return filter(lambda e: e.name == name, self.events)

    @property
    def sent_packets(self) -> Iterator[Packet]:
        for event in self.events:
            if event.name == event_names.TRANSPORT_PACKET_SENT:
                yield Packet(event)

    def receivedPackets(self) -> Iterator[Packet]:
        for event in self.events:
            if event.name == event_names.TRANSPORT_PACKET_RECEIVED:
                yield Packet(event)

    def sentFrames(self) -> Iterator[Frame]:
        for packet in self.sent_packets:
            for frame in packet.frames:
                yield frame

    def sent_frames_of_type(self, frame_type: str) -> Iterator[Frame]:
        return filter(lambda f: f.type == frame_type, self.sentFrames())

    @property
    def sent_stream_frames(self) -> Iterator[StreamFrame]:
        return map(lambda f: StreamFrame(f), self.sent_frames_of_type(frame_types.STREAM))

    def sent_stream_frames_of_stream(self, stream_id: int) -> Iterator[StreamFrame]:
        return filter(lambda f: f.stream_id == stream_id, self.sent_stream_frames)

    @property
    def received_frames(self) -> Iterator[Frame]:
        for packet in self.receivedPackets():
            for frame in packet.frames:
                yield frame

    def received_frames_of_type(self, frame_type: str) -> Iterator[Frame]:
        return filter(lambda f: f.type == frame_type, self.received_frames)


    def stream_flow_limit_sum_updates(self) -> Iterator[tuple[float, int]]:
        """sum of all stream flow limits"""
        """time in seconds, maximum in bytes"""
        yield 0, self.remote_initial_max_stream_data_bidi_remote
        stream_limits: dict[int, int] = {}
        for frame in self.received_frames:
            match frame.type:
                case frame_types.MAX_STREAM_DATA:
                    max_stream_data_frame = MaxStreamDataFrame(frame)
                    stream_limits[max_stream_data_frame.stream_id] = max_stream_data_frame.maximum
                    yield frame.time, sum(stream_limits.values())

    def stream_flow_limit_updates(self, stream_id: int) -> Iterator[tuple[float, int]]:
        """time in seconds, maximum in bytes"""
        yield 0, self.remote_initial_max_stream_data_bidi_remote
        for frame in self.received_frames:
            match frame.type:
                case frame_types.MAX_STREAM_DATA:
                    max_stream_data_frame = MaxStreamDataFrame(frame)
                    yield frame.time, max_stream_data_frame.maximum

    def connection_flow_limit_updates(self) -> Iterator[tuple[float, int]]:
        """time in seconds, maximum in bytes"""
        for frame in self.received_frames:
            if frame.type == frame_types.MAX_DATA:
                yield frame.time, frame.inner['maximum']

    @property
    def remote_parameters(self) -> dict:
        for event in self.events:
            if event.name == event_names.TRANSPORT_PARAMETERS_SET:
                data = event.data
                if data is not None:
                    owner = data.get('owner')
                    if owner == 'remote':
                        return data
        return {}

    @property
    def remote_initial_max_data(self) -> Optional[int]:
        """in bytes"""
        return self.remote_parameters.get('initial_max_data')

    @property
    def remote_initial_max_stream_data_bidi_remote(self) -> Optional[int]:
        """in bytes"""
        return self.remote_parameters.get('initial_max_stream_data_bidi_remote')

    @property
    def bytes_in_flight_updates(self) -> Iterator[tuple[float, int]]:
        """time in seconds, bytes in flight"""
        for event in self.events_of_type(event_names.RECOVERY_METRICS_UPDATED):
            metrics_updated = MetricsUpdated(event)
            bytes_in_flight = metrics_updated.bytes_in_flight
            if bytes_in_flight is not None:
                yield event.time, bytes_in_flight

    @property
    def max_time(self) -> float:
        return self.raw_events[-1]["time"]

    @property
    def congestion_window_updates(self) -> Iterator[tuple[float, int]]:
        """time in seconds, maximum in bytes"""
        """"""
        for event in self.events_of_type(event_names.RECOVERY_METRICS_UPDATED):
            metrics_updated = MetricsUpdated(event)
            congestion_window = metrics_updated.congestion_window
            if congestion_window is not None:
                yield event.time, congestion_window
