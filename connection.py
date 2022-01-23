from __future__ import annotations
import gzip
import json
from typing import Iterator, Optional
import pandas as pd
from frame import Frame
import packet

def read_qlog(filepath: str) -> Connection:
    if filepath.endswith('.gz'):
        with gzip.open(filepath) as file:
            conn = Connection(
                json.loads(file.readline()),
                pd.read_json(file, lines=True))
    else:
        with open(filepath) as file:
            conn = Connection(
                json.loads(file.readline()),
                pd.read_json(file, lines=True))
    conn.df['time'] = conn.df['time'].apply(lambda t: t / 1000) # from ms to s
    return conn

class Connection:
    """A QLOG QUIC Connection"""
    qlog_info: dict
    df: pd.DataFrame

    def __init__(self, qlog_info: dict, df: pd.DataFrame):
        self.qlog_info: qlog_info
        self.df = df

    def sentPackets(self) -> Iterator[packet.Packet]:
        for row in self.df.itertuples():
            name = getattr(row, 'name')
            if name == 'transport:packet_sent':
                yield packet.Packet(row)

    def receivedPackets(self) -> Iterator[packet.Packet]:
        for row in self.df.itertuples():
            name = getattr(row, 'name')
            if name == 'transport:packet_received':
                yield packet.Packet(row)

    def sentFrames(self) -> Iterator[Frame]:
        for packet in self.sentPackets():
            for frame in packet.frames():
                yield frame

    def receivedFrames(self) -> Iterator[Frame]:
        for packet in self.receivedPackets():
            for frame in packet.frames():
                yield frame

    def connection_flow_limit_updates(self) -> Iterator[tuple[float, int]]:
        """time in seconds, maximum in bytes"""
        for frame in self.receivedFrames():
            if frame.type() == 'max_data':
                yield (frame.time(), frame.inner['maximum'])