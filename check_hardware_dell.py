#!/usr/bin/env python3
import argparse
import subprocess


def check_chassis(arguments):
    cmd_list = ["ssh", "-p" + str(arguments.port), arguments.user + "@" + arguments.host]
    command = "/opt/dell/srvadmin/bin/omreport chassis"
    if arguments.sudo:
        command = "sudo " + command
    cmd_list.append(command)
    process = subprocess.run(cmd_list, stdout=subprocess.PIPE)
    stdout = process.stdout.decode('utf-8').strip()
    health = {}
    for line in stdout.splitlines()[5:-2]:
        health[line.split(":")[1].strip()] = line.split(":")[0].strip()
    output = "\n".join([": ".join(["Critical", x]) for x in health if health[x] == "Critical"])
    output += "\n".join([": ".join(["Warning", x]) for x in health if health[x] == "Warning"])
    output += "\n".join([": ".join(["Ok", x]) for x in health if health[x] == "Ok"])
    if "Critical" in health.items():
        print("Critical components:", ", ".join([x for x in health if health[x] == "Critical"]))
        print(output)
        exit(2)
    elif "Warning" in health.items():
        print("Warning components:", ", ".join([x for x in health if health[x] == "Warning"]))
        print(output)
        exit(1)
    elif "Ok" in health.items():
        print("Ok components:", ", ".join([x for x in health if health[x] == "Ok"]))
        print(output)
        exit(0)
    else:
        print(f"UNKNOWN: {stdout}")
        exit(3)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-H",
        "--host",
        action="store",
        dest="host",
        required=True,
        help="Host of Dell server"
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
    check_chassis(parser.parse_args())
