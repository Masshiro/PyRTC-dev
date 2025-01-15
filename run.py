import os
import sys
import shutil
import subprocess
import argparse
import json

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Run Sender or Receiver with specific Scenario.")
parser.add_argument('--sender', action='store_true', help='Sender Flag')
parser.add_argument('--case', '-C', type=str, help='Use case', 
                    choices=['trace', 'dumbbell', 'parkinglot'], default='trace')
parser.add_argument('--index', '-I', default=None, 
                    type=int, help='Index of sender and receiver', choices=[1, 2, 3])
parser.add_argument('--algorithm', '-A', default="dummy", 
                    type=str, help='Bandwidth estimator', choices=["dummy", "HRCC", "GCC"])

args = parser.parse_args()

# Define target directories
target_dir = "alphartc/target"
target_lib_dir = os.path.join(target_dir, "lib")
target_bin_dir = os.path.join(target_dir, "bin")
target_pylib_dir = os.path.join(target_dir, "pylib")

# Set environment variables
os.environ["LD_LIBRARY_PATH"] = f"{target_lib_dir}:{os.environ.get('LD_LIBRARY_PATH', '')}"
os.environ["PYTHONPATH"] = f"{target_pylib_dir}:{os.environ.get('PYTHONPATH', '')}"
os.environ["PATH"] = f"{target_lib_dir}:{os.environ.get('PATH', '')}"
os.environ["PATH"] = f"{target_bin_dir}:{os.environ.get('PATH', '')}"

# Copy input files
input_dir = f"share/input/cases/{args.case}"
output_dir = f"share/output/{args.case}"

if os.path.exists(input_dir):
    for item in os.listdir(input_dir):
        src_path = os.path.join(input_dir, item)
        dst_path = os.path.join(target_bin_dir, item)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
        else:
            shutil.copy2(src_path, dst_path)

# Define executable and config file paths
executable = os.path.join(target_bin_dir, "peerconnection_serverless")
if args.sender:
    if args.case == 'trace':
        config_file = os.path.join(target_bin_dir, "sender_pyinfer.json")
    else:
        config_file = os.path.join(target_bin_dir, f"sender_pyinfer{args.index}.json")
else:
    if args.case == 'trace':
        config_file = os.path.join(target_bin_dir, "receiver_pyinfer.json")
        with open(config_file, "r", encoding="utf-8") as file:
            config_data = json.load(file)
        config_data["logging"]["log_output_path"] = f"share/output/{args.case}/webrtc_{args.algorithm}.log"
        config_data["save_to_file"]["video"]["file_path"] = f"share/output/{args.case}/outvideo_{args.algorithm}.y4m"
        with open(config_file, "w", encoding="utf-8") as file:
            json.dump(config_data, file)
    else:
        config_file = os.path.join(target_bin_dir, f"receiver_pyinfer{args.index}.json")
        with open(config_file, "r", encoding="utf-8") as file:
            config_data = json.load(file)
        config_data["logging"]["log_output_path"] = f"share/output/{args.case}/webrtc{args.index}_{args.algorithm}.log"
        config_data["save_to_file"]["video"]["file_path"] = f"share/output/{args.case}/outvideo{args.index}_{args.algorithm}.yuv"
        with open(config_file, "w", encoding="utf-8") as file:
            json.dump(config_data, file)

# if not args.sender:
if target_bin_dir not in sys.path:
        sys.path.append(target_bin_dir)
shutil.copytree(f"share/input/ccalgs/{args.algorithm}", target_bin_dir, dirs_exist_ok=True)

# Remove old log file if it exists
if not args.sender:
    if args.index == None:
        log_file = os.path.join(output_dir, f"webrtc_{args.algorithm}.log")
    else:
        log_file = os.path.join(output_dir, f"webrtc{args.index}_{args.algorithm}.log")
    if os.path.exists(log_file):
        os.remove(log_file)

# Check if executable and config file exist
if not os.path.isfile(executable):
    print(f"Error: Executable file '{executable}' not found.")
    exit(1)

if not os.path.isfile(config_file):
    print(f"Error: Configuration file '{config_file}' not found.")
    exit(1)

# Execute command
command = [executable, config_file]
print(f"Executing: {' '.join(command)}")
try:
    subprocess.run(command, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error during execution: {e}")
    exit(1)
