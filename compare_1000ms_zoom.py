#!/usr/bin/env python
import os

import matplotlib
from matplotlib import pyplot as plt

from qvis.connection import Connection, read_qlog
from qvis.plot import QvisByteAxisFormatter, QvisTimeAxisFormatter, plot_stream_data_sent

# %% load qlog files
max_ms = 5000
conn: Connection = read_qlog('./data/1000ms/server.qlog.gz', max_ms=max_ms)
conn_1p: Connection = read_qlog('./data/1000ms_client_side_proxy/server.qlog.gz', max_ms=max_ms)
conn_2p: Connection = read_qlog('./data/1000ms_two_proxies/server_side_proxy_client_facing.qlog.gz', shift_ms=2000,
                                max_ms=max_ms)

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
ax.margins(0)
fig.set_size_inches(8, 6)
ax.set_axisbelow(True)
ax.grid(True)
ax.set_ylim(ymin=0, ymax=300000)
ax.set_xlim(xmin=0)
lgnd = ax.legend(fancybox=False, shadow=False)
for handle in lgnd.legendHandles:
    handle._sizes = [30]
ax.xaxis.set_major_formatter(QvisTimeAxisFormatter)
ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(1))
ax.yaxis.set_major_formatter(QvisByteAxisFormatter)
ax.xaxis.set_label_text('Time (s)')
ax.yaxis.set_label_text('Data (bytes)')
output_path = f'./plots/{os.path.splitext(os.path.basename(__file__))[0]}.pdf'
fig.savefig(output_path, bbox_inches='tight', dpi=300)
print(f'saved plot as {output_path}')
plt.plot()
