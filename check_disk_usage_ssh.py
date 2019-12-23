#!/usr/bin/env python3
import argparse
import re
import subprocess
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--hostname", action="store", dest="hostname", help="Hostname of the system you want to query")
    parser.add_argument("--ssh-option", action="append", nargs="*", dest="ssh_options", help="SSH Options, like '-l=centreon-engine'")
    parser.add_argument("--warning-usage-prct", action="store", dest="warning_usage_prct", type=int, help="Warning threshold for usage in percent")
    parser.add_argument("--critical-usage-prct", action="store", dest="critical_usage_prct", type=int,  help="Critical threshold for usage in percent")

    args = parser.parse_args()

    cmd = 'df -h'
    run_list = ["ssh"]

    if args.ssh_options:
        for item in args.ssh_options:
            option = item[0]
            if option.startswith("'"):
                option = option[1:]
            if option.endswith("'"):
                option = option[:-1]
            options = re.split("=", option)
            for opt in options:
                run_list.append(opt)
    run_list.append(args.hostname)
    run_list.append(cmd)
    try:
        ret = subprocess.run(run_list, stdout=subprocess.PIPE)
    except:
        print("SERVICE STATE: UNKOWN - Error in SSH connection")
        sys.exit(3)

    disk_data = []
    for line in ret.stdout.decode('utf-8').splitlines()[1:]:
        disk_data.append([x for x in line.split(" ") if x])

    if len(disk_data) == 0:
        print("SERVICE STATE: UNKNOWN - No disks found")
        sys.exit(3)

    return_code = 0

    perf_data = []
    warning_count = 0
    critical_count = 0

    for line in disk_data:
        if args.warning_usage_prct:
            if int(re.sub("%", "", line[4])) > args.warning_usage_prct:
                return_code = 1 if return_code < 1 else return_code
                warning_count += 1
        if args.critical_usage_prct:
            if int(re.sub("%", "", line[4])) > args.critical_usage_prct:
                return_code = 2 if return_code < 2 else return_code
                critical_count += 1

        perf_data.append(line[0] + "=" + re.sub("%", "", line[4]) + "[%];" +
                         (str(args.warning_usage_prct) if args.warning_usage_prct else "") + ";" +
                         (str(args.critical_usage_prct) if args.critical_usage_prct else "") + ";" +
                         "0;100")
    if return_code == 0:
        print("SERVICE STATUS: OK - All partitions are okay|")
    elif return_code == 1:
        print("SERVICE STATUS: WARNING -", str(warning_count), "partitions are in warning state")
    elif return_code == 2:
        print("SERVICE STATUS: CRITICAL -", str(critical_count), "partitions are in critical state")
    print("|")
    for line in perf_data:
        print(line)

    sys.exit(return_code)

