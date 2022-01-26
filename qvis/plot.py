import time
from typing import Iterator, Optional

import matplotlib.transforms as transforms
import numpy as np
from matplotlib.axes import Axes
from matplotlib.ticker import FuncFormatter

from .connection import Connection


def byte_axis_formatter(bytes: int, position: int) -> str:
    if bytes > 1000000:
        return f'{bytes / 1000000:.0f}M'
    if bytes > 1000:
        return f'{bytes / 1000:.0f}K'
    return f'{bytes:.0f}'


QvisTimeAxisFormatter = FuncFormatter(lambda seconds, position: f'{seconds:.0f}')
QvisByteAxisFormatter = FuncFormatter(byte_axis_formatter)


def extend_time(conn: Connection, values: Iterator[tuple[float, any]]) -> Iterator[tuple[float, any]]:
    value = None
    for new_value in values:
        value = new_value
        yield value
    if value is not None:
        yield conn.max_time, value[1]


def plot_remote_stream_flow_limit(ax: Axes, conn: Connection, stream_id: int, color: str = '#ff69b4',
                                  label: str | None = 'Stream flow control limits', linestyle: str = 'solid'):
    start = time.time()
    ms, limits = zip(*extend_time(conn, conn.remote_stream_flow_limit_updates(stream_id)))
    seconds = list(map(lambda m: m / 1000, ms))
    seconds.insert(0, 0)
    ax.stairs(values=limits, edges=seconds, baseline=None, color=color, label=label, linestyle=linestyle)
    print(f'plotted in {time.time() - start}s')


def plot_local_stream_flow_limit(ax: Axes, conn: Connection, stream_id: int, color: str = '#ff69b4',
                                  label: str | None = 'Stream flow control limits', linestyle: str = 'solid'):
    start = time.time()
    ms, limits = zip(*extend_time(conn, conn.local_stream_flow_limit_updates(stream_id)))
    seconds = list(map(lambda m: m / 1000, ms))
    seconds.insert(0, 0)
    ax.stairs(values=limits, edges=seconds, baseline=None, color=color, label=label, linestyle=linestyle)
    print(f'plotted in {time.time() - start}s')


def plot_connection_flow_limit(ax: Axes, conn: Connection):
    start = time.time()
    ms, limits = zip(*conn.connection_flow_limit_updates())
    seconds = list(map(lambda m: m / 1000, ms))
    seconds.insert(0, 0)
    ax.stairs(values=limits, edges=seconds, baseline=None, color='#a80f3a', label='Connection flow control limit')
    print(f'plotted in {time.time() - start}s')


def plot_congestion_window(ax: Axes, conn: Connection, color: str = '#8a2be2', label: str | None = 'Congestion window',
                           linestyle: str = 'solid'):
    start = time.time()
    ms, window = zip(*extend_time(conn, conn.congestion_window_updates))
    seconds = list(map(lambda m: m / 1000, ms))
    seconds.insert(0, 0)
    ax.stairs(values=window, edges=seconds, baseline=None, color=color, label=label, linestyle=linestyle)
    print(f'plotted in {time.time() - start}s')


def plot_rtt(ax: Axes, conn: Connection, color: str = '#ff9900', label: str | None = 'Latest RTT',
             linestyle: str = 'solid'):
    start = time.time()
    ms, window = zip(*extend_time(conn, conn.rtt_updates))
    seconds = list(map(lambda m: m / 1000, ms))
    seconds.insert(0, 0)
    ax.stairs(values=window, edges=seconds, baseline=None, color=color, label=label, linestyle=linestyle)
    print(f'plotted in {time.time() - start}s')


def plot_bytes_in_flight(ax: Axes, conn: Connection, color: str = '#808000', label: str | None = 'Bytes in flight'):
    start = time.time()
    ms, in_flight = zip(*conn.bytes_in_flight_updates)
    seconds = list(map(lambda m: m / 1000, ms))
    seconds.insert(0, 0)
    ax.stairs(values=in_flight, edges=seconds, baseline=None, color=color, label=label)
    print(f'plotted in {time.time() - start}s')


def plot_raw_data_sent(ax: Axes, conn: Connection, color: str = '#0000ff',
                       label: str = 'Data sent (includes retransmits)'):
    start = time.time()
    ms, length = zip(*map(lambda f: (f.time, f.raw_length),
                          conn.sent_packets))
    seconds = list(map(lambda m: m / 1000, ms))
    cum_length = np.cumsum(length)
    ax.scatter(x=seconds, y=cum_length, s=1.5, rasterized=True, label=label, color=color)
    print(f'plotted in {time.time() - start}s')


def plot_stream_data_sent(ax: Axes, conn: Connection, stream_id: int, color: str = '#0000ff',
                          label: str = 'Stream data sent'):
    start = time.time()
    ms, cum_length = zip(*map(lambda f: (f.time, f.offset + f.length),
                              conn.sent_stream_frames_of_stream(stream_id)))
    seconds = list(map(lambda m: m / 1000, ms))
    ax.scatter(x=seconds, y=cum_length, s=1.5, rasterized=True, label=label, color=color)
    print(f'plotted in {time.time() - start}s')


def plot_stream_data_received(ax: Axes, conn: Connection, stream_id: int, color: str = '#0000ff',
                              label: str = 'Stream data received'):
    start = time.time()
    ms, cum_length = zip(*map(lambda f: (f.time, f.offset + f.length),
                              conn.received_stream_frames_of_stream(stream_id)))
    seconds = list(map(lambda m: m / 1000, ms))
    ax.scatter(x=seconds, y=cum_length, s=1.5, rasterized=True, label=label, color=color)
    print(f'plotted in {time.time() - start}s')


def plot_time_to_first_byte(ax: Axes, conn: Connection, stream_id: int, color: str = 'black',
                            label: Optional[str] = 'Time to first byte'):
    ttfb = conn.time_to_first_byte(stream_id)
    ax.scatter(ttfb / 1000, 0, marker='^', color=color, label=label, clip_on=False, zorder=100, linewidth=1, s=12,
               # path_effects=[path_effects.SimpleLineShadow(shadow_color='red', offset=(0.5, 0.5)), path_effects.Normal()],
               transform=transforms.offset_copy(ax.transData, fig=ax.figure, x=0, y=-2.5, units='points')
               )
