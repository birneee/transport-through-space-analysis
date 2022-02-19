from typing import List

import numpy as np

from qvis_qperf.report import Report


class AggregatedReport:
    reports: List[Report]

    def __init__(self, reports: List[Report]):
        self.reports = reports

    @property
    def time(self) -> int:
        """in full seconds"""
        time = round(self.reports[0].time)
        for report in self.reports:
            if round(report.time) != time:
                raise "report time does not match"
        return time

    @property
    def avg_download_rate(self) -> float:
        """in bits per second"""
        return np.mean(list(map(lambda r: r.download_rate, self.reports)))
