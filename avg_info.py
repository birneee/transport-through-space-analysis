#!/usr/bin/env python
from typing import List

from qvis_qperf.aggregated_connection import AggregatedConnection
from qvis_qperf.connection import Connection, load_all_connections


def create_report(connections: List[Connection], output_name: str):
    agg_connection = AggregatedConnection(connections)
    
    with open(f'./results/{output_name}.txt', 'w') as f:
        f.write(f'runs: {len(connections)}\n')
        f.write(f'runs with internal errors: {len(list(filter(lambda c: c.internal_error is not None, connections)))}\n')
        f.write(f'mean time to first byte: {agg_connection.time_to_first_byte} s\n')
        f.write(f'mean rate: {agg_connection.mean_rate} bit/s\n')
        f.write(f'total at 5s: {agg_connection.total_bytes_at(5)} byte\n')
        f.write(f'total at 10s: {agg_connection.total_bytes_at(10)} byte\n')
        f.write(f'total at 20s: {agg_connection.total_bytes_at(20)} byte\n')
        f.write(f'total at 30s: {agg_connection.total_bytes_at(30)} byte\n')
        f.write(f'total at 40s: {agg_connection.total_bytes_at(40)} byte\n')
        f.write(f'time to first 1MB: {agg_connection.to_avg_connection().time_to_received_bytes(1_000_000)} s\n')
        f.write(f'time to first 2MB: {agg_connection.to_avg_connection().time_to_received_bytes(2_000_000)} s\n')
        f.write(f'time to first 10MB: {agg_connection.to_avg_connection().time_to_received_bytes(10_000_000)} s\n')
        f.write(f'time to first 100MB: {agg_connection.to_avg_connection().time_to_received_bytes(100_000_000)} s\n')


create_report(load_all_connections('./data/72ms/qperf'), 'avg_info_72ms')
create_report(load_all_connections('./data/72ms_client_side_proxy/qperf'), 'avg_info_72ms_client_side_proxy')
create_report(load_all_connections('./data/72ms_two_proxies/qperf'), 'avg_info_72ms_two_proxies')
create_report(load_all_connections('./data/72ms_two_proxies_simple/qperf'), 'avg_info_72ms_two_proxies_simple')
create_report(load_all_connections('./data/72ms_two_proxies_simple_xse/qperf'), 'avg_info_72ms_two_proxies_simple_xse')

create_report(load_all_connections('./data/220ms/qperf'), 'avg_info_220ms')
create_report(load_all_connections('./data/220ms_client_side_proxy/qperf'), 'avg_info_220ms_client_side_proxy')
create_report(load_all_connections('./data/220ms_two_proxies/qperf'), 'avg_info_220ms_two_proxies')
create_report(load_all_connections('./data/220ms_two_proxies_simple/qperf'), 'avg_info_220ms_two_proxies_simple')
create_report(load_all_connections('./data/220ms_two_proxies_simple_xse/qperf'), 'avg_info_220ms_two_proxies_simple_xse')

create_report(load_all_connections('./data/500ms/qperf'), 'avg_info_500ms')
create_report(load_all_connections('./data/500ms_client_side_proxy/qperf'), 'avg_info_500ms_client_side_proxy')
create_report(load_all_connections('./data/500ms_two_proxies/qperf'), 'avg_info_500ms_two_proxies')
create_report(load_all_connections('./data/500ms_two_proxies_simple/qperf'), 'avg_info_500ms_two_proxies_simple')
create_report(load_all_connections('./data/500ms_two_proxies_simple_xse/qperf'), 'avg_info_500ms_two_proxies_simple_xse')

create_report(load_all_connections('./data/1000ms/qperf'), 'avg_info_1000ms')
create_report(load_all_connections('./data/1000ms_client_side_proxy/qperf'), 'avg_info_1000ms_client_side_proxy')
create_report(load_all_connections('./data/1000ms_two_proxies/qperf'), 'avg_info_1000ms_two_proxies')
create_report(load_all_connections('./data/1000ms_two_proxies_simple/qperf'), 'avg_info_1000ms_two_proxies_simple')
create_report(load_all_connections('./data/1000ms_two_proxies_simple_xse/qperf'), 'avg_info_1000ms_two_proxies_simple_xse')

create_report(load_all_connections('./data/2000ms/qperf'), 'avg_info_2000ms')
create_report(load_all_connections('./data/2000ms_client_side_proxy/qperf'), 'avg_info_2000ms_client_side_proxy')
create_report(load_all_connections('./data/2000ms_two_proxies/qperf'), 'avg_info_2000ms_two_proxies')
create_report(load_all_connections('./data/2000ms_two_proxies_simple/qperf'), 'avg_info_2000ms_two_proxies_simple')
