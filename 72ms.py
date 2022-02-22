#!/usr/bin/env python
import os
from typing import List

from matplotlib import pyplot as plt

from qvis_qperf.aggregated_connection import AggregatedConnection
from qvis_qperf.connection import Connection, load_all_connections
from qvis_qperf.plot import plot_rate, plot_time_to_first_byte
from qvis.plot import QvisByteAxisFormatter

max_s = 40
connections = load_all_connections('./data/72ms/qperf', max_s=40)
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
ax.xaxis.set_ticks_position('both')
ax.yaxis.set_ticks_position('both')
ax.set_axisbelow(True)
ax.set_ylim(ymin=0, ymax=120000000)
ax.set_xlim(xmin=0, xmax=40)
lgnd = ax.legend(fancybox=False, shadow=False, loc='lower center',  bbox_to_anchor=(0.47, -0.45), ncol=3, frameon=False)
for handle in lgnd.legendHandles:
    handle._alpha = 1
ax.yaxis.set_major_formatter(QvisByteAxisFormatter)  # works for bits to
fig.set_size_inches(5.5, 2.2)
output_path = f'./plots/{os.path.splitext(os.path.basename(__file__))[0]}.pdf'
fig.savefig(output_path, bbox_inches='tight', dpi=300)
print(f'saved plot as {output_path}')
plt.plot()

with open(f'./results/{os.path.splitext(os.path.basename(__file__))[0]}.txt', 'w') as f:
    f.write(f'mean time to first byte: {agg_connection.time_to_first_byte} s\n')
    f.write(f'mean rate: {agg_connection.mean_rate} bit/s\n')
    f.write(f'total at 10s: {agg_connection.total_bytes_at(10)} byte\n')
    f.write(f'total at 20s: {agg_connection.total_bytes_at(20)} byte\n')
    f.write(f'total at 30s: {agg_connection.total_bytes_at(30)} byte\n')
