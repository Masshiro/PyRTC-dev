from pathlib import Path
import json
from typing import Dict, List


current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent   # locate root directory of the project
# print("The root directory of the project is", project_root)
DEFAULT_DELAY = 0
DEFAULT_TRACE = "med_30mbps.trace"
DEFAULT_QUEUE = 1600


def load_mahimahi_settings(config_path: str) -> List[Dict]:
    with open(f'{project_root}/{config_path}', 'r') as file:
        config = json.load(file)
    return config


def generate_mahimahi_command(config_path: str) -> str:
    mahimahi_settings = load_mahimahi_settings(config_path)
    
    loss_shell = ""
    if 'loss' in mahimahi_settings and mahimahi_settings['loss'] is not None:
        if mahimahi_settings['loss']['type'] == 'down':
            loss_shell = f"mm-loss downlink {mahimahi_settings['loss']['value']} "
        else:
            loss_shell = f"mm-loss uplink {mahimahi_settings['loss']['value']} "

    delay_shell = ""
    if 'delay' in mahimahi_settings and mahimahi_settings['delay'] is not None:
        delay_shell = f"mm-delay {mahimahi_settings['delay']} "
    
    link_shell = ""
    if 'link' in mahimahi_settings and mahimahi_settings['link'] is not None:
        if isinstance(mahimahi_settings['link'], str):
            link_shell = f"mm-link {project_root}/traces/{mahimahi_settings['link']} {project_root}/traces/{mahimahi_settings['link']} "
        if isinstance(mahimahi_settings['link'], list):
            link_shell = f"mm-link {project_root}/traces/{mahimahi_settings['link'][0]} {project_root}/traces/{mahimahi_settings['link'][1]} "
    
    command = delay_shell + loss_shell + link_shell
    command = command.strip()

    return command


if __name__ == '__main__':
    command = generate_mahimahi_command('share/input/cases/trace/mahimahi.json')
    print(command)
