#!/usr/bin/env python
import os
from typing import List

from matplotlib import pyplot as plt

from qvis_qperf.aggregated_connection import AggregatedConnection
from qvis_qperf.connection import Connection, load_all_connections
from qvis_qperf.plot import plot_rate, plot_time_to_first_byte
from qvis.plot import QvisByteAxisFormatter


connections = load_all_connections('./data/72ms/qperf')
agg_connection = AggregatedConnection(connections)

# %% plot
plt.rcParams.update({
    "font.family": "serif",
    "text.usetex": True,
    "pgf.rcfonts": False,
})
fig, ax = plt.subplots()
plot_rate(ax, connections, label='Individual rates', color='gray', alpha=0.2)
plot_rate(ax, agg_connection, label="Average rate", marker='x', color="blue")
plot_time_to_first_byte(ax, agg_connection, color='blue')
ax.xaxis.set_label_text('Time (s)')
ax.yaxis.set_label_text('Rate (bit/s)')
ax.set_axisbelow(True)
ax.grid(True)
ax.set_ylim(ymin=0)
ax.set_xlim(xmin=0, xmax=40)
lgnd = ax.legend(fancybox=False, shadow=False, loc='lower right')
for handle in lgnd.legendHandles:
    handle._alpha = 1
ax.yaxis.set_major_formatter(QvisByteAxisFormatter)  # works for bits to
output_path = f'./plots/{os.path.splitext(os.path.basename(__file__))[0]}.pdf'
fig.savefig(output_path, bbox_inches='tight', dpi=300)
print(f'saved plot as {output_path}')
plt.plot()
with open(f'./results/{os.path.splitext(os.path.basename(__file__))[0]}.txt', 'w') as f:
    f.write(f'mean time to first byte: {agg_connection.time_to_first_byte} s\n')
    f.write(f'mean rate: {agg_connection.mean_rate} bit/s\n')
