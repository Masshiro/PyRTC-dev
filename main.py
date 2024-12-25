import subprocess
import argparse, json
import time
import os

from evaluate.eval_video import init_video_argparse, get_video_score
from evaluate.eval_network import init_network_argparse, get_network_score
from utils.bwe_extract import bwe_extract
from utils.mahi_helpers import generate_mahimahi_command, config_mahimahi_ip

def run_script(command):
    """run a shell script"""
    process = subprocess.Popen(command, shell=True, executable='/bin/bash')
    return process

def build_process():
    try:
        print("Building AlphaRTC...")
        build_cmd = ". ./build.sh"
        build_process = run_script(build_cmd)
        build_process.wait()
        print("AlphaRTC is built successfully.")
    except Exception as e:
        print(f"Error: {e}")

def send_recv_process(enable_mahimahi, mahi_config):
    try:
        if enable_mahimahi:
            print("Starting receiver with Mahimahi enabled...")
            mahi_cmd = generate_mahimahi_command(mahi_config)
            # mahimahi_base = os.getenv("MAHIMAHI_BASE", "0.0.0.0")
            # config_mahimahi_ip("$MAHIMAHI_BASE")
            receiver_cmd = f"{mahi_cmd} -- bash -c '. ./run_receiver.sh'"
            receiver_process = run_script(receiver_cmd)
            time.sleep(5)
        else:
            print("Starting receiver...")
            receiver_cmd = ". ./run_receiver.sh"
            receiver_process = run_script(receiver_cmd)
            time.sleep(5)

        print("Starting sender...")
        sender_cmd = ". ./run_sender.sh"
        sender_process = run_script(sender_cmd)

        receiver_process.wait()
        sender_process.wait()

        # if enable_mahimahi:
        #     mahimahi_process.terminate()
        #     print("Mahimahi simulated links are terminated.")

    except Exception as e:
        print(f"Error: {e}")

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
    parser.add_argument("--build", action="store_true", help="AlphaRTC build flag")
    parser.add_argument("--mahimahi", action="store_true", help="Mahimahi enable flag")
    parser.add_argument("--mahi_config", type=str, help="Mahimahi config file path")
    args = parser.parse_args()
    if args.mahimahi and not args.mahi_config:
        raise ValueError("Mahimahi config file path is required when Mahimahi is enabled.")

    if args.build:
        build_process()
    send_recv_process(enable_mahimahi=args.mahimahi, mahi_config=args.mahi_config)
    evaluate_process()
