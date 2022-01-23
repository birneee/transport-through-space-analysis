#!/usr/bin/env python

# %% imports
from functools import reduce
import time
import matplotlib
from matplotlib import pyplot as plt
from connection import Connection, read_qlog
from plot import QvisByteAxisFormatter, QvisTimeAxisFormatter, plot_connection_flow_limit, plot_data_sent

# %% load
start = time.time()
filepath = './data/test.qlog.gz'
conn: Connection = read_qlog(filepath)
print(f'loading took {time.time() - start}')

# %% plot
start = time.time()
plt.rcParams.update({
    "font.family": "serif",
    "text.usetex": True,
    "pgf.rcfonts": False, 
})
fig, ax = plt.subplots()
plot_data_sent(ax, conn)
plot_connection_flow_limit(ax, conn)
ax.margins(0)
fig = ax.get_figure()
fig.set_size_inches(8, 6)
ax.set_axisbelow(True)
ax.grid(True)
ax.set_ylim(ymin=0)
ax.set_xlim(xmin=0)
lgnd=ax.legend()
for handle in lgnd.legendHandles:
    handle._sizes = [30]
ax.xaxis.set_major_formatter(QvisTimeAxisFormatter)
ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(2))
ax.yaxis.set_major_formatter(QvisByteAxisFormatter)
ax.xaxis.set_label_text('Time (s)')
ax.yaxis.set_label_text('Data (bytes)')
fig.savefig(f'./plots/test.pdf', bbox_inches='tight', dpi=300)
plt.plot()
print(f'plotting took {time.time() - start}')

# %%
