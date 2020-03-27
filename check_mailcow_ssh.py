#!/usr/bin/env python3

import argparse
from subprocess import Popen, PIPE


def check_for_updates(args):
    cmd = "cd /opt/mailcow-dockerized/ && sudo ./update.sh --check"
    stream = Popen(['ssh', args.user_name + "@" + args.host_name, "-p " + args.port, cmd], stdout=PIPE)
    out = stream.stdout.read().decode('utf-8')
    print(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--hostname", action="store", dest="host_name", help="Name of the host to connect to")
    parser.add_argument("-u", "--username", action="store", dest="user_name", help="Name of the user to connect with")
    parser.add_argument("-p", "--port", action="store", dest="port", help="Port to connect to")
    args = parser.parse_args()

    if not args.user_name:
        args.user_name = "centreon-engine"
    if not args.port:
        args.port = "22"

    check_for_updates(args)


if __name__ == '__main__':
    main()
