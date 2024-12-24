import subprocess
import argparse, json
import time

from evaluate.eval_video import init_video_argparse, get_video_score
from evaluate.eval_network import init_network_argparse, get_network_score
from utils.bwe_extract import bwe_extract

def run_script(command):
    """run a shell script"""
    process = subprocess.Popen(command, shell=True, executable='/bin/bash')
    return process

def send_recv_process(enable_mahimahi):
    try:
        if enable_mahimahi:
            print("启动 Mahimahi 网络模拟环境...")
            mahimahi_cmd = "mm-link tracefile1 tracefile2"
            mahimahi_process = run_script(mahimahi_cmd)
            time.sleep(2)  # 确保 Mahimahi 启动完成

        print("Starting receiver...")
        receiver_cmd = ". ./run_receiver.sh"
        receiver_process = run_script(receiver_cmd)
        time.sleep(5)

        print("Starting sender...")
        sender_cmd = ". ./run_sender.sh"
        sender_process = run_script(sender_cmd)

        receiver_process.wait()
        sender_process.wait()

        if enable_mahimahi:
            mahimahi_process.terminate()
            print("已关闭 Mahimahi 模拟环境。")

    except Exception as e:
        print(f"发生错误: {e}")

def evaluate_process():
    video_parser = init_video_argparse()
    network_parser = init_network_argparse()
    parser = argparse.ArgumentParser(parents=[video_parser, network_parser], conflict_handler='resolve')
    args = parser.parse_args([])

    with open('share/input/receiver_pyinfer.json', 'r') as f:
        path_config = json.load(f)
    args.src_video = path_config['video_source']['video_file']['file_path']
    args.dst_video = path_config['save_to_file']['video']['file_path']
    args.video_size = f'{path_config["save_to_file"]["video"]["width"]}x{path_config["save_to_file"]["video"]["height"]}'
    args.pixel_format = "420"
    args.bitdepth = "8"
    args.dst_network_log = path_config['logging']['log_output_path']
    args.output = 'share/output/scores.json'

    out_dict = {}

    out_dict["video"] = get_video_score(args)
    out_dict["network"] = get_network_score(args)
    out_dict["final_score"] = 0.2 * out_dict["video"] + out_dict["network"]

    if args.output:
        with open(args.output, 'w') as f:
            f.write(json.dumps(out_dict))
    else:
        print(json.dumps(out_dict))

    bwe_extract(args.dst_network_log, 'share/output/bwe.txt')
    print(f'Evaluation is done. See share/output/scores.json and bwe.txt for the results.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Whole Workflow Controller")
    parser.add_argument("--mahimahi", action="store_true", help="Mahimahi enable flag")
    args = parser.parse_args()
    send_recv_process(enable_mahimahi=args.mahimahi)
    evaluate_process()
