#!/usr/bin/env python
import os

import matplotlib
from matplotlib import pyplot as plt

from qvis.connection import Connection, read_qlog
from qvis.plot import QvisByteAxisFormatter, QvisTimeAxisFormatter, plot_stream_data_received, plot_time_to_first_byte

# %% load qlog files
max_ms = 40000
conn72: Connection = read_qlog('./data/72ms/qlog/client.qlog.gz', max_ms=max_ms)
conn220: Connection = read_qlog('./data/220ms/qlog/client.qlog.gz', max_ms=max_ms)
conn500: Connection = read_qlog('./data/500ms/qlog/client.qlog.gz', max_ms=max_ms)
conn1000: Connection = read_qlog('./data/1000ms/qlog/client.qlog.gz', max_ms=max_ms)
conn2000: Connection = read_qlog('./data/2000ms/qlog/client.qlog.gz', max_ms=max_ms)


# %% plot
plt.rcParams.update({
    "font.family": "serif",
    "text.usetex": True,
    "pgf.rcfonts": False,
})
fig, ax = plt.subplots()
ax.axline((0, 0), (1, 100_000_000 / 8), color='gray', linestyle=(0, (1, 10)))
plot_stream_data_received(ax, conn72, 0, label='$72\,$ms', color='tab:blue')
plot_stream_data_received(ax, conn220, 0, label='$220\,$ms', color='tab:orange')
plot_stream_data_received(ax, conn500, 0, label='$500\,$ms', color='tab:green')
plot_stream_data_received(ax, conn1000, 0, label='$1000\,$ms', color='tab:red')
plot_stream_data_received(ax, conn2000, 0, label='$2000\,$ms', color='tab:purple')
plot_time_to_first_byte(ax, conn72, 0, color='tab:blue')
plot_time_to_first_byte(ax, conn220, 0, label=None, color='tab:orange')
plot_time_to_first_byte(ax, conn500, 0, label=None, color='tab:green')
plot_time_to_first_byte(ax, conn1000, 0, label=None, color='tab:red')
plot_time_to_first_byte(ax, conn2000, 0, label=None, color='tab:purple')
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
