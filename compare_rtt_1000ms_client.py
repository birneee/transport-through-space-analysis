#!/usr/bin/env python
import os

import matplotlib
from matplotlib import pyplot as plt

from qvis.connection import Connection, read_qlog
from qvis.plot import QvisTimeAxisFormatter, plot_rtt

# %% load qlog files
max_ms = 40000
conn: Connection = read_qlog('./data/1000ms/client.qlog.gz', max_ms=max_ms)
conn_1p: Connection = read_qlog('./data/1000ms_client_side_proxy/1/client_side_proxy_server_facing.qlog.gz',
                                shift_ms=3000, max_ms=max_ms)
conn_2p: Connection = read_qlog('./data/1000ms_two_proxies/1/client_side_proxy_server_facing.qlog.gz', shift_ms=3000,
                                max_ms=max_ms)

# %% plot
plt.rcParams.update({
    "font.family": "serif",
    "text.usetex": True,
    "pgf.rcfonts": False,
})
fig, ax = plt.subplots()
plot_rtt(ax, conn, label='No proxy', color='#253c4b')
plot_rtt(ax, conn_1p, label='Client-side proxy', color='#00885c')
plot_rtt(ax, conn_2p, label='Proxies on both sides', color='#ffa600')
ax.margins(x=0)
fig.set_size_inches(8, 3)
ax.set_axisbelow(True)
ax.grid(True)
ax.set_xlim(xmin=0)
ax.set_ylim(ymin=950)
lgnd = ax.legend(fancybox=False, shadow=False, loc='upper right')
for handle in lgnd.legendHandles:
    handle._sizes = [30]
ax.xaxis.set_major_formatter(QvisTimeAxisFormatter)
ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(2))
# ax.yaxis.set_major_formatter(QvisByteAxisFormatter)
ax.xaxis.set_label_text('Time (s)')
ax.yaxis.set_label_text('RTT (ms)')
output_path = f'./plots/{os.path.splitext(os.path.basename(__file__))[0]}.pdf'
fig.savefig(output_path, bbox_inches='tight', dpi=300)
print(f'saved plot as {output_path}')
plt.plot()
