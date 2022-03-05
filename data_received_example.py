#!/usr/bin/env python
import os

import matplotlib
from matplotlib import pyplot as plt

from qvis.connection import Connection, read_qlog
from qvis.plot import QvisByteAxisFormatter, QvisTimeAxisFormatter, plot_stream_data_received, \
    plot_local_stream_flow_limit, plot_time_to_first_byte


def plot(rtt_ms: int, client_side_proxy_handover_ms: int, output_path: str, max_ms: int = 40000, xmin: float = 0, ymax = None, xaxis_steps: int = 2):
    conn: Connection = read_qlog(f'./data/{rtt_ms}ms/qlog/client.qlog.gz', max_ms=max_ms)
    conn_1p: Connection = read_qlog(f'./data/{rtt_ms}ms_client_side_proxy/qlog/client_side_proxy_server_facing.qlog.gz',
                                    max_ms=max_ms, shift_ms=client_side_proxy_handover_ms)
    conn_2p: Connection = read_qlog(f'./data/{rtt_ms}ms_two_proxies/qlog/client_side_proxy_server_facing.qlog.gz',
                                    max_ms=max_ms, shift_ms=client_side_proxy_handover_ms)
    conn_2p_simple: Connection = read_qlog(
        f'./data/{rtt_ms}ms_two_proxies_simple/qlog/client_side_proxy_server_facing.qlog.gz',
        max_ms=max_ms, shift_ms=client_side_proxy_handover_ms)

    # %% plot
    plt.rcParams.update({
        "font.family": "serif",
        "text.usetex": True,
        "pgf.rcfonts": False,
    })
    fig, ax = plt.subplots()
    ax.axline((0, 0), (1, 100_000_000 / 8), color='gray', linestyle=(0, (1, 10)))

    plot_stream_data_received(ax, conn, 0, label='No PEP', color='#253c4b')
    plot_stream_data_received(ax, conn_1p, 0, label='Client-side PEP', color='#00885c')
    plot_stream_data_received(ax, conn_2p_simple, 0, label='Distributed PEP', color='#ffa600')
    plot_stream_data_received(ax, conn_2p, 0, label='Distributed PEP (static CC)', color='tab:orange')

    plot_local_stream_flow_limit(ax, conn, 0, label='Stream flow control limit', color='#253c4b', linestyle='dashed')
    plot_local_stream_flow_limit(ax, conn_1p, 0, label=None, color='#00885c', linestyle='dashed')
    plot_local_stream_flow_limit(ax, conn_2p_simple, 0, label=None, color='#ffa600', linestyle='dashed')
    plot_local_stream_flow_limit(ax, conn_2p, 0, label=None, color='tab:orange', linestyle='dashed')

    plot_time_to_first_byte(ax, conn, 0, color='#253c4b')
    plot_time_to_first_byte(ax, conn_1p, 0, label=None, color='#00885c')
    plot_time_to_first_byte(ax, conn_2p_simple, 0, label=None, color='#ffa600')
    plot_time_to_first_byte(ax, conn_2p, 0, label=None, color='tab:orange')

    ax.margins(0)
    fig.set_size_inches(8, 6)
    ax.set_axisbelow(True)
    ax.grid(True)
    ax.set_ylim(ymin=0, ymax=ymax)
    ax.set_xlim(xmin=xmin, xmax=max_ms/1000)
    lgnd = ax.legend(fancybox=False, shadow=False)
    for handle in lgnd.legendHandles:
        handle._sizes = [30]
    ax.xaxis.set_major_formatter(QvisTimeAxisFormatter)
    ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(xaxis_steps))
    ax.yaxis.set_major_formatter(QvisByteAxisFormatter)
    ax.xaxis.set_label_text('Time (s)')
    ax.yaxis.set_label_text('Data (bytes)')
    fig.savefig(output_path, bbox_inches='tight', dpi=600)
    print(f'saved plot as {output_path}')
    plt.plot()


plot(72, 216, './plots/data_received_example_72ms.pdf')
plot(220, 660, './plots/data_received_example_220ms.pdf')
plot(500, 1500, './plots/data_received_example_500ms.pdf')
plot(500, 1500, './plots/data_received_example_500ms_zoom.pdf', max_ms=4000, xmin=1, ymax=600000, xaxis_steps=1)
plot(1000, 3000, './plots/data_received_example_1000ms.pdf')
plot(1000, 3000, './plots/data_received_example_1000ms_zoom.pdf', max_ms=8000, xmin=2, ymax=600000, xaxis_steps=1)
plot(2000, 6000, './plots/data_received_example_2000ms.pdf')
