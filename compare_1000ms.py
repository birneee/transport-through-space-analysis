#!/usr/bin/env python
import time

import matplotlib
from matplotlib import pyplot as plt

from qvis.connection import Connection, read_qlog
from qvis.plot import QvisByteAxisFormatter, QvisTimeAxisFormatter, plot_connection_flow_limit, plot_stream_data_sent, \
    plot_stream_flow_limit, plot_congestion_window, plot_bytes_in_flight, plot_raw_data_sent

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
plot_stream_data_sent(ax, conn, 0, label='No proxy', color='#253c4b')
plot_stream_data_sent(ax, conn_1p, 0, label='Client-side proxy', color='#00885c')
plot_stream_data_sent(ax, conn_2p, 0, label='Proxies on both sides', color='#ffa600')
# plot_raw_data_sent(ax, conn_2p, label='Proxies on both sides', color='red')
plot_stream_flow_limit(ax, conn, 0, label='Stream flow control limit', color='gray')
plot_stream_flow_limit(ax, conn_1p, 0, label=None, color='gray')
plot_stream_flow_limit(ax, conn_2p, 0, label=None, color='gray')
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
fig.savefig(f'./plots/compare_1000ms.pdf', bbox_inches='tight', dpi=300)
plt.plot()
