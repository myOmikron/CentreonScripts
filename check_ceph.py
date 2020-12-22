#!/usr/bin/env python3

#
# In order to execute this plugin, sudo may have to be installed on the target system.
# The user needs to have permissions to execute the /usr/bin/ceph executable. So add
# the following lines to /etc/sudoers:
#
# User_Alias CENTREON = centreon-engine
#
# CENTREON ALL=(ALL) NOPASSWD: /usr/bin/ceph health
# CENTREON ALL=(ALL) NOPASSWD: /usr/bin/ceph osd stat
#

import argparse
import subprocess


def check_health(arguments):
    cmd_list = ["ssh", "-p" + str(arguments.port), arguments.user + "@" + arguments.host]
    command = "/usr/bin/ceph health"
    if arguments.sudo:
        command = "sudo " + command
    cmd_list.append(command)
    process = subprocess.run(cmd_list, stdout=subprocess.PIPE)
    stdout = process.stdout.decode('utf-8')
    if stdout.strip().startswith("HEALTH_OK"):
        print(f"{stdout.strip()}")
        exit(0)
    elif stdout.strip().startswith("HEALTH_WARN"):
        print(f"{stdout.strip()}")
        exit(1)
    elif stdout.strip().startswith("HEALTH_ERR"):
        print(f"{stdout.strip()}")
        exit(2)
    else:
        print(f"UNKNOWN - {stdout}")
        exit(3)


def check_osds(arguments):
    cmd_list = ["ssh", "-p" + str(arguments.port), arguments.user + "@" + arguments.host]
    command = "/usr/bin/ceph osd stat"
    if arguments.sudo:
        command = "sudo " + command
    cmd_list.append(command)
    process = subprocess.run(cmd_list, stdout=subprocess.PIPE)
    stdout = process.stdout.decode('utf-8')

    try:
        osd_num = stdout.split(" ")[0]
        osd_up = stdout.split(" ")[2]
        osd_in = stdout.split(" ")[6]

        if osd_num == osd_in == osd_up == arguments.osd_num:
            print(f"ALL {osd_num} OSDs are there, up and in")
            exit(0)
        else:
            print(f"Mismatch of expected {arguments.osd_num} OSDs and num: {osd_num}, up: {osd_up}, in: {osd_in}")
            print(1)
    except Exception:
        print(f"UNKNOWN - Parsing of {stdout} failed")
        exit(3)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-H",
        "--host",
        action="store",
        dest="host",
        required=True,
        help="Host of Ceph server"
    )
    parser.add_argument(
        "-u",
        "--user",
        action="store",
        dest="user",
        default="centreon-engine",
        required=False,
        help="SSH User, defaults to centreon-engine"
    )
    parser.add_argument(
        "-p",
        "--port",
        action="store",
        dest="port",
        required=False,
        default=22,
        type=int,
        help="Specify the SSH port"
    )
    parser.add_argument(
        "--sudo",
        action="store_true",
        dest="sudo",
        required=False,
        help="Use sudo to execute commands"
    )
    parser.add_argument(
        "-c",
        "--check",
        action="store",
        dest="check",
        required=True,
        choices=[
            "health",
            "osd"
        ],
        help="The check that should be executed"
    ),
    parser.add_argument(
        "--osd-num",
        action="store",
        dest="osd_num",
        required=False,
        help="Number of expected OSDs, checks if all are up and in"
    )

    args = parser.parse_args()

    if args.check == "health":
        check_health(args)
    elif args.check == "osd":
        check_osds(args)
