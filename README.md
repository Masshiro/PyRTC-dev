# PyRTC-dev

## Prerequisites

To fully utilize this repository, make sure that **<u>Ubuntu 20.04</u>** is using and following tools are installed.

- Docker Engine: [official installation guide](https://docs.docker.com/engine/install/)
- Docker Compose: [official installation guide](https://docs.docker.com/compose/install/)
- Containernet: [official installation guide](https://github.com/containernet/containernet?tab=readme-ov-file#installation)
- Mahimahi: [official installation guide](http://mahimahi.mit.edu/#getting)

The more detailed installation steps could be found at [Installation Guide](#installation-guide).

## Usage

### Get things ready

Firstly, you may want to clone this repo and initialize the submodule [AlphaRTC](https://github.com/OpenNetLab/AlphaRTC):
```shell
git clone --recurse-submodules https://github.com/Masshiro/PyRTC-dev.git
```
or update the cloned repo using
```shell
git submodule update --init --recursive
```

To build AlphaRTC and make it function, you may need to get [`depot_tools`](https://commondatastorage.googleapis.com/chrome-infra-docs/flat/depot_tools/docs/html/depot_tools_tutorial.html#_setting_up):

```shell
git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
# Add depot_tools to the front of your PATH
export PATH=/path/to/depot_tools:$PATH
```

After doing that, use the build script at the root directory of this repository. Note that `pkg-config` and `ninja-build` should be installed to ensure the building process go smoothly:

```shell
sudo ln -s $(which python3) /usr/bin/python
. build.sh
```

Then you can create docker image named `pyrtc_image:latest` by default along with the docker network which would be used in following trace-driven simulation and named `rtcnet` by default:

```shell
make setup
```

- or you can create image or network separately by using either `make build` or `make network`.

For the test media, choose one and download from [this site](https://media.xiph.org/video/derf/), then name the file as test.y4m and move into `share/input/testmedia`

### Demonstration

To quickly demonstrate the functionality of trace-driven simulation, run:

```shell
python demo.py
```

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

## Installation Guide

**Docker:** (more explanation at [here](https://docs.docker.com/engine/install/ubuntu/))

```shell
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Manage Docker as non-root user:
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```

**Docker Compose Plugin**: (more explanation at [here]())

```shell
sudo apt-get update
sudo apt-get install docker-compose-plugin
```

**Containernet**: (more explanation at [here](https://github.com/containernet/containernet?tab=readme-ov-file#installation))

```shell
sudo apt-get install ansible
git clone https://github.com/containernet/containernet.git
sudo ansible-playbook -i "localhost," -c local containernet/ansible/install.yml
python3 -m venv venv
source venv/bin/activate
pip install .
```

**Mahimahi**: (more explanation at [here](http://mahimahi.mit.edu/#getting))

```shell
# If Ubuntu 20.04 is used
sudo apt-get install mahimahi

# Otherwise
git clone https://github.com/ravinet/mahimahi
cd mahimahi
./autogen.sh
./configure
make
sudo make install
```

To prevent unexpected changes to AlphaRTC source, you may want to run:

```shell
git config submodule.alphartc.ignore all
git update-index --assume-unchanged .gclient_previous_sync_commits
```



## Resources

- [AlphaRTC](https://github.com/OpenNetLab/AlphaRTC)
- [Mahimahi Manual](https://manpages.debian.org/testing/mahimahi/)
