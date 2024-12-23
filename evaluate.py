import argparse, json

from evaluate.eval_video import VideoEvaluation, init_video_argparse, get_video_score
from evaluate.eval_network import NetworkEvaluation, init_network_argparse, get_network_score


if __name__ == "__main__":

    video_parser = init_video_argparse()
    network_parser = init_network_argparse()
    parser = argparse.ArgumentParser(parents=[video_parser, network_parser], conflict_handler='resolve')
    args = parser.parse_args([])

    args.src_video = 'share/input/testmedia/test.yuv'
    args.dst_video = 'share/output/outvideo.yuv'
    args.video_size = "320x240"
    args.pixel_format = "420"
    args.bitdepth = "8"
    args.dst_network_log = 'share/output/webrtc.log'
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
