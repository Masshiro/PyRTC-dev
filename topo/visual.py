import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

import matplotlib.pyplot as plt

from utils.ssim import calculate_video_ssim
from utils.draw import draw_goodput
from evaluate.utils.net_info import NetInfo
from evaluate.utils.net_eval_method import NetEvalMethodExtension
from evaluate.eval_network import init_network_argparse, get_network_score


def network_score(index:int, algorithm: str, topo: str):
    network_parser = init_network_argparse()
    network_args = network_parser.parse_args()
    network_args.dst_network_log = f"share/output/{topo}/webrtc{index}_{algorithm}.log"
    return get_network_score(network_args)

def visual_one_topo(max_index:int, topo: str):
    for algorithm in ["dummy", "HRCC", "GCC"]:
        net_parsers = []
        results = []
        net_eval_extension = NetEvalMethodExtension()
        for i in range(1, max_index+1):
            net_parsers.append(NetInfo(f"share/output/{topo}/webrtc{i}_{algorithm}.log"))
            net_parsers[i-1].parse_net_log()
            results.append(net_eval_extension.eval(net_parsers[i-1]))
        draw_goodput([r[0] for r in results], [f"Flow {i}" for i in range(1, max_index+1)], f"goodput_time_{topo}_{algorithm}", min_gap=200, duration=20)
    
    

if __name__ == "__main__":
    visual_one_topo(2, "dumbbell")
    visual_one_topo(3, "parkinglot")