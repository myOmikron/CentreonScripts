#!/usr/bin/env python3
import argparse
import subprocess
import sys


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--port", required=True, action="store", dest="port", default="22", help="SSH Port")
    parser.add_argument("-H", "--host", required=True, action="store", dest="host", help="IP or domain to connect to")

    args = parser.parse_args()

    run_list = ["ssh", "-p" + args.port, args.host,
                "sudo /opt/hp/hpssacli/bld/hpssacli ctrl slot=0 pd all show | grep physicaldrive"]
    process = subprocess.run(run_list, stdout=subprocess.PIPE)
    stdout = process.stdout.decode('utf-8')
    
    lines = stdout.split('\n')
    processed_lines = []
    for line in lines:
        processed_lines.append(line.lstrip(' '))
    
    return_code = 0
    disks_ok = []
    disks_predictive_failure = []
    disks_failed = []

    for line in processed_lines:
        if "Predictive Failure" in line and return_code <= 1:
            return_code = 1
            disks_predictive_failure.append(line)
            continue
        if ("Failed" in line or "Rebuilding" in line) and return_code <= 2:
            return_code = 2
            disks_failed.append(line)
            continue
        disks_ok.append(line)

    if return_code == 2:
        print("SERVICE STATUS: Disk Status - Critical|")
    elif return_code == 1:
        print("SERVICE STATUS: Disk Status - Warning|")
    else:
        print("SERVICE STATUS: Disk Status - OK|")

    for line in disks_failed:
        print(line)
    for line in disks_predictive_failure:
        print(line)
    for line in disks_ok:
        print(line)

    sys.exit(return_code)

