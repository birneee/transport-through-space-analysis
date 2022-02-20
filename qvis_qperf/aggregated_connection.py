import statistics
from typing import List, Iterator

from qvis_qperf.aggregated_report import AggregatedReport
from qvis_qperf.connection import Connection


class AggregatedConnection:
    connections: List[Connection]

    def __init__(self, connections: List[Connection]):
        self.connections = connections

    @property
    def time_to_first_byte(self) -> float:
        """in seconds"""
        return statistics.mean(map(lambda c: c.time_to_first_byte, self.connections))

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
                reports.append(connection.reports[index])
            yield AggregatedReport(reports)
