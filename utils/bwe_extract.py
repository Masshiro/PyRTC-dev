import re

def bwe_extract(logfile_path, output_file):
    assert logfile_path != None and output_file != None, "log file or output file is not specified"
    with open(logfile_path, 'r') as f:
        lines = f.readlines()
    
    bw_estimations = []

    for line in lines:
        match = re.search(r'Send back BWE estimation:\s*([\d\.eE\+\-]+)\s*at time:\s*(\d+)', line)
        if match:
            value = float(match.group(1))
            timestamp = int(match.group(2))
            bw_estimations.append((value, timestamp))

    
    with open(output_file, 'w') as out:
        for entry in bw_estimations:
            out.write(f"{entry[0]} {entry[1]}\n")
