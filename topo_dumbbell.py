#!/usr/bin/python

from mininet.net import Containernet
from mininet.node import Controller, Docker
from mininet.link import TCLink
from mininet.cli import CLI
from time import sleep

# class DumbbellTopo:
#     def __init__(self):
#         self.net = Containernet(controller=Controller, link=TCLink)
#         self.build()

#     def build(self):
#         print("Creating network with Docker containers...")
#         self.net.addController('c0')
#         switch1 = self.net.addSwitch('s1')
#         switch2 = self.net.addSwitch('s2')
#         self.net.addLink(switch1, switch2, bw=10, delay='10ms', use_htb=False)
#         sender1 = self.net.addDocker('h1', ip='192.168.3.111', dimage='pyrtc_image:latest')
#         sender2 = self.net.addDocker('h2', ip='192.168.3.112', dimage='pyrtc_image:latest')
#         receiver1 = self.net.addDocker('h3', ip='192.168.3.113', dimage='pyrtc_image:latest')
#         receiver2 = self.net.addDocker('h4', ip='192.168.3.114', dimage='pyrtc_image:latest')
#         self.net.addLink(sender1, switch1, bw=10, delay='10ms', use_htb=False)
#         self.net.addLink(sender2, switch1, bw=10, delay='10ms', use_htb=False)
#         self.net.addLink(receiver1, switch2, bw=10, delay='10ms', use_htb=False)
#         self.net.addLink(receiver2, switch2, bw=10, delay='10ms', use_htb=False)

#     def run(self):
#         print("Starting network...")
#         self.net.start()
#         receiver1 = self.net.get('h3')
#         receiver2 = self.net.get('h4')
#         receiver1.cmd('python run.py -C "dumbbell" -I 1 &')
#         receiver2.cmd('python run.py -C "dumbbell" -I 2 &')
#         sleep(3)
#         sender1 = self.net.get('h1')
#         sender2 = self.net.get('h2')
#         sender1.cmd('python run.py --sender -C "dumbbell" -I 1 &')
#         sender2.cmd('python run.py --sender -C "dumbbell" -I 2 &')
#         CLI(self.net)
#         print("Stopping network...")
#         self.net.stop()

# if __name__ == '__main__':
#     topo = DumbbellTopo()
#     topo.run()


net = Containernet(controller=Controller, link=TCLink)
print("Creating network with Docker containers...")
net.addController('c0')
switch1 = net.addSwitch('s1')
switch2 = net.addSwitch('s2')
net.addLink(switch1, switch2, bw=10, delay='10ms')
sender1 = net.addDocker('h1', ip='192.168.2.111', dimage='pyrtc_image:latest', privileged=True)
sender2 = net.addDocker('h2', ip='192.168.2.112', dimage='pyrtc_image:latest', privileged=True)
receiver1 = net.addDocker('h3', ip='192.168.2.113', dimage='pyrtc_image:latest', privileged=True)
receiver2 = net.addDocker('h4', ip='192.168.2.114', dimage='pyrtc_image:latest', privileged=True)
net.addLink(sender1, switch1, bw=10, delay='10ms')
net.addLink(sender2, switch1, bw=10, delay='10ms')
net.addLink(receiver1, switch2, bw=10, delay='10ms')
net.addLink(receiver2, switch2, bw=10, delay='10ms')

net.start()
CLI(net)
net.stop()