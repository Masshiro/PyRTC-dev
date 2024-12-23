# PyRTC-dev

## Usage
- Clone the repo
```shell
git clone --recurse-submodules <URL>
```
or use simple clone and then run
```shell
git submodule update --init --recursive
```

- For the first-time run: make sure `gn` tool is correctly configured: 
```shell
cd alphartc
gclient sync
mv src/* .
```
When it's done, verify by calling `gn --version`.

- Build AlphaRTC
```shell
. build_serverless.sh
```

- For the receiver client, use script to start:
```shell
. serverless_receiver.sh
```

- For the sender client, use script in another shell to start:
```shell
. serverless_sender.sh
```

## TODO
- [ ] Build a JSON configration tool (set options and eventually generate corresponding files e.g. `sender_pyinfer.json`)

- [ ] `share/input` (everything in `examples/peerconnection/serverless/corpus/`):
    - `sender_pyinfer.json` & `receiver_pyinfer.json`
    - `sender.json` & `receiver.json`
    - `test.yuv` (test media, only video is supported)
    - `onnx-model.onnx`
    - `BandwidthEstimator.py`