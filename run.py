import os
import shutil
import subprocess
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Run Sender or Receiver with specific Scenario.")
parser.add_argument('--sender', action='store_true', help='Sender Flag')
parser.add_argument('--case', '-C', type=str, help='Use case', 
                    choices=['trace', 'dumbbell', 'parkinglot'], default='trace')
parser.add_argument('--index', '-I',
                    type=int, help='Index of sender and receiver', choices=[1, 2, 3])

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
    else:
        config_file = os.path.join(target_bin_dir, f"receiver_pyinfer{args.index}.json")

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
shutil.copy2(f"share/input/BandwidthEstimator.py", target_bin_dir)
shutil.copy2(f"share/input/onnx-model.onnx", target_bin_dir)

# Remove old log file if it exists
if not args.sender:
    log_file = os.path.join(output_dir, f"webrtc.log")
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
