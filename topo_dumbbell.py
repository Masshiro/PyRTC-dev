from mininet.net import Containernet
from mininet.node import Controller, Docker
from mininet.link import TCLink
from mininet.cli import CLI
from time import sleep

class DumbbellTopo:
    def __init__(self):
        self.net = Containernet(controller=Controller, link=TCLink)
        self.build()

    def build(self):
        print("Creating network with Docker containers...")
        self.net.addController('c0')
        switch1 = self.net.addSwitch('s1')
        switch2 = self.net.addSwitch('s2')
        self.net.addLink(switch1, switch2, bw=50, delay='10ms', loss=0, max_queue_size=100)
        sender1 = self.net.addDocker('h1', ip='192.168.2.111', dimage='pyrtc_image:latest', network_mode='rtcnet')
        sender2 = self.net.addDocker('h2', ip='192.168.2.112', dimage='pyrtc_image:latest', network_mode='rtcnet')
        receiver1 = self.net.addDocker('h3', ip='192.168.2.113', dimage='pyrtc_image:latest', network_mode='rtcnet')
        receiver2 = self.net.addDocker('h4', ip='192.168.2.114', dimage='pyrtc_image:latest', network_mode='rtcnet')
        self.net.addLink(sender1, switch1, bw=50, delay='10ms')
        self.net.addLink(sender2, switch1, bw=50, delay='10ms')
        self.net.addLink(receiver1, switch2, bw=50, delay='10ms')
        self.net.addLink(receiver2, switch2, bw=50, delay='10ms')

    def run(self):
        print("Starting network...")
        self.net.start()
        receiver1 = self.net.get('h3')
        receiver2 = self.net.get('h4')
        receiver1.cmd('python run.py &')
        receiver2.cmd('python run.py &')
        sleep(3)
        sender1 = self.net.get('h1')
        sender2 = self.net.get('h2')
        sender1.cmd('python run.py --sender &')
        sender2.cmd('python run.py --sender &')
        CLI(self.net)
        print("Stopping network...")
        self.net.stop()

if __name__ == '__main__':
    topo = DumbbellTopo()
    topo.run()
