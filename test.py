import json

with open('share/input/receiver_pyinfer.json', 'r') as f:
    path_config = json.load(f)

print(path_config['video_source']['video_file']['file_path'])
print(path_config['save_to_file']['video']['file_path'])
print(f'{path_config['save_to_file']['video']['width']}x{path_config['save_to_file']['video']['height']}')
print(path_config['logging']['log_output_path'])