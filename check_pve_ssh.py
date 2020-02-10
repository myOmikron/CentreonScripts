#!/usr/bin/env python3
import argparse
import subprocess


def gather_information(args):
    cmd_list = ["ssh", "-p" + args.port, args.user + "@" + args.host]
    command = args.path + "/./pve-monitor.pl --conf " + args.path + "/pve-monitor.conf"
    if args.mode == "nodes":
        command += " --nodes "
    elif args.mode == "containers":
        command += " --containers "
    elif args.mode == "storages":
        command += " --storages "
    elif args.mode == "qemu":
        command += " --qemu "
    cmd_list.append(command + " && echo $?")

    process = subprocess.run(cmd_list, stdout=subprocess.PIPE)
    stdout = process.stdout.decode('utf-8')
    print("\n".join(stdout.splitlines()[:-1]))
    exit(int(stdout.splitlines()[-1]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", required=True, action="store", dest="host", help="IP or domain")
    parser.add_argument("-p", "--port", action="store", dest="port", default="22", help="Port of SSH")
    parser.add_argument("-u", "--user", action="store", dest="user", default="centreon-engine", help="SSH username")
    parser.add_argument("-m", "--mode", action="store", dest="mode",
                        choices=["nodes", "containers", "storages", "qemu"], help="Mode to choose")
    parser.add_argument("-P", "--path", action="store", dest="path", required=True, help="Path to pve-monitor")

    args = parser.parse_args()
    gather_information(args)


if __name__ == '__main__':
    main()
