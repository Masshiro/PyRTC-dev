# PyRTC-dev

## Usage
- Clone the repo
```shell
git clone --recurse-submodules <URL>
```
or update the cloned repo
```shell
git submodule update --init --recursive
```

- To prevent unexpected changes to submodules, you may want to run:
```shell
git config submodule.alphartc.ignore all
git update-index --assume-unchanged .gclient_previous_sync_commits
```

- For the first-time run: make sure `gn` tool is correctly configured: 
```shell
cd alphartc
gclient sync && mv src/* .
cd ..
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

- Maintenance
```shell
cd alphartc
git pull origin main

cd ..
git add alphartc
git commit -m "Update alphartc to latest upstream version"
git push origin <branch_name>
```

## TODO
- [ ] Build a JSON configration tool (set options and eventually generate corresponding files e.g. `sender_pyinfer.json`)

- [ ] `share/input` (everything in `examples/peerconnection/serverless/corpus/`):
    - `sender_pyinfer.json` & `receiver_pyinfer.json`
    - `sender.json` & `receiver.json`
    - `test.yuv` (test media, only video is supported)
    - `onnx-model.onnx`
    - `BandwidthEstimator.py`