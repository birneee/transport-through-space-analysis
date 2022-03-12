from __future__ import annotations

import itertools
import os
import re
import statistics
from typing import List, Iterator, Optional

import numpy as np

from qvis_qperf.aggregated_report import AggregatedReport
from qvis_qperf.geometry import Point, Line, segments_intersection
from qvis_qperf.interception import BytesReceivedInterception
from qvis_qperf.report import Report

CLIENT_REPORT_REGEX = r'^[^\d\.]+(?P<time>\d+\.?\d*)[^\d\.]+(?P<rate>\d+\.?\d*)[^\d\.]+(?P<bytes>\d+)[^\d\.]+(?P<packets>\d+)$'

TIME_TO_FIRST_BYTE_REGEX = r'^[^\d\.]+time to first byte[^\d\.]+(?P<time>\d+\.?\d*)[^\d\.]+s$'

INTERNAL_ERROR_REGEX = r'^.*INTERNAL_ERROR: (?P<text>.*)$'


class Connection:
    time_to_first_byte: float
    reports: List[Report]
    internal_error: Optional[str]

    def __init__(self, file: str, add_zero_report: bool = True, max_s: float = float('inf')):
        """parse qvis_qperf output file"""
        self.reports = []
        self.internal_error = None
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
                match = re.match(INTERNAL_ERROR_REGEX, line)
                if match:
                    self.internal_error = str(match.group('text'))

    @property
    def mean_rate(self) -> float:
        """in bit per second"""
        return statistics.mean(map(lambda r: r.download_rate, self.reports))

    @property
    def max_time(self) -> float:
        """in seconds"""
        return self.reports[-1].time

    def reports_in_interval(self, start: float, end: float) -> List[Report]:
        reports = []
        for report in self.reports:
            if report.time >= end:
                break
            if start > report.time:
                continue
            reports.append(report)
        return reports

    def total_bytes_at(self, time: float) -> float:
        """time: in seconds"""
        """in bytes"""
        total = 0
        for report in self.reports:
            if report.time > time:
                break
            total += report.bytes_received
        return total

    def interceptions(self, other: Connection) -> Iterator[BytesReceivedInterception]:
        self_times = list(map(lambda r: r.time, self.reports))
        self_data = np.cumsum(list(map(lambda r: r.bytes_received, self.reports)))
        other_times = list(map(lambda r: r.time, other.reports))
        other_data = np.cumsum(list(map(lambda r: r.bytes_received, other.reports)))
        for self_index in range(0, len(self_times) - 1):
            for other_index in range(0, len(other_times) - 1):
                l1 = Line(Point(self_times[self_index], self_data[self_index]),
                          Point(self_times[self_index + 1], self_data[self_index + 1]))
                l2 = Line(Point(other_times[other_index], other_data[other_index]),
                          Point(other_times[other_index + 1], other_data[other_index + 1]))
                intersection = segments_intersection(l1, l2)
                if intersection is not None:
                    if intersection.positive:
                        yield BytesReceivedInterception(intersection.point.x, int(intersection.point.y), upper=self, lower=other)
                    else:
                        yield BytesReceivedInterception(intersection.point.x, int(intersection.point.y), upper=other, lower=self)

def load_all_connections(dir: str, file_extension: str = '.log', max_s: float = float('inf')) -> List[Connection]:
    connections: List[Connection] = []
    for file in os.listdir(dir):
        fe = os.path.splitext(file)[1]
        if fe == file_extension:
            connections.append(Connection(os.path.join(dir, file), max_s=max_s))
    return connections


def reduce_steps(connection: Connection | List[Connection], n=10, keep_zero=True) -> Connection | List[Connection]:
    if isinstance(connection, List):
        connections = connection
        return list(map(lambda c: reduce_steps(c, n, keep_zero), connections))
    new_connection = Connection.__new__(Connection)
    new_connection.time_to_first_byte = connection.time_to_first_byte
    new_connection.reports = []
    new_connection.internal_error = connection.internal_error
    if keep_zero:
        new_connection.reports.append(connection.reports[0])
    for i in range(1, len(connection.reports), n):
        new_connection.reports.append(AggregatedReport(connection.reports[i:i + n]).to_sum_report())
    return new_connection


def all_intersections(connections: List[Connection]) -> Iterator[BytesReceivedInterception]:
    for conn1, conn2 in itertools.combinations(connections, 2):
        for interception in conn1.interceptions(conn2):
            yield interception