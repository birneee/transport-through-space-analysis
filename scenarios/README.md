# QPERF-GO Scenarios

## Delay Emulation

### Scripts

Following scripts require root privileges to create network namespaces.

- no_pep.sh
  - unmodified QUIC
- no_pep_optimized.sh
  - optimized congestion and receive window
- client_side_pep.sh
  - client-side proxy
  - optimized max receive window
- distributed_pep.sh
  - client-side and server-side proxy
  - optimized congestion and receive window
- distributed_pep_static_cc.sh
  - client-side and server-side proxy
  - optimized receive window and static congestion window

### Options

Following environment variables can be used to configure the scenarios.

- `RTT`
  - set the emulated RTT in ms
  - default: 1000 ms
- `BANDWIDTH`
  - set the emulated bandwidth in Mbit/s
  - default: 100 Mbit/s
- `QLOG`
  - enable qlog output for client, server and proxies (0 or 1)
  - default: 0
- `XSE`
  - enable XSE-QUIC extension (0 or 1)
  - default: 0
- `RAW`
  - enable raw qperf output (0 or 1)
  - default: 0
- `TIME`
  - transfer duration in seconds
  - default: 40

### Examples
```bash
RTT=250 BANDWIDTH=1000 QLOG=1 ./distributed_pep_static_cc.sh 
```
```bash
TIME=5 INTERVAL=0.5 ./no_pep.sh 
```

## Migration Emulation

TODO