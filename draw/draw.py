from net_info import NetInfo
from net_eval_method import net_eval_printout
from net_eval_method import NetEvalMethodExtension
from draw import draw_goodput_time
import numpy as np

import matplotlib.pyplot as plt

def draw_goodput(time_nbytes_list: list, min_gap=500, duration=60):
    for idx, time_nbytes in enumerate(time_nbytes_list):
        timestamps = list(time_nbytes.keys())
        nbytes = list(time_nbytes.values())
        # sorted_dict = dict(sorted(time_nbytes.items()))
        # timestamps = list(sorted_dict.keys())
        # nbytes = list(sorted_dict.values())
        rel_stamps = [timestamps[i]-timestamps[0] for i in range(len(timestamps))]
        goodput_list = []
        prev_time = rel_stamps[0]

        # goodput_list.append()
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
        
        plt.plot(goodput_time, goodput_list, label=algs_list[idx])
    
    # print("goodput: ", len(goodput_list))
    xticks = np.arange(0, duration*1000+1, 10000)
    xtick_labels = (xticks / 1000).astype(int)
    plt.xticks(xticks, xtick_labels)
    plt.ylabel("Goodput (Mbps)")
    plt.xlabel("Time (s)")
    plt.legend()
    plt.savefig('figure_comb.png')
    
    return timestamps, rel_stamps

if __name__ == "__main__":
    net_parser1 = NetInfo('webrtc_HRCC.log')
    net_parser2 = NetInfo('webrtc_dummy.log')
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

    time_nbytes_list = [result1[0], result2[0]]
    algs_list = ["HRCC", "dummy"]

    draw_goodput(time_nbytes_list)