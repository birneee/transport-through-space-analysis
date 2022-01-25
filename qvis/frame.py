from typing import Optional, Iterator


class Frame(object):
    inner: dict
    packet: 'packet.Packet'

    def __init__(self, inner: dict, packet: 'packet.Packet'):
        self.inner = inner
        self.packet = packet

    @property
    def type(self) -> str:
        return self.inner['frame_type']

    @property
    def time(self) -> float:
        """in seconds"""
        return self.packet.time


class AckFrame:
    base: Frame

    def __init__(self, base: Frame):
        self.base = base

    @property
    def acked_packet_numbers(self) -> Iterator[int]:
        for acked_range in self.base.inner.get("acked_ranges"):
            if len(acked_range) == 1:
                yield acked_range[0]
            elif len(acked_range) == 2:
                yield from range(int(acked_range[0]), int(acked_range[1])+1)
            else:
                raise Exception("invalid range")


class MaxStreamDataFrame:
    base: Frame

    def __init__(self, base: Frame):
        self.base = base

    @property
    def stream_id(self) -> int:
        return self.base.inner.get('stream_id')

    @property
    def maximum(self) -> int:
        return self.base.inner.get('maximum')


class StreamFrame(Frame):
    base: Frame

    def __init__(self, base: Frame):
        super().__init__(base.inner, base.packet)
        self.base = base

    @property
    def stream_id(self) -> int:
        return self.base.inner.get('stream_id')

    @property
    def offset(self) -> int:
        return self.base.inner.get('offset')

    @property
    def length(self) -> int:
        return self.base.inner.get('length')
