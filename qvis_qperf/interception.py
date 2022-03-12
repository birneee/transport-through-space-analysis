
class BytesReceivedInterception:
    time: float
    bytes_received: int
    upper: 'Connection'
    lower: 'Connection'

    def __init__(self, time: float, bytes_received: int, upper: 'Connection', lower: 'Connection'):
        self.time = time
        self.bytes_received = bytes_received
        self.upper = upper
        self.lower = lower
