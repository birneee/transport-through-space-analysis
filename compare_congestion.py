#!/usr/bin/env python
import os

import matplotlib
from matplotlib import pyplot as plt

from qvis.connection import Connection, read_qlog
from qvis.plot import QvisByteAxisFormatter, QvisTimeAxisFormatter, plot_congestion_window, plot_bytes_in_flight


def plot(rtt_ms: int, server_side_proxy_handover_ms: int, output_path: str, max_ms = 40000):
    conn: Connection = read_qlog(f'./data/{rtt_ms}ms/qlog/server.qlog.gz', max_ms=max_ms)
    conn_1p: Connection = read_qlog(f'./data/{rtt_ms}ms_client_side_proxy/qlog/server.qlog.gz', max_ms=max_ms)
    conn_2p: Connection = read_qlog(f'./data/{rtt_ms}ms_two_proxies/qlog/server_side_proxy_client_facing.qlog.gz', shift_ms=server_side_proxy_handover_ms,
                                    max_ms=max_ms)
    conn_2p_simple: Connection = read_qlog(f'./data/{rtt_ms}ms_two_proxies_simple/qlog/server_side_proxy_client_facing.qlog.gz',
                                    shift_ms=server_side_proxy_handover_ms,
                                    max_ms=max_ms)
    # %% plot
    plt.rcParams.update({
        "font.family": "serif",
        "text.usetex": True,
        "pgf.rcfonts": False,
    })
    fig, ax = plt.subplots()
    bdp = rtt_ms / 1000 * 100_000_000 / 8
    ax.axline((0, bdp), (1, bdp), color='gray', linestyle=(0, (1, 10)))
    # plot_bytes_in_flight(ax, conn, label='No proxy', color='#253c4b')
    # plot_bytes_in_flight(ax, conn_1p, label='Client-side proxy', color='#00885c')
    # plot_bytes_in_flight(ax, conn_2p, label='Proxies on both sides', color='#ffa600')
    plot_congestion_window(ax, conn, label='No PEP', color='#253c4b', linestyle='dashed', linewidth=1.5)
    plot_congestion_window(ax, conn_1p, label='Client-side PEP', color='#00885c', linestyle='dashed', linewidth=1.5)
    plot_congestion_window(ax, conn_2p_simple, label='Distributed PEP', color='#ffa600', linestyle='dashed', linewidth=1.5)
    plot_congestion_window(ax, conn_2p, label='Distributed PEP (static CC)', color='tab:orange', linestyle='dashed', linewidth=1.5)
    fig.set_size_inches(8, 6)
    ax.set_axisbelow(True)
    ax.grid(True)
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0, xmax=max_ms/1000)
    lgnd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False)
    for handle in lgnd.legendHandles:
        handle._sizes = [30]
    ax.xaxis.set_major_formatter(QvisTimeAxisFormatter)
    ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(2))
    ax.yaxis.set_major_formatter(QvisByteAxisFormatter)
    ax.xaxis.set_label_text('Time (s)')
    ax.yaxis.set_label_text('Data (bytes)')
    fig.savefig(output_path, bbox_inches='tight', dpi=300)
    print(f'saved plot as {output_path}')
    plt.plot()


plot(72, 144, './plots/compare_congestion_72ms.pdf')
plot(220, 440, './plots/compare_congestion_220ms.pdf')
plot(500, 1000, './plots/compare_congestion_500ms.pdf')
plot(1000, 2000, './plots/compare_congestion_1000ms.pdf')
plot(2000, 4000, './plots/compare_congestion_2000ms.pdf')
