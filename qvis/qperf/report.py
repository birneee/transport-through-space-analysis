class Report:
    time: float
    """in seconds"""
    download_rate: float
    """in bits per second"""
    bytes_received: int
    packets_receive: int

    def __init__(self, time: float, download_rate: float, bytes_received: int, packets_received: int):
        self.time = time
        self.download_rate = download_rate
        self.bytes_received = bytes_received
        self.packets_receive = packets_received