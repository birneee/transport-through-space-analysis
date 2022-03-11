import statistics
from typing import List

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
        return sum(map(lambda r: r.bytes_received, self.reports))

    @property
    def avg_bytes_received(self) -> float:
        return statistics.mean(map(lambda r: r.bytes_received, self.reports))

    @property
    def sum_packets_received(self) -> int:
        return sum(map(lambda r: r.packets_received, self.reports))

    @property
    def avg_packets_received(self) -> float:
        return statistics.mean(map(lambda r: r.packets_received, self.reports))

    def to_sum_report(self) -> Report:
        """the returned report is a report with the summed bytes and packets received"""
        return Report(self.max_time, self.avg_download_rate, int(self.sum_bytes_received),
                      int(self.sum_packets_received))

    def to_avg_report(self) -> Report:
        """the returned report is a report with the average bytes and packets received"""
        return Report(self.avg_time, self.avg_download_rate, int(self.avg_bytes_received),
                      int(self.avg_packets_received))
