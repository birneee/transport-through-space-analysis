#!/usr/bin/env python
import matplotlib
from matplotlib import pyplot as plt, transforms
from qvis.plot import QvisByteAxisFormatter

from qvis_qperf.connection import load_all_connections
from qvis_qperf.plot import plot_bytes_at_second

def plot(max_s:float=40, output_name:str ='total_data'):
    plt.rcParams.update({
        "font.family": "serif",
        "text.usetex": True,
        "pgf.rcfonts": False,
    })
    fig, ax = plt.subplots()
    offset = lambda p: transforms.ScaledTranslation(p / 72., 0, plt.gcf().dpi_scale_trans)
    trans = plt.gca().transData
    xlabels = ['72\,ms RTT', '220\,ms RTT', '500\,ms RTT', '1000\,ms RTT', '2000\,ms RTT']

    plot_bytes_at_second(ax, [
        load_all_connections('./data/72ms/qperf'),
        load_all_connections('./data/220ms/qperf'),
        load_all_connections('./data/500ms/qperf'),
        load_all_connections('./data/1000ms/qperf'),
        load_all_connections('./data/2000ms/qperf'),
    ], max_s, x=xlabels, label='No PEP', transform=trans + offset(-28), color="#253c4b")

    plot_bytes_at_second(ax, [
        load_all_connections('./data/72ms_client_side_proxy/qperf'),
        load_all_connections('./data/220ms_client_side_proxy/qperf'),
        load_all_connections('./data/500ms_client_side_proxy/qperf'),
        load_all_connections('./data/1000ms_client_side_proxy/qperf'),
        load_all_connections('./data/2000ms_client_side_proxy/qperf'),
    ], max_s, x=xlabels, label='Client-side PEP', transform=trans + offset(-14), color="#00885c")

    plot_bytes_at_second(ax, [
        load_all_connections('./data/72ms_two_proxies_simple/qperf'),
        load_all_connections('./data/220ms_two_proxies_simple/qperf'),
        load_all_connections('./data/500ms_two_proxies_simple/qperf'),
        load_all_connections('./data/1000ms_two_proxies_simple/qperf'),
        load_all_connections('./data/2000ms_two_proxies_simple/qperf'),
    ], max_s, x=xlabels, label='Distributed PEP', color="#ffa600")

    plot_bytes_at_second(ax, [
        load_all_connections('./data/72ms_two_proxies_simple_xse/qperf'),
        load_all_connections('./data/220ms_two_proxies_simple_xse/qperf'),
        load_all_connections('./data/500ms_two_proxies_simple_xse/qperf'),
        load_all_connections('./data/1000ms_two_proxies_simple_xse/qperf'),
    ], max_s, x=xlabels[:-1], label='Distributed PEP (XSE)', transform=trans + offset(14), color="#bc32cf")

    plot_bytes_at_second(ax, [
        load_all_connections('./data/72ms_two_proxies/qperf'),
        load_all_connections('./data/220ms_two_proxies/qperf'),
        load_all_connections('./data/500ms_two_proxies/qperf'),
        load_all_connections('./data/1000ms_two_proxies/qperf'),
        load_all_connections('./data/2000ms_two_proxies/qperf'),
    ], max_s, x=xlabels, color='tab:orange', label='Distributed PEP (static CC)', transform=trans + offset(28))

    ax.xaxis.set_label_text('Scenario')
    ax.yaxis.set_label_text('Data (bytes)')
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('left')
    ax.margins(x=0.2)
    ax.grid(True, axis='y')
    ax.set_axisbelow(True)
    ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(50_000_000))
    lgnd = ax.legend(fancybox=False, shadow=False, loc='lower center', bbox_to_anchor=(0.47, -0.25), ncol=3,
                     frameon=False)
    for handle in lgnd.legendHandles:
        handle._alpha = 1
    ax.yaxis.set_major_formatter(QvisByteAxisFormatter)  # works for bits to
    fig.set_size_inches(8, 5)
    output_path = f'./plots/{output_name}.pdf'
    fig.savefig(output_path, bbox_inches='tight', dpi=300)
    print(f'saved plot as {output_path}')
    plt.plot()

plot(40, 'total_data_40s')
