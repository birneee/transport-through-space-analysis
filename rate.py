#!/usr/bin/env python
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
        start_time = agg_connection.time_to_first_byte
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

    with open(f'./results/{output_name}.txt', 'w') as f:
        f.write(f'runs: {len(connections)}\n')
        f.write(f'runs with internal errors: {len(list(filter(lambda c: c.internal_error is not None, connections)))}\n')
        f.write(f'mean time to first byte: {agg_connection.time_to_first_byte} s\n')
        f.write(f'mean rate: {agg_connection.mean_rate} bit/s\n')
        f.write(f'total at 10s: {agg_connection.total_bytes_at(10)} byte\n')
        f.write(f'total at 20s: {agg_connection.total_bytes_at(20)} byte\n')
        f.write(f'total at 30s: {agg_connection.total_bytes_at(30)} byte\n')


plot(reduce_steps(load_all_connections('./data/72ms/qperf'), 10), 'rate_72ms')
plot(reduce_steps(load_all_connections('./data/72ms_client_side_proxy/qperf'), 10), 'rate_72ms_client_side_proxy')
plot(reduce_steps(load_all_connections('./data/72ms_two_proxies/qperf'), 10), 'rate_72ms_two_proxies')
plot(reduce_steps(load_all_connections('./data/72ms_two_proxies_simple/qperf'), 10), 'rate_72ms_two_proxies_simple')
plot(reduce_steps(load_all_connections('./data/72ms_two_proxies_simple_xse/qperf'), 10), 'rate_72ms_two_proxies_simple_xse')

plot(reduce_steps(load_all_connections('./data/220ms/qperf'), 10), 'rate_220ms')
plot(reduce_steps(load_all_connections('./data/220ms_client_side_proxy/qperf'), 10), 'rate_220ms_client_side_proxy')
plot(reduce_steps(load_all_connections('./data/220ms_two_proxies/qperf'), 10), 'rate_220ms_two_proxies')
plot(reduce_steps(load_all_connections('./data/220ms_two_proxies_simple/qperf'), 10), 'rate_220ms_two_proxies_simple')
plot(reduce_steps(load_all_connections('./data/220ms_two_proxies_simple_xse/qperf'), 10), 'rate_220ms_two_proxies_simple_xse')

plot(reduce_steps(load_all_connections('./data/500ms/qperf'), 10), 'rate_500ms')
plot(reduce_steps(load_all_connections('./data/500ms_client_side_proxy/qperf'), 10), 'rate_500ms_client_side_proxy')
plot(reduce_steps(load_all_connections('./data/500ms_two_proxies/qperf'), 10), 'rate_500ms_two_proxies')
plot(reduce_steps(load_all_connections('./data/500ms_two_proxies_simple/qperf'), 10), 'rate_500ms_two_proxies_simple')
plot(reduce_steps(load_all_connections('./data/500ms_two_proxies_simple_xse/qperf'), 10), 'rate_500ms_two_proxies_simple_xse')

plot(reduce_steps(load_all_connections('./data/1000ms/qperf'), 10), 'rate_1000ms')
plot(reduce_steps(load_all_connections('./data/1000ms_client_side_proxy/qperf'), 10), 'rate_1000ms_client_side_proxy')
plot(reduce_steps(load_all_connections('./data/1000ms_two_proxies/qperf'), 10), 'rate_1000ms_two_proxies')
plot(reduce_steps(load_all_connections('./data/1000ms_two_proxies_simple/qperf'), 10), 'rate_1000ms_two_proxies_simple')
plot(reduce_steps(load_all_connections('./data/1000ms_two_proxies_simple_xse/qperf'), 10), 'rate_1000ms_two_proxies_simple_xse')

plot(reduce_steps(load_all_connections('./data/2000ms/qperf'), 10), 'rate_2000ms')
plot(reduce_steps(load_all_connections('./data/2000ms_client_side_proxy/qperf'), 10), 'rate_2000ms_client_side_proxy')
plot(reduce_steps(load_all_connections('./data/2000ms_two_proxies/qperf'), 10), 'rate_2000ms_two_proxies')
plot(reduce_steps(load_all_connections('./data/2000ms_two_proxies_simple/qperf'), 10), 'rate_2000ms_two_proxies_simple')
