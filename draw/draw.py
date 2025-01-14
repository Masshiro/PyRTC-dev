import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from evaluate.utils.net_info import NetInfo
from evaluate.utils.net_eval_method import NetEvalMethodExtension

from evaluate.eval_video import init_video_argparse, get_video_score
from evaluate.eval_network import init_network_argparse, get_network_score

from utils.ssim import calculate_video_ssim

import numpy as np
import matplotlib.pyplot as plt
import argparse
import json

def draw_goodput(time_nbytes_list: list, algs_list: list, save_file_name="hrcc_dummy_put.png", min_gap=500, duration=60):
    plt.figure()
    for idx, time_nbytes in enumerate(time_nbytes_list):
        timestamps = list(time_nbytes.keys())
        nbytes = list(time_nbytes.values())
        rel_stamps = [timestamps[i]-timestamps[0] for i in range(len(timestamps))]
        goodput_list = []
        prev_time = rel_stamps[0]

        goodput_gap = nbytes[1]
        goodput_time = []
        for i in range(1, len(time_nbytes)):
            if rel_stamps[i] - prev_time < min_gap:
                goodput_gap += nbytes[i]
                continue
            else:
                goodput_list.append((goodput_gap * 8. /1000.) / (rel_stamps[i] - prev_time) )
                goodput_time.append(rel_stamps[i])
                prev_time = rel_stamps[i]
                goodput_gap = 0
        
        plt.plot(goodput_time, goodput_list,  label=algs_list[idx])
    
    xticks = np.arange(0, duration*1000+1, 10000)
    xtick_labels = (xticks / 1000).astype(int)
    plt.xticks(xticks, xtick_labels)
    plt.ylabel("Goodput (Mbps)")
    plt.xlabel("Time (s)")
    plt.legend(loc='upper left')
    plt.savefig(f"share/output/figures/{save_file_name}", bbox_inches='tight')
    
    return timestamps, rel_stamps

def draw_score(case_name, save_file_name="score.png"):
    scores = []
    for alg_name in ["dummy", "HRCC"]:
        video_parser = init_video_argparse()
        network_parser = init_network_argparse()
        parser = argparse.ArgumentParser(parents=[video_parser, network_parser], conflict_handler='resolve')
        args = parser.parse_args([])

        args.src_video = "share/input/testmedia/test.y4m"
        args.dst_video = f"share/output/{case_name}/outvideo_{alg_name}.y4m"
        # args.frame_align_method = "ocr"
        # args.output = f"share/output/{case_name}/scores_{alg_name}.json"
        # args.video_size = "1280x720"
        # args.pixel_format = "420"
        # args.bitdepth = "8"
        args.dst_network_log = f"share/output/{case_name}/webrtc_{alg_name}.log"
        # video_score = get_video_score(args)
        video_score = calculate_video_ssim(args.src_video, args.dst_video)
        network_score = get_network_score(args)
        print(f'video score: {video_score}, network score: {network_score}')
        final_score = 50 * video_score + network_score
        scores.append(final_score)
    
    plt.figure()
    labels = ['dummy', 'HRCC']  # 横坐标标签
    plt.bar(labels, scores, alpha=0.9, width=0.35, facecolor='lightskyblue', edgecolor='white', label='one', lw=1)

    plt.xlabel("Algorithm")
    plt.ylabel("Score")
    plt.savefig(f"share/output/figures/{save_file_name}", bbox_inches='tight')


if __name__ == "__main__":
    ########################################################

    net_parser1 = NetInfo('share/output/trace/webrtc_HRCC.log')
    net_parser2 = NetInfo('share/output/trace/webrtc_dummy.log')
    parse_result1 = net_parser1.parse_net_log()
    parse_result2 = net_parser2.parse_net_log()

    net_eval_extension = NetEvalMethodExtension()
    result1 = net_eval_extension.eval(net_parser1)
    result2 = net_eval_extension.eval(net_parser2)
    print(f'self inflicted delay: ', result1[1])
    print(f'95 quantile one-way delay: ', result1[2])
    print(f'good put: ', result1[3])
    print(f'loss rate: ', result1[4])
    print('*'*30)
    print(f'self inflicted delay: ', result2[1])
    print(f'95 quantile one-way delay: ', result2[2])
    print(f'good put: ', result2[3])
    print(f'loss rate: ', result2[4])

    draw_goodput([result1[0], result2[0]], ["HRCC", "dummy"], "hrcc_dummy_put_taxi.png")

    ########################################################

    draw_score("trace", "score_trace_taxi.png")