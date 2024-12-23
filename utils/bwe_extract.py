import re

def bwe_extract(logfile_path, output_file):
    assert logfile_path != None and output_file != None, "log file or output file is not specified"
    with open(logfile_path, 'r') as f:
        lines = f.readlines()
    
    bw_estimations = []

    for line in lines:
        match = re.search(r'BW-Estimation:\s*([\d\.eE\+\-]+)', line)
        if match:
            value = float(match.group(1))
            bw_estimations.append(value)
    
    with open(output_file, 'w') as out:
        for value in bw_estimations:
            out.write(f"{value}\n")
