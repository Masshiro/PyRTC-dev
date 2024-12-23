#!/bin/bash

output_dir="alphartc/out/Default"
target_dir="alphartc/target"
target_lib_dir="${target_dir}/lib"
target_bin_dir="${target_dir}/bin"
target_pylib_dir="${target_dir}/pylib"


if [ -d "${output_dir}" ]; then
    echo "=> Directory ${output_dir} exists. Deleting..."
    rm -rf "${output_dir}"
fi

if [ -d "${target_dir}" ]; then
    echo "=> Directory ${target_dir} exists. Deleting..."
    rm -rf "${target_dir}"
fi


echo "=> Building peerconnection_serverless using ninja..."
gn gen "${output_dir}"
ninja -C "${output_dir}" peerconnection_serverless


echo "=> Creating target directories..."
mkdir -p "${target_lib_dir}"
mkdir -p "${target_bin_dir}"
mkdir -p "${target_pylib_dir}"


echo "=> Copying files and shared libraries..."
cp -r share/input/* "${target_bin_dir}"
cp alphartc/modules/third_party/onnxinfer/lib/*.so "${target_lib_dir}"
cp alphartc/modules/third_party/onnxinfer/lib/*.so.* "${target_lib_dir}"


echo "=> Copying executables and Python scripts..."
cp "${output_dir}/peerconnection_serverless" "${target_bin_dir}/peerconnection_serverless.origin"
cp alphartc/examples/peerconnection/serverless/peerconnection_serverless "${target_bin_dir}"
cp alphartc/modules/third_party/cmdinfer/*.py "${target_pylib_dir}/"


echo "=> Build and file copy processes completed."
