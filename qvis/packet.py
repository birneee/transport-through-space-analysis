from __future__ import annotations
from typing import Iterator, Optional

from .event import Event
from .frame import Frame


class Packet:
    event: Event

    def __init__(self, event: Event):
        self.event = event

    @property
    def time(self) -> float:
        """in seconds"""
        return self.event.time

    @property
    def header(self) -> dict:
        return self.event.data.get('header')

    @property
    def packet_number(self) -> int:
        return self.header.get('packet_number')

    @property
    def raw_length(self) -> int:
        return self.event.data['raw']['length']

    @property
    def frames(self) -> Iterator['Frame']:
        data = self.event.data
        if data is None:
            return
        frames = data.get('frames')
        if frames is None:
            return
        for frame in frames:
            yield Frame(frame, self)

    @property
    def corresponding_ack(self) -> Optional[Packet]:
        return self.event.connection.received_ack.get(self.packet_number)
