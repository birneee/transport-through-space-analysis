import os
import re
import statistics
from typing import List

from qvis_qperf.report import Report

CLIENT_REPORT_REGEX = r'^[^\d\.]+(?P<time>\d+\.?\d*)[^\d\.]+(?P<rate>\d+\.?\d*)[^\d\.]+(?P<bytes>\d+)[^\d\.]+(?P<packets>\d+)$'

TIME_TO_FIRST_BYTE_REGEX = r'^[^\d\.]+time to first byte[^\d\.]+(?P<time>\d+\.?\d*)[^\d\.]+s$'

class Connection:
    time_to_first_byte: float
    reports: List[Report]

    def __init__(self, file: str, add_zero_report: bool = True, max_s: float = float('inf')):
        """parse qvis_qperf output file"""
        self.reports = []
        with open(file) as file:
            for line in file:
                match = re.match(CLIENT_REPORT_REGEX, line)
                if match:
                    time = float(match.group('time')) + self.time_to_first_byte
                    if time <= max_s:
                        self.reports.append(Report(
                            time,
                            float(match.group('rate')),
                            int(match.group('bytes')),
                            int(match.group('packets')),
                        ))
                    continue
                match = re.match(TIME_TO_FIRST_BYTE_REGEX, line)
                if match:
                    self.time_to_first_byte = float(match.group('time'))
                    if add_zero_report:
                        self.reports.append(Report(self.time_to_first_byte, 0, 0, 0))
                    continue

    @property
    def mean_rate(self) -> float:
        """in bit per second"""
        return statistics.mean(map(lambda r: r.download_rate, self.reports))

    def total_bytes_at(self, time: float) -> float:
        """time: in seconds"""
        """in bytes"""
        total = 0
        for report in self.reports:
            if report.time > time:
                break
            total += report.bytes_received
        return total


def load_all_connections(dir: str, file_extension: str = '.log', max_s: float = float('inf')) -> List[Connection]:
    connections: List[Connection] = []
    for file in os.listdir(dir):
        fe = os.path.splitext(file)[1]
        if fe == file_extension:
            connections.append(Connection(os.path.join(dir, file), max_s))
    return connections
