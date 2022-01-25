#!/usr/bin/env python
import time

import matplotlib
from matplotlib import pyplot as plt

from qvis.connection import Connection, read_qlog
from qvis.plot import QvisByteAxisFormatter, QvisTimeAxisFormatter, plot_connection_flow_limit, plot_stream_data_sent, \
    plot_stream_flow_limit, plot_congestion_window, plot_bytes_in_flight


# %% load qlog files
max_ms = 20000
conn: Connection = read_qlog('./data/server_1000ms.qlog.gz', max_ms)
conn_1p: Connection = read_qlog('./data/server_1000ms_client_side_proxy.qlog.gz', max_ms)
conn_2p: Connection = read_qlog('./data/server_1000ms_two_proxies.qlog.gz', max_ms)


# %% plot
plt.rcParams.update({
    "font.family": "serif",
    "text.usetex": True,
    "pgf.rcfonts": False,
})
fig, ax = plt.subplots()
plot_congestion_window(ax, conn, label='No proxy', color='#253c4b', linestyle='dashed')
plot_congestion_window(ax, conn_1p, label='Client-side proxy', color='#00885c', linestyle='dashed')
plot_congestion_window(ax, conn_2p, label='Proxies on both sides', color='#ffa600', linestyle='dashed')
plot_bytes_in_flight(ax, conn, label='No proxy', color='#253c4b')
plot_bytes_in_flight(ax, conn_1p, label='Client-side proxy', color='#00885c')
plot_bytes_in_flight(ax, conn_2p, label='Proxies on both sides', color='#ffa600')
ax.margins(0)
fig.set_size_inches(8, 6)
ax.set_axisbelow(True)
ax.grid(True)
ax.set_ylim(ymin=0)
ax.set_xlim(xmin=0)
lgnd=ax.legend(fancybox=False, shadow=False)
for handle in lgnd.legendHandles:
    handle._sizes = [30]
ax.xaxis.set_major_formatter(QvisTimeAxisFormatter)
ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(2))
ax.yaxis.set_major_formatter(QvisByteAxisFormatter)
ax.xaxis.set_label_text('Time (s)')
ax.yaxis.set_label_text('Data (bytes)')
fig.savefig(f'./plots/compare_congestion_1000ms.pdf', bbox_inches='tight', dpi=300)
plt.plot()
