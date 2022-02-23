import statistics
from typing import List

import numpy as np

from qvis_qperf.report import Report


class AggregatedReport:
    reports: List[Report]

    def __init__(self, reports: List[Report]):
        self.reports = reports

    @property
    def avg_time(self) -> float:
        """in seconds"""
        return statistics.mean(map(lambda r: r.time, self.reports))

    @property
    def max_time(self) -> float:
        """in seconds"""
        return self.reports[-1].time

    @property
    def avg_download_rate(self) -> float:
        """in bits per second"""
        return statistics.mean(map(lambda r: r.download_rate, self.reports))

    @property
    def sum_bytes_received(self) -> int:
        """in bits per second"""
        return sum(map(lambda r: r.bytes_received, self.reports))

    @property
    def sum_packets_received(self) -> int:
        """in bits per second"""
        return sum(map(lambda r: r.packets_received, self.reports))

    def to_report(self, use_max_time: bool = False) -> Report:
        if use_max_time:
            return Report(self.max_time, self.avg_download_rate, self.sum_bytes_received, self.sum_packets_received)
        else:
            return Report(self.avg_time, self.avg_download_rate, self.sum_bytes_received, self.sum_packets_received)
