import time
from typing import List

from .aggregated_connection import AggregatedConnection
from .connection import Connection
from matplotlib.axes import Axes


def plot_rate(ax: Axes, connection: Connection | AggregatedConnection, color: str = '#0000ff',
              label: str | None = 'Rate', marker: str | None = None, linewidth: float = 1, alpha: float = 1,
              markersize: float = 5):
    start = time.time()
    seconds: List[int]
    download_rates: List[float]
    if isinstance(connection, Connection):
        seconds = list(map(lambda r: r.time, connection.reports))
        download_rates = list(map(lambda r: r.download_rate, connection.reports))
    elif isinstance(connection, AggregatedConnection):
        seconds = list(map(lambda r: r.time, connection.reports))
        download_rates = list(map(lambda r: r.avg_download_rate, connection.reports))
    else:
        raise "unsupported type"
    ax.plot(seconds, download_rates, rasterized=True, label=label, color=color, marker=marker, linewidth=linewidth,
            alpha=alpha, markersize=markersize)
    print(f'plotted in {time.time() - start}s')
