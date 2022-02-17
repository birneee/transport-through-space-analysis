import time
from connection import Connection


def plot_rate(connection: Connection, color: str = '#0000ff', label: str = 'Stream data received'):
        start = time.time()
        ms, cum_length = zip(*map(lambda f: (f.time, f.offset + f.length),
                                  conn.received_stream_frames_of_stream(stream_id)))
        seconds = list(map(lambda m: m / 1000, ms))
        ax.scatter(x=seconds, y=cum_length, s=1.5, rasterized=True, label=label, color=color)
        print(f'plotted in {time.time() - start}s')