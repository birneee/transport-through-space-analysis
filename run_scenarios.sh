#!/bin/bash

QPERF_BIN=$(realpath "../qperf-go/qperf-go")
SCENARIO_DIR=$(realpath "../qperf-go/scenarios")
OUTPUT_DIR=$(realpath "data")

PATH="$PATH:$SCENARIO_DIR"

function rename_qlog() {
  find . -maxdepth 1 -name '*.qlog' -exec perl-rename 's/^(.+)_[0-9a-f]+\.qlog/$1\.qlog/' {} \;
}

function zip_qlog() {
  find . -maxdepth 1 -name '*.qlog' -exec gzip {} \;
}

# QLOG no proxies

(
  DIR=$OUTPUT_DIR/72ms/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=72 QLOG=1 delay.sh
    rename_qlog
    zip_qlog
  fi
)

(
  DIR=$OUTPUT_DIR/220ms/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=220 QLOG=1 delay.sh
    rename_qlog
    zip_qlog
  fi
)

(
  DIR=$OUTPUT_DIR/500ms/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=500 QLOG=1 delay.sh
    rename_qlog
    zip_qlog
  fi
)

(
  DIR=$OUTPUT_DIR/1000ms/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=1000 QLOG=1 delay.sh
    rename_qlog
    zip_qlog
  fi
)

(
  DIR=$OUTPUT_DIR/2000ms/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=2000 QLOG=1 delay.sh
    rename_qlog
    zip_qlog
  fi
)

# QLOG client side proxy

(
  DIR=$OUTPUT_DIR/72ms_client_side_proxy/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=72 QLOG=1 delay_proxy.sh
    rename_qlog
    zip_qlog
  fi
)

(
  DIR=$OUTPUT_DIR/220ms_client_side_proxy/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=220 QLOG=1 delay_proxy.sh
    rename_qlog
    zip_qlog
  fi
)

(
  DIR=$OUTPUT_DIR/500ms_client_side_proxy/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=500 QLOG=1 delay_proxy.sh
    rename_qlog
    zip_qlog
  fi
)

(
  DIR=$OUTPUT_DIR/1000ms_client_side_proxy/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=1000 QLOG=1 delay_proxy.sh
    rename_qlog
    zip_qlog
  fi
)

(
  DIR=$OUTPUT_DIR/2000ms_client_side_proxy/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=2000 QLOG=1 delay_proxy.sh
    rename_qlog
    zip_qlog
  fi
)

# QLOG two proxies

(
  DIR=$OUTPUT_DIR/72ms_two_proxies/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=72 QLOG=1 delay_two_proxies.sh
    rename_qlog
    zip_qlog
  fi
)

(
  DIR=$OUTPUT_DIR/220ms_two_proxies/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=220 QLOG=1 delay_two_proxies.sh
    rename_qlog
    zip_qlog
  fi
)

(
  DIR=$OUTPUT_DIR/500ms_two_proxies/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=500 QLOG=1 delay_two_proxies.sh
    rename_qlog
    zip_qlog
  fi
)

(
  DIR=$OUTPUT_DIR/1000ms_two_proxies/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=1000 QLOG=1 delay_two_proxies.sh
    rename_qlog
    zip_qlog
  fi
)

(
  DIR=$OUTPUT_DIR/2000ms_two_proxies/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=2000 QLOG=1 delay_two_proxies.sh
    rename_qlog
    zip_qlog
  fi
)

# QLOG two proxies simple optimizations

(
  DIR=$OUTPUT_DIR/72ms_two_proxies_simple/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=72 QLOG=1 delay_two_proxies_simple.sh
    rename_qlog
    zip_qlog
  fi
)

(
  DIR=$OUTPUT_DIR/220ms_two_proxies_simple/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=220 QLOG=1 delay_two_proxies_simple.sh
    rename_qlog
    zip_qlog
  fi
)

(
  DIR=$OUTPUT_DIR/500ms_two_proxies_simple/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=500 QLOG=1 delay_two_proxies_simple.sh
    rename_qlog
    zip_qlog
  fi
)

(
  DIR=$OUTPUT_DIR/1000ms_two_proxies_simple/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=1000 QLOG=1 delay_two_proxies_simple.sh
    rename_qlog
    zip_qlog
  fi
)

(
  DIR=$OUTPUT_DIR/2000ms_two_proxies_simple/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=2000 QLOG=1 delay_two_proxies_simple.sh
    rename_qlog
    zip_qlog
  fi
)

# QLOG two proxies simple optimizations with XSE

(
  DIR=$OUTPUT_DIR/72ms_two_proxies_simple_xse/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=72 XSE=1 QLOG=1 delay_two_proxies_simple.sh
    rename_qlog
    zip_qlog
  fi
)

(
  DIR=$OUTPUT_DIR/220ms_two_proxies_simple_xse/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=220 XSE=1 QLOG=1 delay_two_proxies_simple.sh
    rename_qlog
    zip_qlog
  fi
)

(
  DIR=$OUTPUT_DIR/500ms_two_proxies_simple_xse/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=500 XSE=1 QLOG=1 delay_two_proxies_simple.sh
    rename_qlog
    zip_qlog
  fi
)

(
  DIR=$OUTPUT_DIR/1000ms_two_proxies_simple_xse/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=1000 XSE=1 QLOG=1 delay_two_proxies_simple.sh
    rename_qlog
    zip_qlog
  fi
)

