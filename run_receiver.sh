#!/bin/bash

target_dir="alphartc/target"
target_lib_dir="${target_dir}/lib"
target_bin_dir="${target_dir}/bin"
target_pylib_dir="${target_dir}/pylib"

export LD_LIBRARY_PATH="${target_lib_dir}:$LD_LIBRARY_PATH"
export PYTHONPATH="${target_pylib_dir}:$PYTHONPATH"
export PATH="alphartc/target/lib:$PATH"
export PATH="alphartc/target/bin:$PATH"

executable="$target_bin_dir/peerconnection_serverless"
config_file="$target_bin_dir/receiver_pyinfer.json"

if [ ! -z "$MAHIMAHI_BASE" ]; then
  DEST_IP=$(
    ip addr show ingress \
      | grep -w "inet" \
      | awk '{print $2}' \
      | cut -d/ -f1
  )
else
  DEST_IP="0.0.0.0"
fi

jq --arg ip "$DEST_IP" '.serverless_connection.sender.dest_ip = $ip' alphartc/target/bin/sender_pyinfer.json > temp.json && mv temp.json alphartc/target/bin/sender_pyinfer.json
jq --arg ip "$DEST_IP" '.serverless_connection.sender.dest_ip = $ip' alphartc/target/bin/sender.json > temp.json && mv temp.json alphartc/target/bin/sender.json


if [[ ! -f "$executable" ]]; then
    echo "Error: Executable file '$executable' not found."
    exit 1
fi

if [[ ! -f "$config_file" ]]; then
    echo "Error: Configuration file '$config_file' not found."
    exit 1
fi


echo "Executing: $executable $config_file"
"$executable" "$config_file"