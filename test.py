import json

from utils.mahi_helpers import generate_mahimahi_command

# with open('share/input/receiver_pyinfer.json', 'r') as f:
#     path_config = json.load(f)

# print(path_config['video_source']['video_file']['file_path'])
# print(path_config['save_to_file']['video']['file_path'])
# print(f'{path_config['save_to_file']['video']['width']}x{path_config['save_to_file']['video']['height']}')
# print(path_config['logging']['log_output_path'])


import subprocess
# receiver_cmd = "mm-delay 20 mm-link /home/quanwei/Projects/PyRTC-dev/traces/ATT-LTE-driving.up /home/quanwei/Projects/PyRTC-dev/traces/ATT-LTE-driving.up --downlink-queue=droptail --downlink-queue-args=bytes=1600 -- bash -c '. ./run_receiver.sh'"

mahi_cmd = generate_mahimahi_command('share/input/mahimahi.json')
# receiver_cmd = f"{mahi_cmd} -- bash -c '. ./run_receiver.sh'"
receiver_cmd = f"{mahi_cmd} -- bash -c 'ip addr show'"

# receiver_cmd = ". ./run_receiver.sh"

result = subprocess.Popen(receiver_cmd, shell=True, executable='/bin/bash')

# print("STDOUT:", result.stdout)
# print("STDERR:", result.stderr)
