from typing import Optional

class Frame:
    inner: dict
    packet: 'packet.Packet'

    def __init__(self, inner: dict, packet: 'packet.Packet'):
        self.inner = inner
        self.packet = packet

    def type(self) -> str:
        return self.inner['frame_type']

    def length(self) -> Optional[str]:
        return self.inner.get('length')

    def time(self) -> float:
        """in seconds"""
        return self.packet.time()
