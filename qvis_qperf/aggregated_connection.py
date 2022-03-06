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

    def total_bytes_at(self, time: float) -> float:
        """time: in seconds"""
        """in bytes"""
        return statistics.mean(map(lambda c: c.total_bytes_at(time), self.connections))

    @property
    def mean_rate(self) -> float:
        """in bit per second"""
        return statistics.mean(map(lambda c: c.mean_rate, self.connections))

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

    def to_connection(self, use_max_time: bool = False) -> Connection:
        connection = Connection.__new__(Connection)
        connection.time_to_first_byte = self.time_to_first_byte
        connection.reports = list(map(lambda r: r.to_report(use_max_time=use_max_time), self.reports))
        return connection

    def interceptions(self, other: Connection | AggregatedConnection) -> Iterator[BytesReceivedInterception]:
        if isinstance(other, AggregatedConnection):
            return self.to_connection().interceptions(other.to_connection())
        elif isinstance(other, Connection):
            return self.to_connection().interceptions(other)
        else:
            raise "unsupported type"
