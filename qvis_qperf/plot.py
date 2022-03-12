import time
from typing import List, Optional

import matplotlib
import numpy as np

from .aggregated_connection import AggregatedConnection
from matplotlib.axes import Axes
import matplotlib.transforms as transforms

from .connection import Connection, all_intersections


def plot_rate(ax: Axes, connection: Connection | AggregatedConnection | List[Connection], color: str = '#0000ff',
              label: str | None = 'Rate', marker: str | None = None, linewidth: float = 1, alpha: float = 1,
              markersize: float = 5, linestyle: str | None = 'solid'):
    """chunk_interval in seconds"""
    start = time.time()
    if isinstance(connection, Connection):
        seconds: List[int] = list(map(lambda r: r.time, connection.reports))
        download_rates: List[float] = list(map(lambda r: r.download_rate, connection.reports))
        ax.plot(seconds, download_rates, rasterized=True, label=label, color=color, marker=marker, linewidth=linewidth,
                alpha=alpha, markersize=markersize, linestyle=linestyle)
    elif isinstance(connection, AggregatedConnection):
        plot_rate(ax, connection.to_avg_connection(), color=color, label=label, marker=marker, linewidth=linewidth,
                  alpha=alpha, markersize=markersize, linestyle=linestyle)
    elif isinstance(connection, List):
        connections = connection
        for index, connection in enumerate(connections):
            if index == 0:
                plot_rate(ax, connection, color=color, label=label, marker=marker, linewidth=linewidth, alpha=alpha,
                          markersize=markersize, linestyle=linestyle)
            else:
                plot_rate(ax, connection, color=color, label=None, marker=marker, linewidth=linewidth, alpha=alpha,
                          markersize=markersize, linestyle=linestyle)
    else:
        raise "unsupported type"
    print(f'plotted in {time.time() - start}s')


def plot_time_to_first_byte(ax: Axes, connection: Connection | AggregatedConnection, color: str = 'black',
                            label: Optional[str] = 'Time to first byte'):
    ttfb: float  # in seconds
    if isinstance(connection, Connection):
        ttfb = connection.time_to_first_byte
    elif isinstance(connection, AggregatedConnection):
        ttfb = connection.time_to_first_byte
    else:
        raise "unsupported type"
    ax.scatter(ttfb, 0, marker='^', color=color, label=label, clip_on=False, zorder=100, linewidth=1, s=12,
               transform=transforms.offset_copy(ax.transData, fig=ax.figure, x=0, y=-2.5, units='points'))


def plot_data_received(ax: Axes, connection: Connection | AggregatedConnection, color: Optional[str] = None,
                       label: Optional[str] = None, rasterized: bool = False, marker: Optional[str] = None,
                       linewidth: float = 1, markersize: float = 5, linestyle: Optional[str] = 'solid'):
    start = time.time()
    if isinstance(connection, Connection):
        seconds: List[int] = list(map(lambda r: r.time, connection.reports))
        bytes_received: List[float] = list(map(lambda r: r.bytes_received, connection.reports))
        bytes_received = np.cumsum(bytes_received)
        ax.plot(seconds, bytes_received, rasterized=rasterized, label=label, color=color, marker=marker,
                linewidth=linewidth, markersize=markersize, linestyle=linestyle)
    elif isinstance(connection, AggregatedConnection):
        plot_data_received(ax, connection.to_avg_connection(), rasterized=rasterized, label=label, color=color,
                           marker=marker, linewidth=linewidth, markersize=markersize, linestyle=linestyle)
    else:
        raise "unsupported type"
    print(f'plotted in {time.time() - start}s')


def plot_data_received_intersection(ax: Axes, connections: List[Connection], colors: [str], label: str = 'Intersections', markersize=None):
    up_marker = matplotlib.markers.MarkerStyle(marker='|')
    up_marker._transform = up_marker.get_transform().rotate_deg(-20)
    down_marker = matplotlib.markers.MarkerStyle(marker='|')
    down_marker._transform = down_marker.get_transform().rotate_deg(20)

    if label is not None:
        # fake plot for legend entry
        ax.plot(0, 0, marker=down_marker, markersize=markersize, color=colors[0], label=label, linewidth=0, alpha=0.0)

    # real plot
    for interception in all_intersections(connections):
        upper_color = colors[connections.index(interception.upper)]
        lower_color = colors[connections.index(interception.lower)]
        ax.plot(interception.time, interception.bytes_received, marker=up_marker, color = upper_color, markersize=markersize)
        ax.plot(interception.time, interception.bytes_received, marker=down_marker, color = lower_color, markersize=markersize)
