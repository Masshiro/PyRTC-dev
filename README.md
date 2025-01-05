# PyRTC-dev

## Usage

Clone this repo and initialize the submodule [AlphaRTC](https://github.com/OpenNetLab/AlphaRTC):
```shell
git clone --recurse-submodules <URL>
```
or update the cloned repo
```shell
git submodule update --init --recursive
```

To prevent unexpected changes to AlphaRTC source, you may want to run:
```shell
git config submodule.alphartc.ignore all
git update-index --assume-unchanged .gclient_previous_sync_commits
```

Initially, you need to follow the [step here](https://commondatastorage.googleapis.com/chrome-infra-docs/flat/depot_tools/docs/html/depot_tools_tutorial.html#_setting_up) to install `depot_tools`. And ensure some packeges has been installed in your system:
```shell
sudo apt install pkg-config ninja-build
```

and then make sure `gn` tool is correctly configured by running: 
```shell
cd alphartc
gclient sync && mv src/* .
cd ..
```
When it's done, verify by calling `gn --version`.

Then build the AlphaRTC using script:
```shell
. build.sh
```

For the receiver client, use script to start:
```shell
. run_receiver.sh
```

For the sender client, use script in another shell to start:
```shell
. run_sender.sh
```

For updating AlphaRTC, you can do the followings:
```shell
cd alphartc
git pull origin main

cd ..
git add alphartc
git commit -m "Update alphartc to latest upstream version"
git push origin <branch_name>
```

Create Docker network:
```shell
docker network create --subnet=192.168.2.0/24 rtcnet
```

Run each docker with:
```shell
docker run -it --rm --privileged -v share:/app/share --network rtcnet --ip 192.168.2.101 --name rtc_c1 pyrtc_image

docker run -it --rm --privileged -v share:/app/share --network rtcnet --ip 192.168.2.102 --name rtc_c2 pyrtc_image
```

## Requirements
- `jq`: `sudo apt-get install jq`


## Resources
- [AlphaRTC](https://github.com/OpenNetLab/AlphaRTC)
- [Mahimahi Manual](https://manpages.debian.org/testing/mahimahi/)