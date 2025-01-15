#!/usr/bin/python

from mininet.net import Containernet
from mininet.node import Controller, Docker
from mininet.link import TCLink
from mininet.cli import CLI
from time import sleep
import os
import argparse

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class DumbbellTopo:
    def __init__(self):
        self.net = Containernet(controller=Controller, link=TCLink)
        self.build()

    def build(self):
        print("=> Using dumbbell topology...")
        print("=> Creating network with Docker containers...")
        self.net.addController('c0')

        # Create switches
        switch1 = self.net.addSwitch('s1')
        switch2 = self.net.addSwitch('s2')

        # Add links between switches
        self.net.addLink(switch1, switch2, bw=10, delay='10ms', use_htb=True)
        
        # Add hosts and connect to switches
        sender1 = self.net.addDocker('h1', ip='192.168.3.101', dimage='pyrtc_image:latest', volumes=["{}/share:/app/share".format(project_root)])
        sender2 = self.net.addDocker('h2', ip='192.168.3.102', dimage='pyrtc_image:latest', volumes=["{}/share:/app/share".format(project_root)])
        receiver1 = self.net.addDocker('h3', ip='192.168.3.103', dimage='pyrtc_image:latest', volumes=["{}/share:/app/share".format(project_root)])
        receiver2 = self.net.addDocker('h4', ip='192.168.3.104', dimage='pyrtc_image:latest', volumes=["{}/share:/app/share".format(project_root)])
        
        self.net.addLink(sender1, switch1, bw=10, delay='10ms', use_htb=True)
        self.net.addLink(sender2, switch1, bw=10, delay='10ms', use_htb=True)
        self.net.addLink(receiver1, switch2, bw=10, delay='10ms', use_htb=True)
        self.net.addLink(receiver2, switch2, bw=10, delay='10ms', use_htb=True)

    def run(self, alg):
        print("=> Starting network...")
        self.net.start()

        sender1 = self.net.get('h1')
        sender2 = self.net.get('h2')
        receiver1 = self.net.get('h3')
        receiver2 = self.net.get('h4')
        
        receiver1.cmd(f"python run.py -C \"dumbbell\" -I 1 -A {alg} &") #> share/output/dumbbell/r1.log 2>&1
        receiver2.cmd(f"python run.py -C \"dumbbell\" -I 2 -A {alg} &")
        sleep(3)
        sender1.cmd(f"python run.py --sender -C \"dumbbell\" -I 1 -A {alg} &")
        sender2.cmd(f"python run.py --sender -C \"dumbbell\" -I 2 -A {alg} &")

        # receiver1_proc = receiver1.popen(f"python run.py -C dumbbell -I 1 -A {alg}")
        # receiver2_proc = receiver2.popen(f"python run.py -C dumbbell -I 2 -A {alg}")

        # sender1_proc = sender1.popen(f"python run.py --sender -C dumbbell -I 1 -A {alg}")
        # sender2_proc = sender2.popen(f"python run.py --sender -C dumbbell -I 2 -A {alg}")
        
        print("=> Transferring video & audio...")
        # sender1_proc.wait()
        # sender2_proc.wait()
        # receiver1_proc.wait()
        # receiver2_proc.wait()
        sender1.cmd('wait')
        sender2.cmd('wait')

        print("=> Transferring done. Stopping network...")
        sleep(5)
        self.net.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--algorithm', '-A', default="dummy", 
                    type=str, help='Bandwidth estimator', choices=["dummy", "HRCC", "GCC"])
    args = parser.parse_args()

    topo = DumbbellTopo()
    topo.run(args.algorithm)