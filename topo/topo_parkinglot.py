#!/usr/bin/python

from mininet.net import Containernet
from mininet.node import Controller, Docker
from mininet.link import TCLink
from mininet.cli import CLI
from time import sleep
import os
import argparse

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class ParkinglotTopo:
    def __init__(self):
        self.net = Containernet(controller=Controller, link=TCLink)
        self.build()

    def build(self):
        print("=> Using parking-lot topology...")
        print("=> Creating network with Docker containers...")
        self.net.addController('c0')

        # Create switches
        switch1 = self.net.addSwitch('s1')
        switch2 = self.net.addSwitch('s2')
        switch3 = self.net.addSwitch('s3')

        # Add links between switches
        self.net.addLink(switch1, switch2, bw=10, delay='10ms', loss=0, use_htb=True)
        self.net.addLink(switch2, switch3, bw=10, delay='10ms', loss=0, use_htb=True)

        # Add hosts and connect to switches
        sender1 = self.net.addDocker('h1', ip='192.168.4.101', dimage='pyrtc_image:latest', volumes=["{}/share:/app/share".format(project_root)])
        sender2 = self.net.addDocker('h2', ip='192.168.4.102', dimage='pyrtc_image:latest', volumes=["{}/share:/app/share".format(project_root)])
        sender3 = self.net.addDocker('h4', ip='192.168.4.104', dimage='pyrtc_image:latest', volumes=["{}/share:/app/share".format(project_root)])
        receiver1 = self.net.addDocker('h6', ip='192.168.4.106', dimage='pyrtc_image:latest', volumes=["{}/share:/app/share".format(project_root)])
        receiver2 = self.net.addDocker('h3', ip='192.168.4.103', dimage='pyrtc_image:latest', volumes=["{}/share:/app/share".format(project_root)])
        receiver3 = self.net.addDocker('h5', ip='192.168.4.105', dimage='pyrtc_image:latest', volumes=["{}/share:/app/share".format(project_root)])

        self.net.addLink(sender1, switch1, bw=10, delay='5ms', use_htb=True)
        self.net.addLink(sender2, switch1, bw=10, delay='10ms', use_htb=True)
        self.net.addLink(sender3, switch2, bw=10, delay='5ms', use_htb=True)
        self.net.addLink(receiver1, switch3, bw=10, delay='10ms', use_htb=True)
        self.net.addLink(receiver2, switch2, bw=10, delay='10ms', use_htb=True)
        self.net.addLink(receiver3, switch3, bw=10, delay='10ms', use_htb=True)
        

    def run(self, alg):
        print("=> Starting network...")
        self.net.start()

        sender1 = self.net.get('h1')
        sender2 = self.net.get('h2')
        sender3 = self.net.get('h4')
        receiver1 = self.net.get('h6')
        receiver2 = self.net.get('h3')
        receiver3 = self.net.get('h5')
        
        receiver1.cmd(f'python run.py -C "parkinglot" -I 1 -A {alg} &')
        receiver2.cmd(f'python run.py -C "parkinglot" -I 2 -A {alg} &')
        receiver3.cmd(f'python run.py -C "parkinglot" -I 3 -A {alg} &')
        sleep(5)
        sender1.cmd(f'python run.py --sender -C "parkinglot" -I 1 -A {alg} &')
        sender2.cmd(f'python run.py --sender -C "parkinglot" -I 2 -A {alg} &')
        sender3.cmd(f'python run.py --sender -C "parkinglot" -I 3 -A {alg} &')

        print("=> Transferring video & audio...")
        sender1.cmd('wait')
        sender2.cmd('wait')
        sender3.cmd('wait')

        print("=> Transferring done. Stopping network...")
        self.net.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--algorithm', '-A', default="dummy", 
                    type=str, help='Bandwidth estimator', choices=["dummy", "HRCC", "GCC"])
    args = parser.parse_args()

    topo = ParkinglotTopo()
    topo.run(args.algorithm)