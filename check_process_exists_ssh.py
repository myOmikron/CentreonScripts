#!/usr/bin/env python3

import argparse
import sys
from subprocess import PIPE, Popen

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--hostname", action="store", dest="host_name", help="Name of the host to connect to")
    parser.add_argument("-u", "--username", action="store", dest="user_name", help="Name of the user to connect with")
    parser.add_argument("-p", "--port", action="store", dest="port", help="Port to connect to")
    parser.add_argument("-P", "--process", action="store", dest="process", help="Process to search")
    args = parser.parse_args()

    cmd = "pgrep " + args.process
    if not args.user_name:
        args.user_name = "centreon-engine"
    if not args.port:
        args.port = "22"
    stream = Popen(['ssh', args.user_name + "@" + args.host_name, "-p " + args.port, cmd],
                   stdout=PIPE)
    out = stream.stdout.read().decode('utf-8')
    if len(out.splitlines()) > 0:
        print("SERVICE STATUS: OK - Process is running")
        sys.exit(0)
    else:
        print("SERVICE STATUS: CRITICAL - Process not found")
        sys.exit(2)
