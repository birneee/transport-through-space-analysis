from __future__ import annotations
import logging
import statistics
from typing import List, Iterator

from qvis_qperf.aggregated_report import AggregatedReport
from qvis_qperf.connection import Connection
from qvis_qperf.interception import BytesReceivedInterception


class AggregatedConnection:
    connections: List[Connection]

    def __init__(self, connections: List[Connection]):
        self.connections = connections

    @property
    def time_to_first_byte(self) -> float:
        """in seconds"""
        return statistics.mean(map(lambda c: c.time_to_first_byte, self.connections))

    @property
    def establishment_time(self) -> float:
        """in seconds"""
        return statistics.mean(map(lambda c: c.establishment_time, self.connections))

    def total_bytes_at(self, time: float) -> float:
        """time: in seconds"""
        """in bytes"""
        return statistics.mean(map(lambda c: c.total_received_bytes_at(time), self.connections))

    def mean_rate(self, exclude_zero_report: bool = True, start_time: float = 0) -> float:
        """in bit per second"""
        return statistics.mean(
            map(lambda c: c.mean_rate(exclude_zero_report=exclude_zero_report, start_time=start_time),
                self.connections))

    @property
    def ramp_up_time_from_start(self) -> float:
        """!!! very inaccurate, searches for first rate drop
        in seconds"""
        return statistics.mean(
            map(lambda c: c.ramp_up_time_from_start,
                self.connections))

    @property
    def ramp_up_time_from_ttfb(self) -> float:
        """!!! very inaccurate, searches for first rate drop
        in seconds"""
        return statistics.mean(
            map(lambda c: c.ramp_up_time_from_ttfb,
                self.connections))

    @property
    def mean_rate_after_ramp_up(self) -> float:
        """!!! very inaccurate, searches for first rate drop
        in bit per second"""
        return statistics.mean(
            map(lambda c: c.mean_rate_after_ramp_up,
                self.connections))

    @property
    def reports(self) -> Iterator[AggregatedReport]:
        num_reports = len(self.connections[0].reports)
        for index in range(num_reports):
            reports = []
            for connection in self.connections:
                try:
                    reports.append(connection.reports[index])
                except:
                    logging.warning(f'no report at index {index}')
            yield AggregatedReport(reports)

    def to_avg_connection(self) -> Connection:
        connection = Connection.__new__(Connection)
        connection.establishment_time = self.establishment_time
        connection.time_to_first_byte = self.time_to_first_byte
        connection.reports = list(map(lambda r: r.to_avg_report(), self.reports))
        return connection

    def interceptions(self, other: Connection | AggregatedConnection) -> Iterator[BytesReceivedInterception]:
        if isinstance(other, AggregatedConnection):
            return self.to_avg_connection().intersections(other.to_avg_connection())
        elif isinstance(other, Connection):
            return self.to_avg_connection().intersections(other)
        else:
            raise "unsupported type"

    def reduce_steps(self, n:int) -> AggregatedConnection:
        return AggregatedConnection(list(map(lambda c: c.reduce_steps(n), self.connections)))
