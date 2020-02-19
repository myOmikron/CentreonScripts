#!/usr/bin/env python3

import dateutil.parser
from datetime import datetime, timedelta
import sys
import argparse
import subprocess


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", action="store", required=True, dest="url", help="URL of the specified website")
    parser.add_argument("-w", "--warning", action="store", required=True, dest="warning", help="Days after which the script should return a warning")
    parser.add_argument("-c", "--critical", action="store", required=True, dest="critical", help="Days after which the script should return a critical error")
    parser.add_argument("-p", "--port", action="store", dest="port", help="Optional: Port from https server")
    args = parser.parse_args()

    if args.port is None:
        args.port = "443"
    
    cmd = "echo | openssl s_client -showcerts -servername " + args.url + " -connect " + args.url + ":" + args.port + " 2>/dev/null | openssl x509 -inform pem -enddate -noout"
    ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    expiring_date = ret.stdout.read().decode('utf-8').split("=")[1][:-1]
    expiring_date = dateutil.parser.parse(expiring_date)
    expiring_date = expiring_date.replace(tzinfo=None)
    now = datetime.now().replace(tzinfo=None)
    remaining = expiring_date - now

    if remaining < timedelta(days=int(args.critical)):
        print("SERVICE STATUS: Critical - Certificate expires at:", str(expiring_date.strftime("%b %d %Y %H:%M:%S")))
        sys.exit(2)
    elif remaining < timedelta(days=int(args.warning)):
        print("SERVICE STATUS: Warning - Certificate expires at:", str(expiring_date.strftime("%b %d %Y %H:%M:%S")))
        sys.exit(1)
    print("SERVICE STATUS: OK - Certificate expires at:", str(expiring_date.strftime("%b %d %Y %H:%M:%S")))
    sys.exit(0)

