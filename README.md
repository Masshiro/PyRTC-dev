# PyRTC-dev

## Prerequisites

To fully utilize this repository, make sure that Ubuntu 20.04 or 22.04 is using and following tools are installed.

- Docker Engine: [official installation guide](https://docs.docker.com/engine/install/)
- Docker Compose: [official installation guide](https://docs.docker.com/compose/install/)
- Containernet: [official installation guide](https://github.com/containernet/containernet?tab=readme-ov-file#installation)
- Mahimahi: [official installation guide](http://mahimahi.mit.edu/#getting)

## Usage

### Get things ready

Firstly, you may want to clone this repo and initialize the submodule [AlphaRTC](https://github.com/OpenNetLab/AlphaRTC):
```shell
git clone --recurse-submodules <URL>
```
or update the cloned repo using
```shell
git submodule update --init --recursive
```

To prevent unexpected changes to AlphaRTC source, you may want to run:
```shell
git config submodule.alphartc.ignore all
git update-index --assume-unchanged .gclient_previous_sync_commits
```

To build AlphaRTC and make it function, you may need to follow [the installation steps](https://commondatastorage.googleapis.com/chrome-infra-docs/flat/depot_tools/docs/html/depot_tools_tutorial.html#_setting_up) to get `depot_tools`. After doing that, use the build script at the root directory of this repository:

```shell
. build.sh
```

- `pkg-config` and `ninja-build` should be installed to ensure the building process go smoothly.

Then you can create docker image named `pyrtc_image:latest` by default along with the docker network which would be used in following trace-driven simulation and named `rtcnet` by default:

```shell
make setup
```

- or you can create image or network separately by using either `make build` or `make network`.

### Trace-driven simulation

Since the default subnet of `rtcnet` is 192.168.2.0/24, two containers can be started with specific IP addresses accordingly.

For receiver container, run:

```shell
docker run -it --rm --privileged -v $(pwd)/share:/app/share --network rtcnet --ip 192.168.2.102 --name rtc_c2 pyrtc_image
```

- then in the bash shell of it, run `python run.py`

For sender container, run:

```shell
docker run -it --rm --privileged -v $(pwd)/share:/app/share --network rtcnet --ip 192.168.2.101 --name rtc_c1 pyrtc_image
```

- then in the bash shell of it, `CMD=$(python3 utils/mahi_helpers.py) && $CMD -- python run.py --sender`

Or you can run the sender and receiver processes automatically via Docker Compose:

```shell
docker compose up
```

- when the simulation finished, run `docker compose down`


### Topology-based simulation
In addtion to the trace-driven simulation, we further construct two kind of topologies for the tests, which are dumbbell and parking-lot, respectively. They are formed using [Containernet](https://containernet.github.io/), a extension of the [Mininet](https://mininet.org/), with traditional nodes being replaced by Docker containers. The details of both topologies' defination can be found at [former work's repository](https://github.com/Zhiming-Huang/luc).

Suppose containernet has been installed following [bare-metal option](https://github.com/containernet/containernet?tab=readme-ov-file#option-1-bare-metal-installation), you may first start the virtual Python environment in which containernet was maintained:
```shell
source path/to/your/venv/bin/activate
```
then run either simulation by:
- ```shell
  sudo -E env PATH=$PATH python topo/topo_dumbbell.py
    ```
- ```shell
  sudo -E env PATH=$PATH python topo/topo_parkinglot.py
    ```


## Resources
- [AlphaRTC](https://github.com/OpenNetLab/AlphaRTC)
- [Mahimahi Manual](https://manpages.debian.org/testing/mahimahi/)
