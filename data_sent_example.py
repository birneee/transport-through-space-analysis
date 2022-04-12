#!/usr/bin/env python

import matplotlib
from matplotlib import pyplot as plt

from qvis.connection import Connection, read_qlog
from qvis.plot import QvisByteAxisFormatter, QvisTimeAxisFormatter, plot_available_congestion_window_of_stream, \
    plot_remote_stream_flow_limit, plot_stream_data_sent


def plot(rtt_ms: int, server_side_proxy_handover_ms: int, output_path: str, max_ms: int = 40000, ymax=None,
         xaxis_steps: float = 2, plot_width: float = 8, plot_height: float = 6, legend_anchor_x: float = 0.5, legend_anchor_y: float = -0.1):
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
    plot_stream_data_sent(ax, conn_2p, 0, label='Dist. PEP (static CC)', color='tab:orange')

    plot_remote_stream_flow_limit(ax, conn, 0, label='Flow control limit', color='#253c4b', linestyle='dashed')
    plot_remote_stream_flow_limit(ax, conn_1p, 0, label=None, color='#00885c', linestyle='dashed')
    plot_remote_stream_flow_limit(ax, conn_2p_simple, 0, label=None, color='#ffa600', linestyle='dashed')
    plot_remote_stream_flow_limit(ax, conn_2p, 0, label=None, color='tab:orange', linestyle='dashed')

    plot_available_congestion_window_of_stream(ax, conn, 0, label='Congestion window', color='#253c4b',
                                               linestyle='dotted', chunk_size=10)
    plot_available_congestion_window_of_stream(ax, conn_1p, 0, label=None, color='#00885c', linestyle='dotted',
                                               chunk_size=10)
    plot_available_congestion_window_of_stream(ax, conn_2p_simple, 0, label=None, color='#ffa600', linestyle='dotted',
                                               chunk_size=10)
    plot_available_congestion_window_of_stream(ax, conn_2p, 0, label=None, color='tab:orange', linestyle='dotted',
                                               chunk_size=10)

    ax.margins(0)
    fig.set_size_inches(plot_width, plot_height)
    ax.set_axisbelow(True)
    ax.grid(True)
    ax.set_ylim(ymin=0, ymax=ymax)
    ax.set_xlim(xmin=0, xmax=max_ms/1000)
    lgnd = ax.legend(loc='upper center', bbox_to_anchor=(legend_anchor_x, legend_anchor_y), ncol=3, frameon=False)
    for handle in lgnd.legendHandles:
        handle._sizes = [30]
    ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(xaxis_steps))
    ax.yaxis.set_major_formatter(QvisByteAxisFormatter)
    ax.xaxis.set_label_text('Time (s)')
    ax.yaxis.set_label_text('Data (bytes)')
    fig.savefig(output_path, bbox_inches='tight', dpi=600)
    print(f'saved plot as {output_path}')
    plt.plot()


plot(72, 144, './plots/data_sent_example_72ms.pdf')
plot(220, 440, './plots/data_sent_example_220ms.pdf')
plot(500, 1000, './plots/data_sent_example_500ms.pdf')
plot(1000, 2000, './plots/data_sent_example_1000ms.pdf')
plot(2000, 4000, './plots/data_sent_example_2000ms.pdf')

plot(72, 144, './plots/data_sent_example_72ms_zoom.pdf', max_ms=500, ymax=1000000, xaxis_steps=0.1, plot_width=6, plot_height=4, legend_anchor_x=0.45, legend_anchor_y=-0.13)
plot(220, 440, './plots/data_sent_example_220ms_zoom.pdf', max_ms=1500, ymax=1000000, xaxis_steps=0.2, plot_width=6, plot_height=4, legend_anchor_x=0.45, legend_anchor_y=-0.13)
plot(500, 1000, './plots/data_sent_example_500ms_zoom.pdf', max_ms=3500, ymax=1000000, xaxis_steps=0.5, plot_width=6, plot_height=4, legend_anchor_x=0.45, legend_anchor_y=-0.13)
plot(1000, 2000, './plots/data_sent_example_1000ms_zoom.pdf', max_ms=7000, ymax=1000000, xaxis_steps=1, plot_width=6, plot_height=4, legend_anchor_x=0.45, legend_anchor_y=-0.13)
plot(2000, 4000, './plots/data_sent_example_2000ms_zoom.pdf', max_ms=14000, ymax=1000000, xaxis_steps=1, plot_width=6, plot_height=4, legend_anchor_x=0.45, legend_anchor_y=-0.13)
