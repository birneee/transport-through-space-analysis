#!/usr/bin/env python
import os
from typing import List

from qvis.qperf.connection import QperfConnection

connection: List[QperfConnection] = []
dir = './data/1000ms_two_proxies_simple/qperf'
for file in os.listdir(dir):
    file_extension = os.path.splitext(file)[1]
    if file_extension == '.qperf':
        connection.append(QperfConnection(os.path.join(dir, file)))


