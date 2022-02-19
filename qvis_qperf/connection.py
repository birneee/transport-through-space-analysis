import re
from typing import List

from qvis_qperf.report import Report

CLIENT_REPORT_REGEX = r'[^\d\.]+(?P<time>\d+\.?\d*)[^\d\.]+(?P<rate>\d+\.?\d*)[^\d\.]+(?P<bytes>\d+)[^\d\.]+(?P<packets>\d+)$'


class Connection:
    reports: List[Report]

    def __init__(self, file: str):
        """parse qvis_qperf output file"""
        self.reports = []
        with open(file) as file:
            for line in file:
                match = re.match(CLIENT_REPORT_REGEX, line)
                if match:
                    self.reports.append(Report(
                        float(match.group('time')),
                        float(match.group('rate')),
                        int(match.group('bytes')),
                        int(match.group('packets')),
                    ))
