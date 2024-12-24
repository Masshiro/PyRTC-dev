from pathlib import Path
import json
from typing import Dict, List


current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent   # locate root directory of the project
# print("The root directory of the project is", project_root)
DEFAULT_DELAY = 0
DEFAULT_TRACE = f'{project_root}/traces/med_30mbps.trace'
DEFAULT_QUEUE = 1600


def load_mahimahi_settings(config_path: str) -> List[Dict]:
    with open(f'{project_root}/{config_path}', 'r') as file:
        config = json.load(file)
    return config


def generate_mahimahi_command(config_path: str) -> str:
    mahimahi_settings = load_mahimahi_settings(config_path)
    
    loss_directive = ""
    if 'loss' in mahimahi_settings and mahimahi_settings['loss'] is not None:
        loss_directive = f"mm-loss downlink {mahimahi_settings['loss']}"

    delay = mahimahi_settings.get('delay', DEFAULT_DELAY)
    trace_file = mahimahi_settings.get('trace_file', DEFAULT_TRACE)
    queue_size = mahimahi_settings.get('queue_size', DEFAULT_QUEUE)

    command = f"mm-delay {delay} {loss_directive}".strip()
    command += f" mm-link traces/{trace_file} traces/{trace_file} --downlink-queue=droptail --downlink-queue-args=bytes={queue_size}"

    return command


if __name__ == '__main__':
    command = generate_mahimahi_command('share/input/mahimahi.json')
    print(command)
