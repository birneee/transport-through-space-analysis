from typing import Optional


class BytesReceivedInterception:
    time: float
    bytes_received: int
    positive: Optional[bool]

    def __init__(self, time: float, bytes_received: int, positive: Optional[bool] = None):
        self.time = time
        self.bytes_received = bytes_received
        self.positive = positive
