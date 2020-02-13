#!/usr/bin/env python3
import argparse
import re
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", action="store", dest="port", default="22", help="SSH Port")
    parser.add_argument("-H", "--host", required=True, action="store", dest="host", help="IP or domain to connect to")
    parser.add_argument("-u", "--user", action="store", dest="user", default="centreon-engine", help="User")
    parser.add_argument("--sudo", action="store_true", dest="sudo", help="Specify true if sudo should be used")
    parser.add_argument("-P", "--path", action="store", dest="path", default="/opt/MegaRAID/MegaCli/MegaCli64",
                        help="Path to MegaCLI application. Default: /opt/MegaRAID/MegaCli/MegaCli64")

    args = parser.parse_args()

    cmd = "sudo " if args.sudo else ""
    cmd += args.path
    cmd += r""" -pdlist -a0 \
         | grep -E '(Slot Number)|(Firmware state)' \
         | sed ':a;N;$!ba;s/\\nFirmware state: /\:/g'"""
    run_list = ["ssh", "-p", args.port, "-l", args.user, args.host, cmd]
    result = subprocess.run(run_list, stdout=subprocess.PIPE)

    status = {}

    temp_slot = ""
    for line in result.stdout.decode('utf-8').splitlines():
        if "Slot Number:" in line:
            temp_slot = "".join(re.findall(r"\d", line))
        elif "Firmware state:" in line:
            status[temp_slot] = line.split(":")[1][1:]

    is_critical = False
    critical_items = []
    hotspare_items = []
    online_items = []
    for disk in status:
        if "Online" not in status[disk] and "Hotspare" not in status[disk]:
            is_critical = True
            critical_items.append(disk)
        elif "Hotspare" in status[disk]:
            hotspare_items.append(disk)
        else:
            online_items.append(disk)

    if is_critical:
        print("STATUS Critical:", end="")
    else:
        print("STATUS OK:", end="")

    print("{} Disks Critical,".format(len(critical_items)) if is_critical else "",
          "{} Disks Online, {} Disks Hotspare".format(len(online_items), len(hotspare_items)), "|")

    print("".join(["Disk " + x + ": " + status[x] + "\n" for x in status]))

    if is_critical:
        sys.exit(2)
    sys.exit(0)


if __name__ == '__main__':
    main()
