#!/usr/bin/env python
import math
from typing import List

from matplotlib import pyplot as plt
from qvis.plot import QvisByteAxisFormatter

from qvis_qperf.aggregated_connection import AggregatedConnection
from qvis_qperf.connection import Connection, load_all_connections, reduce_steps
from qvis_qperf.plot import plot_time_to_first_byte, plot_rate


def plot(connections: List[Connection], output_name: str, zero_at_ttfb: bool = False, timespan: float = 40):
    agg_connection = AggregatedConnection(connections)
    start_time = 0
    if zero_at_ttfb:
        start_time = math.floor(agg_connection.time_to_first_byte)
    end_time = start_time + timespan
    plt.rcParams.update({
        "font.family": "serif",
        "text.usetex": True,
        "pgf.rcfonts": False,
    })
    fig, ax = plt.subplots()
    ax.axline((0, 100_000_000), (1, 100_000_000), color='gray', linestyle=(0, (1, 10)))
    plot_rate(ax, connections, label='Individual rates', color='gray', alpha=0.2)
    plot_rate(ax, agg_connection, label="Average rate", marker='x', color="blue")
    plot_time_to_first_byte(ax, agg_connection, color='blue')
    ax.xaxis.set_label_text('Time (s)')
    ax.yaxis.set_label_text('Rate (bit/s)')
    ax.xaxis.set_ticks_position('both')
    ax.yaxis.set_ticks_position('both')
    ax.set_axisbelow(True)
    ax.set_ylim(ymin=0, ymax=120000000)
    ax.set_xlim(xmin=start_time, xmax=end_time)
    lgnd = ax.legend(fancybox=False, shadow=False, loc='lower center', bbox_to_anchor=(0.47, -0.45), ncol=3,
                     frameon=False)
    for handle in lgnd.legendHandles:
        handle._alpha = 1
    ax.yaxis.set_major_formatter(QvisByteAxisFormatter)  # works for bits to
    fig.set_size_inches(5.5, 2.2)
    output_path = f'./plots/{output_name}.pdf'
    fig.savefig(output_path, bbox_inches='tight', dpi=300)
    print(f'saved plot as {output_path}')
    plt.plot()


plot(reduce_steps(load_all_connections('./data/72ms/qperf'), 2), 'rate_start_72ms', zero_at_ttfb=True, timespan=5)
plot(reduce_steps(load_all_connections('./data/72ms_client_side_proxy/qperf'), 2), 'rate_start_72ms_client_side_proxy', zero_at_ttfb=True, timespan=5)
plot(reduce_steps(load_all_connections('./data/72ms_two_proxies/qperf'), 2), 'rate_start_72ms_two_proxies', zero_at_ttfb=True, timespan=5)
plot(reduce_steps(load_all_connections('./data/72ms_two_proxies_simple/qperf'), 2), 'rate_start_72ms_two_proxies_simple', zero_at_ttfb=True, timespan=5)
plot(reduce_steps(load_all_connections('./data/72ms_two_proxies_simple_xse/qperf'), 2), 'rate_start_72ms_two_proxies_simple_xse', zero_at_ttfb=True, timespan=5)

plot(reduce_steps(load_all_connections('./data/220ms/qperf'), 2), 'rate_start_220ms', zero_at_ttfb=True, timespan=5)
plot(reduce_steps(load_all_connections('./data/220ms_client_side_proxy/qperf'), 2), 'rate_start_220ms_client_side_proxy', zero_at_ttfb=True, timespan=5)
plot(reduce_steps(load_all_connections('./data/220ms_two_proxies/qperf'), 2), 'rate_start_220ms_two_proxies', zero_at_ttfb=True, timespan=5)
plot(reduce_steps(load_all_connections('./data/220ms_two_proxies_simple/qperf'), 2), 'rate_start_220ms_two_proxies_simple', zero_at_ttfb=True, timespan=5)
plot(reduce_steps(load_all_connections('./data/220ms_two_proxies_simple_xse/qperf'), 2), 'rate_start_220ms_two_proxies_simple_xse', zero_at_ttfb=True, timespan=5)

plot(reduce_steps(load_all_connections('./data/500ms/qperf'), 2), 'rate_start_500ms', zero_at_ttfb=True, timespan=5)
plot(reduce_steps(load_all_connections('./data/500ms_client_side_proxy/qperf'), 2), 'rate_start_500ms_client_side_proxy', zero_at_ttfb=True, timespan=5)
plot(reduce_steps(load_all_connections('./data/500ms_two_proxies/qperf'), 2), 'rate_start_500ms_two_proxies', zero_at_ttfb=True, timespan=5)
plot(reduce_steps(load_all_connections('./data/500ms_two_proxies_simple/qperf'), 2), 'rate_start_500ms_two_proxies_simple', zero_at_ttfb=True, timespan=5)
plot(reduce_steps(load_all_connections('./data/500ms_two_proxies_simple_xse/qperf'), 2), 'rate_start_500ms_two_proxies_simple_xse', zero_at_ttfb=True, timespan=5)

plot(reduce_steps(load_all_connections('./data/1000ms/qperf'), 2), 'rate_start_1000ms', zero_at_ttfb=True, timespan=5)
plot(reduce_steps(load_all_connections('./data/1000ms_client_side_proxy/qperf'), 2), 'rate_start_1000ms_client_side_proxy', zero_at_ttfb=True, timespan=5)
plot(reduce_steps(load_all_connections('./data/1000ms_two_proxies/qperf'), 2), 'rate_start_1000ms_two_proxies', zero_at_ttfb=True, timespan=5)
plot(reduce_steps(load_all_connections('./data/1000ms_two_proxies_simple/qperf'), 2), 'rate_start_1000ms_two_proxies_simple', zero_at_ttfb=True, timespan=5)
plot(reduce_steps(load_all_connections('./data/1000ms_two_proxies_simple_xse/qperf'), 2), 'rate_start_1000ms_two_proxies_simple_xse', zero_at_ttfb=True, timespan=5)

plot(reduce_steps(load_all_connections('./data/2000ms/qperf'), 2), 'rate_start_2000ms', zero_at_ttfb=True, timespan=5)
plot(reduce_steps(load_all_connections('./data/2000ms_client_side_proxy/qperf'), 2), 'rate_start_2000ms_client_side_proxy', zero_at_ttfb=True, timespan=5)
plot(reduce_steps(load_all_connections('./data/2000ms_two_proxies/qperf'), 2), 'rate_start_2000ms_two_proxies', zero_at_ttfb=True, timespan=5)
plot(reduce_steps(load_all_connections('./data/2000ms_two_proxies_simple/qperf'), 2), 'rate_start_2000ms_two_proxies_simple', zero_at_ttfb=True, timespan=5)
