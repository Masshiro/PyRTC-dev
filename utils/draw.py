import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from evaluate.eval_video import init_video_argparse, get_video_score
from evaluate.eval_network import init_network_argparse, get_network_score
from utils.ssim import calculate_video_ssim

import numpy as np
import matplotlib.pyplot as plt
import argparse
import json
from itertools import cycle

def draw_goodput(time_nbytes_list: list, label_list: list, save_file_name="goodput", min_gap=500, duration=60):
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
        
        plt.plot(goodput_time, goodput_list,  label=label_list[idx])
    
    xticks = np.arange(0, duration*1000+1, 10000)
    xtick_labels = (xticks / 1000).astype(int)
    plt.xticks(xticks, xtick_labels)
    plt.ylabel("Goodput (Mbps)", fontsize=20)
    plt.xlabel("Time (s)", fontsize=20)
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.savefig(f"share/output/figures/{save_file_name}.pdf", format='pdf', bbox_inches='tight')
    
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
    labels = ['dummy', 'HRCC']
    plt.bar(labels, scores, alpha=0.9, width=0.35, facecolor='lightskyblue', edgecolor='white', label='one', lw=1)

    plt.xlabel("Algorithm")
    plt.ylabel("Score")
    plt.savefig(f"share/output/figures/{save_file_name}", bbox_inches='tight')

def draw_metrics_from_json_traces(json_file, algorithm_name, metric_x, metric_y, xy_labels:tuple):
    with open(json_file, 'r') as file:
        data = json.load(file)

    metrics = []
    traces = []
    for trace_name, trace_data in data.items():
        if algorithm_name in trace_data:
            algo_data = trace_data[algorithm_name]
            if metric_x in algo_data and metric_y in algo_data:
                avg_x = sum(algo_data[metric_x]) / len(algo_data[metric_x])
                avg_y = sum(algo_data[metric_y]) / len(algo_data[metric_y])
                metrics.append((avg_x, avg_y, trace_name))

    metrics.sort(reverse=True, key=lambda x: x[0])
    x_values = [item[0] for item in metrics]
    y_values = [item[1] for item in metrics]
    traces = [item[2] for item in metrics]

    markers = cycle(['o', 's', 'D', '^', 'v', '*', 'P', 'X'])
    colors = cycle(plt.cm.tab10(np.linspace(0, 1, len(traces))))

    plt.figure(figsize=(10, 7))
    for i, (x, y, trace) in enumerate(zip(x_values, y_values, traces)):
        marker = next(markers)
        color = next(colors)
        plt.scatter(x, y, label=trace, marker=marker, color=color, s=200)
        # plt.text(x, y, trace, fontsize=9, ha='right')

    plt.gca().invert_xaxis()
    plt.xlabel(xy_labels[0], fontsize=20)
    plt.ylabel(xy_labels[1], fontsize=20)
    plt.grid(True)
    plt.legend(title="Traces", loc='upper left', fontsize=20, title_fontsize=22)
    # plt.show()


    plt.savefig(f"share/output/figures/{algorithm_name}_{metric_x}_{metric_y}.pdf", bbox_inches='tight', format='pdf')

def draw_combined_scores_from_json_traces(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    traces = list(data.keys())
    algorithms = ['dummy', 'HRCC', 'GCC']
    labels = ['Dummy', 'HRCC', 'GCC']
    bar_width = 0.2

    heights = {algo: [] for algo in algorithms}
    for trace_name in traces:
        for algo in algorithms:
            if algo in data[trace_name]:
                algo_data = data[trace_name][algo]
                avg_ssim = sum(algo_data['SSIM']) / len(algo_data['SSIM'])
                avg_network_score = sum(algo_data['network score']) / len(algo_data['network score'])
                heights[algo].append(avg_ssim * 50 + avg_network_score)

    x = np.arange(len(traces))
    plt.figure(figsize=(12, 6))

    for i, (algo, label) in enumerate(zip(algorithms, labels)):
        plt.bar(x + i * (bar_width), heights[algo], width=bar_width, label=label)

    plt.xticks(x + bar_width, traces)
    plt.xlabel('Trace')
    plt.ylabel('Combined Score')
    plt.ylim(0, 100)
    plt.legend(title="Algorithm", loc="upper right", fontsize=20)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.savefig(f"share/output/figures/trace_scores.pdf", bbox_inches='tight', format='pdf')


if __name__ == "__main__":
    ########################################################

    # net_parser1 = NetInfo('share/output/trace/webrtc_HRCC.log')
    # net_parser2 = NetInfo('share/output/trace/webrtc_dummy.log')
    # parse_result1 = net_parser1.parse_net_log()
    # parse_result2 = net_parser2.parse_net_log()

    # net_eval_extension = NetEvalMethodExtension()
    # result1 = net_eval_extension.eval(net_parser1)
    # result2 = net_eval_extension.eval(net_parser2)
    # print(f'self inflicted delay: ', result1[1])
    # print(f'95 quantile one-way delay: ', result1[2])
    # print(f'good put: ', result1[3])
    # print(f'loss rate: ', result1[4])
    # print('*'*30)
    # print(f'self inflicted delay: ', result2[1])
    # print(f'95 quantile one-way delay: ', result2[2])
    # print(f'good put: ', result2[3])
    # print(f'loss rate: ', result2[4])

    # draw_goodput([result1[0], result2[0]], ["HRCC", "dummy"], "hrcc_dummy_put_taxi.png")

    ########################################################

    # draw_score("trace", "score_trace_taxi.png")

    ########################################################

    # draw_metrics_from_json("share/output/trace/demo_results.json", "HRCC", "delay1", "goodput", ("Self-inflicted delay (ms)", "Goodput (Mbps)"))

    # for alg in ["dummy", "HRCC", "GCC"]:
    #     draw_metrics_from_json_traces("share/output/trace/demo_results.json", alg, "delay1", "goodput", ("Self-Inflicted Delay (ms)", "Average Goodput (Mbps)"))
    #     draw_metrics_from_json_traces("share/output/trace/demo_results.json", alg, "delay2", "goodput", ("95th Percentile One-Way Delay (ms)", "Average Goodput (Mbps)"))

    draw_combined_scores_from_json_traces("share/output/trace/demo_results.json")