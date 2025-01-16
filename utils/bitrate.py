import subprocess
import os
import argparse

from moviepy import VideoFileClip

def calculate_bitrate_with_ffmpeg(video_path):
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    duration = float(result.stdout.strip())
    
    file_size = os.path.getsize(video_path)
    file_size_bits = file_size * 8
    bitrate = file_size_bits / duration  # bps
    bitrate_kbps = bitrate / 1000
    
    return bitrate_kbps

def calculate_bitrate(video_path):
    clip = VideoFileClip(video_path)
    duration = clip.duration
    
    file_size = os.path.getsize(video_path)
    file_size_bits = file_size * 8
    bitrate = file_size_bits / duration  # bps
    bitrate_kbps = bitrate / 1000
    
    clip.close()
    return bitrate_kbps

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-F', 
                        default="share/input/testmedia/test.y4m", type=str)
    parser.add_argument('--method', '-M', default="moviepy", choices=["moviepy", "ffmpeg"], type=str)
    args = parser.parse_args()

    if args.method == "ffmpeg":
        bitrate = calculate_bitrate_with_ffmpeg(args.file)
    else:
        bitrate = calculate_bitrate(args.file)

    print(f"Video's bitrate: {bitrate:.2f} kbps")
