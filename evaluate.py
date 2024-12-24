import argparse, json

from evaluate.eval_video import VideoEvaluation, init_video_argparse, get_video_score
from evaluate.eval_network import NetworkEvaluation, init_network_argparse, get_network_score
from utils.bwe_extract import bwe_extract


if __name__ == "__main__":

    video_parser = init_video_argparse()
    network_parser = init_network_argparse()
    parser = argparse.ArgumentParser(parents=[video_parser, network_parser], conflict_handler='resolve')
    args = parser.parse_args([])

    with open('share/input/receiver_pyinfer.json', 'r') as f:
        path_config = json.load(f)
    args.src_video = path_config['video_source']['video_file']['file_path']
    args.dst_video = path_config['save_to_file']['video']['file_path']
    args.video_size = f'{path_config['save_to_file']['video']['width']}x{path_config['save_to_file']['video']['height']}'
    args.pixel_format = "420"
    args.bitdepth = "8"
    args.dst_network_log = path_config['logging']['log_output_path']
    args.output = 'share/output/scores.json'

    # print(args)

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
