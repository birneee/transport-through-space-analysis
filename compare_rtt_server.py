#!/usr/bin/env python
import math
import os

import matplotlib
from matplotlib import pyplot as plt

from qvis.connection import Connection, read_qlog
from qvis.plot import QvisTimeAxisFormatter, plot_rtt


def plot(rtt_ms: int, server_side_proxy_handover_ms: int, output_path: str, max_ms: int = 40000, xmin: float = 0,
         ymax=None, xaxis_steps: int = 2):
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
    plot_rtt(ax, conn, label='No PEP', color='#253c4b', rtt_ms_step_size=min(5, rtt_ms/100))
    plot_rtt(ax, conn_1p, label='Client-side PEP', color='#00885c', rtt_ms_step_size=min(5, rtt_ms/100))
    plot_rtt(ax, conn_2p_simple, label='Distributed PEP', color='#ffa600', rtt_ms_step_size=min(5, rtt_ms/100))
    plot_rtt(ax, conn_2p, label='Distributed PEP (static CC)', color='tab:orange', rtt_ms_step_size=min(5, rtt_ms/100))
    ax.margins(x=0)
    fig.set_size_inches(8, 3)
    ax.set_axisbelow(True)
    ax.grid(True)
    ax.set_xlim(xmin=xmin, xmax=max_ms / 1000)
    ax.set_ylim(ymin=rtt_ms * 0.95, ymax=ymax)
    lgnd = ax.legend(fancybox=False, shadow=False, loc='upper right')
    for handle in lgnd.legendHandles:
        handle._sizes = [30]
    ax.xaxis.set_major_formatter(QvisTimeAxisFormatter)
    ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(xaxis_steps))
    ax.xaxis.set_label_text('Time (s)')
    ax.yaxis.set_label_text('RTT (ms)')
    fig.savefig(output_path, bbox_inches='tight', dpi=600)
    print(f'saved plot as {output_path}')
    plt.plot()


# plot(72, 144, './plots/compare_rtt_72ms_server.pdf')
# plot(220, 440, './plots/compare_rtt_220ms_server.pdf')
# plot(500, 1000, './plots/compare_rtt_500ms_server.pdf')
plot(1000, 2000, './plots/compare_rtt_1000ms_server.pdf')
plot(2000, 4000, './plots/compare_rtt_2000ms_server.pdf')
