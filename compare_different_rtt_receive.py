#!/usr/bin/env python
import os

import matplotlib
from matplotlib import pyplot as plt

from qvis.connection import Connection, read_qlog
from qvis.plot import QvisByteAxisFormatter, QvisTimeAxisFormatter, plot_stream_data_received, plot_time_to_first_byte

# %% load qlog files
max_ms = 40000
conn63: Connection = read_qlog('./data/63ms/2/client.qlog.gz', max_ms=max_ms)
conn125: Connection = read_qlog('./data/125ms/4/client.qlog.gz', max_ms=max_ms)
conn250: Connection = read_qlog('./data/250ms/2/client.qlog.gz', max_ms=max_ms)
conn500: Connection = read_qlog('./data/500ms/client.qlog.gz', max_ms=max_ms)
conn1000: Connection = read_qlog('./data/1000ms/client.qlog.gz', max_ms=max_ms)
conn2000: Connection = read_qlog('./data/2000ms/client.qlog.gz', max_ms=max_ms)


# %% plot
plt.rcParams.update({
    "font.family": "serif",
    "text.usetex": True,
    "pgf.rcfonts": False,
})
fig, ax = plt.subplots()
ax.axline((0, 0), (1, 100_000_000 / 8), color='gray', linestyle=(0, (1, 10)))
plot_stream_data_received(ax, conn63, 0, label='$63\,$ms', color='#253C4B')
plot_stream_data_received(ax, conn125, 0, label='$125\,$ms', color='#1E5F6F')
plot_stream_data_received(ax, conn250, 0, label='$250\,$ms', color='#168293')
plot_stream_data_received(ax, conn500, 0, label='$500\,$ms', color='#0FA4B7')
plot_stream_data_received(ax, conn1000, 0, label='$1000\,$ms', color='#07C7DB')
plot_stream_data_received(ax, conn2000, 0, label='$2000\,$ms', color='#00EAFF')
plot_time_to_first_byte(ax, conn63, 0, color='#253C4B')
plot_time_to_first_byte(ax, conn125, 0, label=None, color='#1E5F6F')
plot_time_to_first_byte(ax, conn250, 0, label=None, color='#168293')
plot_time_to_first_byte(ax, conn500, 0, label=None, color='#0FA4B7')
plot_time_to_first_byte(ax, conn1000, 0, label=None, color='#07C7DB')
plot_time_to_first_byte(ax, conn2000, 0, label=None, color='#00EAFF')
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
output_path = f'./plots/{os.path.splitext(os.path.basename(__file__))[0]}.pdf'
fig.savefig(output_path, bbox_inches='tight', dpi=600)
print(f'saved plot as {output_path}')
plt.plot()
