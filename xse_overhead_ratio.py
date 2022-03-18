#!/usr/bin/env python
import os

from matplotlib import pyplot as plt
from qvis.connection import Connection, read_qlog
from qvis.plot import plot_received_xse_overhead_ratio

def plot():
    file_name = os.path.splitext(os.path.basename(__file__))[0]
    """file name of this script without extension"""

    max_ms = 10000

    conn_72ms: Connection = read_qlog('./data/72ms_two_proxies_simple_xse/qlog/client.qlog.gz', max_ms=max_ms)
    conn_220ms: Connection = read_qlog('./data/220ms_two_proxies_simple_xse/qlog/client.qlog.gz', max_ms=max_ms)
    conn_500ms: Connection = read_qlog('./data/500ms_two_proxies_simple_xse/qlog/client.qlog.gz', max_ms=max_ms)
    conn_1000ms: Connection = read_qlog('./data/1000ms_two_proxies_simple_xse/qlog/client.qlog.gz', max_ms=max_ms)

    plt.rcParams.update({
        "font.family": "serif",
        "text.usetex": True,
        "pgf.rcfonts": False,
    })
    fig, ax = plt.subplots()
    min_ratio = (16405 - 16384) / 16384
    ax.axline((0, min_ratio), (1, min_ratio), color='gray', linestyle=(0, (1, 10)))
    plot_received_xse_overhead_ratio(ax, conn_72ms, 0, label='72\,ms', color='tab:blue', shift_ms=-conn_72ms.time_to_first_byte(0), markersize=5)
    plot_received_xse_overhead_ratio(ax, conn_220ms, 0, label='220\,ms', color='tab:orange', shift_ms=-conn_220ms.time_to_first_byte(0), markersize=5)
    plot_received_xse_overhead_ratio(ax, conn_500ms, 0, label='500\,ms', color='tab:green', shift_ms=-conn_500ms.time_to_first_byte(0), markersize=5)
    plot_received_xse_overhead_ratio(ax, conn_1000ms, 0, label='1000\,ms', color='tab:red', shift_ms=-conn_1000ms.time_to_first_byte(0), markersize=5)
    fig.set_size_inches(8, 6)
    ax.set_axisbelow(True)
    ax.grid(True)
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0, xmax=0.02)
    lgnd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False)
    for handle in lgnd.legendHandles:
        handle._sizes = [30]
    ax.xaxis.set_label_text('Time (s)')
    ax.yaxis.set_label_text('Ratio')
    output_path = f'./plots/{file_name}.pdf'
    fig.savefig(output_path, bbox_inches='tight', dpi=600)
    print(f'saved plot as {output_path}')
    plt.plot()


def report(connection: Connection, xse_connection: Connection, output_file: str):
    with open(output_file, 'w') as f:
        f.write(f'without xse: {connection.avg_stream_receive_rate(0)} bit/s\n')
        xse_raw = xse_connection.avg_raw_xse_stream_receive_rate(0)
        f.write(f'with xse: raw: {xse_raw} bit/s\n')
        xse_data = xse_connection.avg_xse_stream_receive_rate(0)
        f.write(f'with xse: payload: {xse_data} bit/s\n')
        overhead_ratio = (xse_raw - xse_data) / xse_data
        f.write(f'with xse: overhead: {overhead_ratio}\n')

plot()

report(read_qlog('./data/72ms_two_proxies_simple/qlog/client.qlog.gz'), read_qlog('./data/72ms_two_proxies_simple_xse/qlog/client.qlog.gz'), './results/xse_overhead_72ms.txt')
report(read_qlog('./data/220ms_two_proxies_simple/qlog/client.qlog.gz'), read_qlog('./data/220ms_two_proxies_simple_xse/qlog/client.qlog.gz'), './results/xse_overhead_220ms.txt')
report(read_qlog('./data/500ms_two_proxies_simple/qlog/client.qlog.gz'), read_qlog('./data/500ms_two_proxies_simple_xse/qlog/client.qlog.gz'), './results/xse_overhead_500ms.txt')
report(read_qlog('./data/1000ms_two_proxies_simple/qlog/client.qlog.gz'), read_qlog('./data/1000ms_two_proxies_simple_xse/qlog/client.qlog.gz'), './results/xse_overhead_1000ms.txt')
report(read_qlog('./data/2000ms_two_proxies_simple/qlog/client.qlog.gz'), read_qlog('./data/2000ms_two_proxies_simple_xse/qlog/client.qlog.gz'), './results/xse_overhead_2000ms.txt')
