import statistics
from typing import List

import numpy as np

from qvis_qperf.report import Report


class AggregatedReport:
    reports: List[Report]

    def __init__(self, reports: List[Report]):
        self.reports = reports

    @property
    def time(self) -> float:
        """in seconds"""
        return statistics.mean(map(lambda r: r.time, self.reports))

    @property
    def avg_download_rate(self) -> float:
        """in bits per second"""
        return statistics.mean(map(lambda r: r.download_rate, self.reports))
