#!/usr/bin/env python
import os

import matplotlib
from matplotlib import pyplot as plt
from qvis.plot import QvisByteAxisFormatter, QvisTimeAxisFormatter

from qvis_qperf.aggregated_connection import AggregatedConnection
from qvis_qperf.connection import load_all_connections
from qvis_qperf.plot import plot_rate, plot_time_to_first_byte

# %% load connections

conns_72 = load_all_connections('./data/72ms/qperf')
conns_220 = load_all_connections('./data/220ms/qperf')
conns_500 = load_all_connections('./data/500ms/qperf')
conns_1000 = load_all_connections('./data/1000ms/qperf')

# %% load qlog files

agg_conn_72 = AggregatedConnection(conns_72)
agg_conn_220 = AggregatedConnection(conns_220)
agg_conn_500 = AggregatedConnection(conns_500)
agg_conn_1000 = AggregatedConnection(conns_1000)


# %% plot
plt.rcParams.update({
    "font.family": "serif",
    "text.usetex": True,
    "pgf.rcfonts": False,
})
fig, ax = plt.subplots()

plot_rate(ax, agg_conn_72, label=r'$72\,$ms', color='tab:blue', marker='x')
plot_rate(ax, agg_conn_220, label=r'$220\,$ms', color='tab:orange', marker='x')
plot_rate(ax, agg_conn_500, label=r'$500\,$ms', color='tab:green', marker='x')
plot_rate(ax, agg_conn_1000, label=r'$1000\,$ms', color='tab:red', marker='x')

plot_rate(ax, conns_72, label='Individual Rates', color='tab:blue', alpha=0.1, linestyle='dotted')
plot_rate(ax, conns_220, label=None, color='tab:orange', alpha=0.1, linestyle='dotted')
plot_rate(ax, conns_500, label=None, color='tab:green', alpha=0.1, linestyle='dotted')
plot_rate(ax, conns_1000, label=None, color='tab:red', alpha=0.05, linestyle='dotted')

plot_time_to_first_byte(ax, agg_conn_72, color='tab:blue')
plot_time_to_first_byte(ax, agg_conn_220, label=None, color='tab:orange')
plot_time_to_first_byte(ax, agg_conn_500, label=None, color='tab:green')
plot_time_to_first_byte(ax, agg_conn_1000, label=None, color='tab:red')

fig.set_size_inches(8, 6)
ax.set_axisbelow(True)
ax.grid(True)
ax.set_ylim(ymin=0)
ax.set_xlim(xmin=0, xmax=40)
lgnd = ax.legend(fancybox=False, shadow=False, loc='lower right')
for handle in lgnd.legendHandles:
    handle._sizes = [30]
    handle._alpha = 1
ax.xaxis.set_major_formatter(QvisTimeAxisFormatter)
ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(2))
ax.yaxis.set_major_formatter(QvisByteAxisFormatter)
ax.xaxis.set_label_text('Time (s)')
ax.yaxis.set_label_text('Rate (bit/s)')
output_path = f'./plots/{os.path.splitext(os.path.basename(__file__))[0]}.pdf'
fig.savefig(output_path, bbox_inches='tight', dpi=600)
print(f'saved plot as {output_path}')
plt.plot()
