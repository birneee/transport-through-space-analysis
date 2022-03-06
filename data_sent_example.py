#!/usr/bin/env python

import matplotlib
from matplotlib import pyplot as plt

from qvis.connection import Connection, read_qlog
from qvis.plot import QvisByteAxisFormatter, QvisTimeAxisFormatter, plot_available_congestion_window_of_stream, \
    plot_remote_stream_flow_limit, plot_stream_data_sent


def plot(rtt_ms: int, server_side_proxy_handover_ms: int, output_path: str, max_ms: int = 40000, ymax = None, xaxis_steps: int = 2):
    conn: Connection = read_qlog(f'./data/{rtt_ms}ms/qlog/server.qlog.gz', max_ms=max_ms)
    conn_1p: Connection = read_qlog(f'./data/{rtt_ms}ms_client_side_proxy/qlog/server.qlog.gz', max_ms=max_ms)
    conn_2p: Connection = read_qlog(f'./data/{rtt_ms}ms_two_proxies/qlog/server_side_proxy_client_facing.qlog.gz',
                                    shift_ms=server_side_proxy_handover_ms,
                                    max_ms=max_ms)
    conn_2p_simple: Connection = read_qlog(
        f'./data/{rtt_ms}ms_two_proxies_simple/qlog/server_side_proxy_client_facing.qlog.gz',
        shift_ms=server_side_proxy_handover_ms,
        max_ms=max_ms)

    plt.rcParams.update({
        "font.family": "serif",
        "text.usetex": True,
        "pgf.rcfonts": False,
    })
    fig, ax = plt.subplots()
    ax.axline((0, 0), (1, 100_000_000 / 8), color='gray', linestyle=(0, (1, 10)))

    plot_stream_data_sent(ax, conn, 0, label='No PEP', color='#253c4b')
    plot_stream_data_sent(ax, conn_1p, 0, label='Client-side PEP', color='#00885c')
    plot_stream_data_sent(ax, conn_2p_simple, 0, label='Distributed PEP', color='#ffa600')
    plot_stream_data_sent(ax, conn_2p, 0, label='Distributed PEP (static CC)', color='tab:orange')

    plot_remote_stream_flow_limit(ax, conn, 0, label='Stream flow control limit', color='#253c4b', linestyle='dashed')
    plot_remote_stream_flow_limit(ax, conn_1p, 0, label=None, color='#00885c', linestyle='dashed')
    plot_remote_stream_flow_limit(ax, conn_2p_simple, 0, label=None, color='#ffa600', linestyle='dashed')
    plot_remote_stream_flow_limit(ax, conn_2p, 0, label=None, color='tab:orange', linestyle='dashed')

    plot_available_congestion_window_of_stream(ax, conn, 0, label='Congestion window', color='#253c4b',
                                               linestyle='dotted')
    plot_available_congestion_window_of_stream(ax, conn_1p, 0, label=None, color='#00885c', linestyle='dotted')
    plot_available_congestion_window_of_stream(ax, conn_2p_simple, 0, label=None, color='#ffa600', linestyle='dotted')
    plot_available_congestion_window_of_stream(ax, conn_2p, 0, label=None, color='tab:orange', linestyle='dotted')

    ax.margins(0)
    fig.set_size_inches(8, 6)
    ax.set_axisbelow(True)
    ax.grid(True)
    ax.set_ylim(ymin=0, ymax=ymax)
    ax.set_xlim(xmin=0, xmax=max_ms/1000)
    lgnd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3, frameon=False)
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


plot(500, 1000, './plots/data_sent_example_500ms.pdf')
plot(500, 1000, './plots/data_sent_example_500ms_zoom.pdf', max_ms=3000, ymax=600000, xaxis_steps=1)
plot(1000, 2000, './plots/data_sent_example_1000ms.pdf')
plot(1000, 2000, './plots/data_sent_example_1000ms_zoom.pdf', max_ms=6000, ymax=600000, xaxis_steps=1)
