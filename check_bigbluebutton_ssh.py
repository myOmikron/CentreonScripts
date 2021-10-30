#!/usr/bin/env python3

#
# In order to execute this plugin, sudo may have to be installed on the target system.
# The user needs to have permissions to execute the /usr/bin/bbb-conf executable. So add
# the following lines to /etc/sudoers:
#
# User_Alias CENTREON = centreon-engine
#
# CENTREON ALL=(ALL) NOPASSWD: /usr/bin/bbb-conf --status
#

import argparse
import subprocess
import re
from datetime import datetime, timedelta


months = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}


def check_freeswitch(args):
    cmd = "journalctl -u freeswitch --no-pager"
    if args.sudo:
        cmd = "sudo " + cmd

    try:
        result = subprocess.run([
            "ssh", "-p", args.port, "-l", args.user, args.host, cmd
        ], stdout=subprocess.PIPE)
        if result.returncode == 0:
            kills = re.findall(r"([A-Za-z]+) ([0-9]+) ([0-9]+):([0-9]+):([0-9]+) .+? status=9/KILL", result.stdout.decode("utf-8"))
            now = datetime.utcnow()
            deaths = 0
            for month, day, hour, minute, second in kills:
                kill = datetime(now.year, months[month], int(day), int(hour), int(minute), int(second))
                if now - kill < timedelta(minutes=15):
                    deaths += 1
            if deaths > 0:
                print(f"Critical - freeswitch was killed in the last 15min | 'freeswitch_killed'={deaths}[];[];[];[];[]")
                exit(2)
            else:
                print(f"OK - no recent SIGKILLs | 'freeswitch_killed'={deaths}[];[];[];[];[]")
                exit(0)
        else:
            print(f"UNKNOWN - Returncode of SSH was not 0")
            exit(3)
    except Exception as err:
        print(f"UNKNOWN - {err}")
        exit(3)


def get_status(arguments):
    active_services = []
    non_active_services = []
    command = "/usr/bin/bbb-conf --status"
    if arguments.sudo:
        command = "sudo " + command
    try:
        run_list = ["ssh", "-p", args.port, "-l", args.user, args.host, command]
        result = subprocess.run(run_list, stdout=subprocess.PIPE)
        if result.returncode == 0:
            result = result.stdout.decode('utf-8')
            result = result.replace('►', '').replace('—', '').replace('✔', '').replace('[', '').replace(']', '').replace('✘', '')
            services = dict(x.replace(' ', '').rsplit("-", 1) for x in result.splitlines())
            non_active_services = [(x, services[x]) for x in services if services[x] == "failed" or services[x] == "inactive"]
            active_services = [(x, services[x]) for x in services if services[x] == "active"]
        else:
            print(f"UNKNOWN - Returncode of SSH was not 0")
            exit(3)
    except Exception as err:
        print(f"UNKNOWN - {err}")
        exit(3)
    if non_active_services:
        return_code = 2
        print(f"Critical - Following components hasn't started: {', '.join([x[0] for x in non_active_services])}||")
    else:
        return_code = 0
        print(f"OK - All services are running")
    exit(return_code)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u",
        "--user",
        action="store",
        dest="user",
        required=False,
        default="centreon-engine",
        help="User for ssh"
    )
    parser.add_argument(
        "-p",
        "--port",
        action="store",
        dest="port",
        required=False,
        default="22",
        help="Port of ssh server"
    )
    parser.add_argument(
        "-H",
        "--host",
        action="store",
        dest="host",
        required=True,
        help="Hostname or IP Address of BBB Server"
    )
    parser.add_argument(
        "--sudo",
        action="store_true",
        dest="sudo",
        help="Specify if the command should be executed with sudo"
    )
    parser.add_argument(
        "-c",
        "--check",
        action="store",
        dest="check",
        required=True,
        choices=["status", "freeswitch"],
        help="Specify the check that should be executed"
    )

    args = parser.parse_args()

    if args.check == "status":
        get_status(args)
    elif args.check == "freeswitch":
        check_freeswitch(args)
