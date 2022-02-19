#!/usr/bin/env python
import os
from typing import List

from matplotlib import pyplot as plt

from qvis_qperf.aggregated_connection import AggregatedConnection
from qvis_qperf.connection import Connection
from qvis_qperf.plot import plot_rate
from qvis.plot import QvisByteAxisFormatter


connections: List[Connection] = []
dir = './data/1000ms_two_proxies_simple/qperf'
for file in os.listdir(dir):
    file_extension = os.path.splitext(file)[1]
    if file_extension == '.qperf':
        connections.append(Connection(os.path.join(dir, file)))
agg_connection = AggregatedConnection(connections)

# %% plot
plt.rcParams.update({
    "font.family": "serif",
    "text.usetex": True,
    "pgf.rcfonts": False,
})
fig, ax = plt.subplots()
for index, connection in enumerate(connections):
    label = None
    if index == 0:
        label = 'Individual Rates'
    plot_rate(ax, connection, color='gray', label=label, marker="x", alpha=0.2, markersize=4)
plot_rate(ax, agg_connection, label="Average Rate", marker='x')
ax.xaxis.set_label_text('Time (s)')
ax.yaxis.set_label_text('Rate (bit/s)')
ax.set_axisbelow(True)
ax.grid(True)
lgnd = ax.legend(fancybox=False, shadow=False)
ax.yaxis.set_major_formatter(QvisByteAxisFormatter)  # works for bits to
output_path = f'./plots/{os.path.splitext(os.path.basename(__file__))[0]}.pdf'
fig.savefig(output_path, bbox_inches='tight', dpi=300)
print(f'saved plot as {output_path}')
plt.plot()
