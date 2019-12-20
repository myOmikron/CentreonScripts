#!/usr/bin/env python3

from paramiko.client import SSHClient
import argparse
import sys


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--hostname", action="store", dest="host_name", help="Name of the host to connect to")
    parser.add_argument("-u", "--user", action="store", dest="user_name", help="Name of the user")
    parser.add_argument("-p", "--port", action="store", dest="port", help="Port of the SSH Server")
    args = parser.parse_args()

    with SSHClient() as client:
        client.load_system_host_keys()
        try:
            client.connect(args.host_name, port=args.port, username=args.user_name, key_filename="/var/lib/centreon-engine/.ssh/id_rsa")
        except:
            print("SERVICE STATUS: CRITICAL - SSH Server not reachable")
            sys.exit(2)
    print("SERVICE STATUS: OK - SSH Server responded correctly")
    sys.exit(0)
