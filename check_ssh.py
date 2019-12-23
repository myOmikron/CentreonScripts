#!/usr/bin/env python3

import argparse
import subprocess
import sys
import re


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--hostname", action="store", required=True, dest="host_name", help="Name of the host to connect to")
    parser.add_argument("--ssh-option", action="append", nargs="*", dest="ssh_options", help="SSH options to specify behaviour")
    parser.add_argument("--send-command", action="store", dest="send_command", type=int, help="Specify False, if you don't want to send a command")
    args = parser.parse_args()
        
    if args.send_command is None:
        args.send_command = 1
    if args.send_command != 0 and args.send_command != 1:
        args.send_command = 1

    run_list = ["ssh", args.host_name]
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
    if args.send_command == 1:
        run_list.append("whoami")
    try:
        ret = subprocess.run(run_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        print("SERVICE STATUS: CRITICAL - SSH Server not reachable")
        sys.exit(2)
    if ret.returncode == 0:
        print("SERVICE STATUS: OK - SSH Login successful")
        sys.exit(0)
    print("SERVICE STATUS: UNKNOWN")
    sys.exit(3)
