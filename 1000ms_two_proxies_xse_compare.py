#!/usr/bin/env python
import os

import matplotlib
from matplotlib import pyplot as plt

from qvis.connection import Connection, read_qlog
from qvis.plot import QvisByteAxisFormatter, QvisTimeAxisFormatter, plot_stream_data_received, \
    plot_local_stream_flow_limit, plot_time_to_first_byte, plot_xse_data_received

file_name = os.path.splitext(os.path.basename(__file__))[0]
"""file name of this script without extension"""

# %% load qlog files
max_ms = 40000
conn: Connection = read_qlog('./data/1000ms_two_proxies/1/client.qlog.gz',
                             max_ms=max_ms, shift_ms=3000)
conn_xse: Connection = read_qlog('./data/1000ms_two_proxies_xse/2/client.qlog.gz',
                                 max_ms=max_ms, shift_ms=3000)

# %% results
with open(f'./results/{file_name}.txt', 'w') as f:
    f.write(f'without xse: {conn.avg_stream_receive_rate(0)} bit/s\n')
    xse_raw = conn_xse.avg_stream_receive_rate(0)
    f.write(f'with xse: raw: {xse_raw} bit/s\n')
    xse_data = conn_xse.avg_xse_stream_receive_rate(0)
    f.write(f'with xse: payload: {xse_data} bit/s\n')
    overhead_ratio = (xse_raw - xse_data) / xse_data
    f.write(f'with xse: overhead: {overhead_ratio}\n')

# %% plot
plt.rcParams.update({
    "font.family": "serif",
    "text.usetex": True,
    "pgf.rcfonts": False,
})
fig, ax = plt.subplots()
ax.axline((0, 0), (1, 100_000_000 / 8), color='gray', linestyle=(0, (1, 10)))
plot_stream_data_received(ax, conn, 0, label='Without XSE-QUIC extension', color='#ffa600')
plot_xse_data_received(ax, conn_xse, 0, label='With XSE-QUIC extension', color='#ff00c7')
plot_time_to_first_byte(ax, conn, 0, label='Time to first byte', color='#ffa600')
plot_time_to_first_byte(ax, conn_xse, 0, label=None, color='#ff00c7')
ax.margins(0)
fig.set_size_inches(8, 6)
ax.set_axisbelow(True)
ax.grid(True)
ax.set_ylim(ymin=0)
ax.set_xlim(xmin=0)
lgnd = ax.legend(fancybox=False, shadow=False)
for handle in lgnd.legendHandles:
    handle._sizes = [30]
ax.xaxis.set_major_formatter(QvisTimeAxisFormatter)
ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(2))
ax.yaxis.set_major_formatter(QvisByteAxisFormatter)
ax.xaxis.set_label_text('Time (s)')
ax.yaxis.set_label_text('Data (bytes)')
output_path = f'./plots/{file_name}.pdf'
fig.savefig(output_path, bbox_inches='tight', dpi=600)
print(f'saved plot as {output_path}')
plt.plot()