(
  DIR=$OUTPUT_DIR/2000ms_two_proxies_simple_xse/qlog
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    RTT=2000 XSE=1 QLOG=1 delay_two_proxies_simple.sh
    rename_qlog
    zip_qlog
  fi
)

# QPERF no proxies

(
  DIR=$OUTPUT_DIR/72ms/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=72 RAW=1 INTERVAL=0.1 delay.sh | tee $i.log;
    done
  fi
)

(
  DIR=$OUTPUT_DIR/220ms/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=220 RAW=1 INTERVAL=0.1 delay.sh | tee $i.log;
    done
  fi
)

(
  DIR=$OUTPUT_DIR/500ms/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=500 RAW=1 INTERVAL=0.1 delay.sh | tee $i.log;
    done
  fi
)

(
  DIR=$OUTPUT_DIR/1000ms/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=1000 RAW=1 INTERVAL=0.1 delay.sh | tee $i.log;
    done
  fi
)

(
  DIR=$OUTPUT_DIR/2000ms/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=2000 RAW=1 INTERVAL=0.1 delay.sh | tee $i.log;
    done
  fi
)

# QPERF client side proxy

(
  DIR=$OUTPUT_DIR/72ms_client_side_proxy/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=72 RAW=1 INTERVAL=0.1 delay_proxy.sh | tee $i.log;
    done
  fi
)

(
  DIR=$OUTPUT_DIR/220ms_client_side_proxy/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=220 RAW=1 INTERVAL=0.1 delay_proxy.sh | tee $i.log;
    done
  fi
)

(
  DIR=$OUTPUT_DIR/500ms_client_side_proxy/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=500 RAW=1 INTERVAL=0.1 delay_proxy.sh | tee $i.log;
    done
  fi
)

(
  DIR=$OUTPUT_DIR/1000ms_client_side_proxy/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=1000 RAW=1 INTERVAL=0.1 delay_proxy.sh | tee $i.log;
    done
  fi
)

(
  DIR=$OUTPUT_DIR/2000ms_client_side_proxy/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=2000 RAW=1 INTERVAL=0.1 delay_proxy.sh | tee $i.log;
    done
  fi
)

# QPERF two proxies

(
  DIR=$OUTPUT_DIR/72ms_two_proxies/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=72 RAW=1 INTERVAL=0.1 delay_two_proxies.sh | tee $i.log;
    done
  fi
)

(
  DIR=$OUTPUT_DIR/220ms_two_proxies/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=220 RAW=1 INTERVAL=0.1 delay_two_proxies.sh | tee $i.log;
    done
  fi
)

(
  DIR=$OUTPUT_DIR/500ms_two_proxies/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=500 RAW=1 INTERVAL=0.1 delay_two_proxies.sh | tee $i.log;
    done
  fi
)

(
  DIR=$OUTPUT_DIR/1000ms_two_proxies/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=1000 RAW=1 INTERVAL=0.1 delay_two_proxies.sh | tee $i.log;
    done
  fi
)

(
  DIR=$OUTPUT_DIR/2000ms_two_proxies/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=2000 RAW=1 INTERVAL=0.1 delay_two_proxies.sh | tee $i.log;
    done
  fi
)

# QPERF two proxies simple optimizations

(
  DIR=$OUTPUT_DIR/72ms_two_proxies_simple/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=72 RAW=1 INTERVAL=0.1 delay_two_proxies_simple.sh | tee $i.log;
    done
  fi
)

(
  DIR=$OUTPUT_DIR/220ms_two_proxies_simple/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=220 RAW=1 INTERVAL=0.1 delay_two_proxies_simple.sh | tee $i.log;
    done
  fi
)

(
  DIR=$OUTPUT_DIR/500ms_two_proxies_simple/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=500 RAW=1 INTERVAL=0.1 delay_two_proxies_simple.sh | tee $i.log;
    done
  fi
)

(
  DIR=$OUTPUT_DIR/1000ms_two_proxies_simple/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=1000 RAW=1 INTERVAL=0.1 delay_two_proxies_simple.sh | tee $i.log;
    done
  fi
)

(
  DIR=$OUTPUT_DIR/2000ms_two_proxies_simple/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=2000 RAW=1 INTERVAL=0.1 delay_two_proxies_simple.sh | tee $i.log;
    done
  fi
)

# QPERF two proxies simple optimizations with XSE

(
  DIR=$OUTPUT_DIR/72ms_two_proxies_simple_xse/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=72 XSE=1 RAW=1 INTERVAL=0.1 delay_two_proxies_simple.sh | tee $i.log;
    done
  fi
)

(
  DIR=$OUTPUT_DIR/220ms_two_proxies_simple_xse/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=220 XSE=1 RAW=1 INTERVAL=0.1 delay_two_proxies_simple.sh | tee $i.log;
    done
  fi
)

(
  DIR=$OUTPUT_DIR/500ms_two_proxies_simple_xse/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=500 XSE=1 RAW=1 INTERVAL=0.1 delay_two_proxies_simple.sh | tee $i.log;
    done
  fi
)

(
  DIR=$OUTPUT_DIR/1000ms_two_proxies_simple_xse/qperf
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    cd "$DIR";
    for i in {1..100}; do
      RTT=1000 XSE=1 RAW=1 INTERVAL=0.1 delay_two_proxies_simple.sh | tee $i.log;
    done
  fi
)
