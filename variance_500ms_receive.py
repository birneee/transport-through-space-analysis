#!/usr/bin/env python
import os

import matplotlib
from matplotlib import pyplot as plt

from qvis.connection import Connection, read_qlog
from qvis.plot import QvisByteAxisFormatter, QvisTimeAxisFormatter, plot_stream_data_received, plot_time_to_first_byte

# %% load qlog files
max_ms = 40000
conn1: Connection = read_qlog('./data/500ms/client.qlog.gz', max_ms=max_ms)
conn2: Connection = read_qlog('./data/500ms/2/client.qlog.gz', max_ms=max_ms)
conn3: Connection = read_qlog('./data/500ms/3/client.qlog.gz', max_ms=max_ms)
conn4: Connection = read_qlog('./data/500ms/4/client.qlog.gz', max_ms=max_ms)
conn5: Connection = read_qlog('./data/500ms/5/client.qlog.gz', max_ms=max_ms)


# %% plot
plt.rcParams.update({
    "font.family": "serif",
    "text.usetex": True,
    "pgf.rcfonts": False,
})
fig, ax = plt.subplots()
ax.axline((0, 0), (1, 100_000_000 / 8), color='gray', linestyle=(0, (1, 10)))
plot_stream_data_received(ax, conn1, 0, label='Run 1', color='#253C4B')
plot_stream_data_received(ax, conn2, 0, label='Run 2', color='#1E5F6F')
plot_stream_data_received(ax, conn3, 0, label='Run 3', color='#168293')
plot_stream_data_received(ax, conn4, 0, label='Run 4', color='#0FA4B7')
plot_stream_data_received(ax, conn5, 0, label='Run 5', color='#07C7DB')
plot_time_to_first_byte(ax, conn1, 0)
plot_time_to_first_byte(ax, conn2, 0, label=None)
plot_time_to_first_byte(ax, conn3, 0, label=None)
plot_time_to_first_byte(ax, conn4, 0, label=None)
plot_time_to_first_byte(ax, conn5, 0, label=None)
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
fig.savefig(output_path, bbox_inches='tight', dpi=300)
print(f'saved plot as {output_path}')
plt.plot()
