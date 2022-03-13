#!/usr/bin/env python
from typing import Optional

import matplotlib
from matplotlib import pyplot as plt
from qvis.plot import QvisTimeAxisFormatter, QvisByteAxisFormatter

from qvis_qperf.aggregated_connection import AggregatedConnection
from qvis_qperf.connection import load_all_connections, all_intersections
from qvis_qperf.plot import plot_time_to_first_byte, plot_data_received, plot_data_received_intersection


def plot(rtt_ms: int, output_path: str, start_time: float = 0, timespan: float = 40,
         xaxis_steps: Optional[float] = None):
    end_time = start_time + timespan

    conn_no_pep = AggregatedConnection(load_all_connections(f'./data/{rtt_ms}ms/qperf', max_s=end_time + 0.1))
    conn_client_side_pep = AggregatedConnection(
        load_all_connections(f'./data/{rtt_ms}ms_client_side_proxy/qperf', max_s=end_time + 0.1))
    conn_distributed_pep = AggregatedConnection(
        load_all_connections(f'./data/{rtt_ms}ms_two_proxies_simple/qperf', max_s=end_time + 0.1))
    conn_distributed_pep_static_cc = AggregatedConnection(
        load_all_connections(f'./data/{rtt_ms}ms_two_proxies/qperf', max_s=end_time + 0.1))

    plt.rcParams.update({
        "font.family": "serif",
        "text.usetex": True,
        "pgf.rcfonts": False,
    })
    fig, ax = plt.subplots()
    ax.axline((0, 0), (1, 100_000_000 / 8), color='gray', linestyle=(0, (1, 10)))
    plot_data_received(ax, conn_no_pep, label=r'No PEP', color='#253c4b', linewidth=1.5)
    plot_data_received(ax, conn_client_side_pep, label='Client-side PEP', color='#00885c', linewidth=1.5)
    plot_data_received(ax, conn_distributed_pep, label='Distributed PEP', color='#ffa600', linewidth=1.5)
    plot_data_received(ax, conn_distributed_pep_static_cc, label='Distributed PEP (static CC)', color='tab:orange',
                       linewidth=1.5)

    plot_time_to_first_byte(ax, conn_no_pep, color='#253c4b')
    plot_time_to_first_byte(ax, conn_client_side_pep, color='#00885c', label=None)
    plot_time_to_first_byte(ax, conn_distributed_pep, color='#ffa600', label=None)
    plot_time_to_first_byte(ax, conn_distributed_pep_static_cc, color='tab:orange', label=None)

    plot_data_received_intersection(
        ax,
        list(map(lambda c: c.to_avg_connection(),
                 [conn_no_pep, conn_client_side_pep, conn_distributed_pep, conn_distributed_pep_static_cc])),
        ['#253c4b', '#00885c', '#ffa600', 'tab:orange'],
        label='Intersections',
        markersize=15,
    )

    ax.xaxis.set_label_text('Time (s)')
    ax.yaxis.set_label_text('Data (bytes)')
    ax.set_axisbelow(True)
    ax.grid(True)
    ax.set_ylim(ymin=0, ymax=None)
    ax.set_xlim(xmin=start_time, xmax=end_time)
    lgnd = ax.legend(fancybox=False, shadow=False, loc='lower center', bbox_to_anchor=(0.47, -0.22), ncol=3,
                     frameon=False)
    for handle in lgnd.legendHandles:
        handle._alpha = 1
    if xaxis_steps is not None:
        ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(xaxis_steps))
    ax.yaxis.set_major_formatter(QvisByteAxisFormatter)
    fig.set_size_inches(8, 6)
    fig.savefig(output_path, bbox_inches='tight', dpi=300)
    print(f'saved plot as {output_path}')
    plt.plot()


def report_intercept(rtt_ms: int, output_path: str):
    conn_no_pep = AggregatedConnection(load_all_connections(f'./data/{rtt_ms}ms/qperf'))
    conn_client_side_pep = AggregatedConnection(load_all_connections(f'./data/{rtt_ms}ms_client_side_proxy/qperf'))
    conn_distributed_pep = AggregatedConnection(load_all_connections(f'./data/{rtt_ms}ms_two_proxies_simple/qperf'))
    conn_distributed_pep_static_cc = AggregatedConnection(load_all_connections(f'./data/{rtt_ms}ms_two_proxies/qperf'))

    with open(output_path, 'w') as f:
        connections = list(map(lambda c: c.to_avg_connection(), [conn_no_pep, conn_client_side_pep, conn_distributed_pep, conn_distributed_pep_static_cc]))
        connection_names = ['No PEP', 'Client-side PEP', 'Distributed PEP', 'Distributed PEP (static CC)']
        for interception in all_intersections(connections):
            upper_name = connection_names[connections.index(interception.upper)]
            lower_name = connection_names[connections.index(interception.lower)]
            f.write(f'{upper_name} overtakes {lower_name} at {interception.time}s {interception.bytes_received}B\n')


plot(72, './plots/data_received_72ms.pdf', xaxis_steps=2)
plot(220, './plots/data_received_220ms.pdf', xaxis_steps=2)
plot(500, './plots/data_received_500ms.pdf', xaxis_steps=2)
plot(1000, './plots/data_received_1000ms.pdf', xaxis_steps=2)
plot(2000, './plots/data_received_2000ms.pdf', xaxis_steps=2)

plot(72, './plots/data_received_72ms_zoom.pdf', timespan=1.5, xaxis_steps=0.1)
plot(220, './plots/data_received_220ms_zoom.pdf', start_time=0.6, timespan=2, xaxis_steps=0.2)
plot(500, './plots/data_received_500ms_zoom.pdf', start_time=1.4, timespan=2, xaxis_steps=0.2)
plot(1000, './plots/data_received_1000ms_zoom.pdf', start_time=3, timespan=3.4, xaxis_steps=0.2)
plot(2000, './plots/data_received_2000ms_zoom.pdf', start_time=6, timespan=5, xaxis_steps=0.5)

report_intercept(72, './results/data_received_intercept_72ms.txt')
report_intercept(220, './results/data_received_intercept_220ms.txt')
report_intercept(500, './results/data_received_intercept_500ms.txt')
report_intercept(1000, './results/data_received_intercept_1000ms.txt')
report_intercept(2000, './results/data_received_intercept_2000ms.txt')
