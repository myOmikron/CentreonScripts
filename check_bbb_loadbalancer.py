#!/usr/bin/env python3
import argparse

import requests
from rc_protocol import get_checksum


def get_request(args, endpoint, params=None):
    if params is None:
        params = {}

    with requests.get(args.host + endpoint, params=params, headers={
        "Authorization": get_checksum(params, args.secret, salt=endpoint),
    }) as response:

        if response.status_code != 200:
            print("UNKNOWN - Request failed with status code: " + str(response.status_code))
            exit(3)

        try:
            json = response.json()
        except:
            print("UNKNOWN - Request didn't return valid json: " + str(response.text))
            exit(3)

        if not json["success"]:
            print("UNKNOWN - Request wasn't successful" + str(json["info"]))
            exit(3)

        return json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-S",
        "--secret",
        action="store",
        dest="secret",
        required=True,
        help="Shared RCP Secret of BBB Loadbalancer"
    )
    parser.add_argument(
        "-H",
        "--host",
        action="store",
        dest="host",
        required=True,
        help="Hostname of BBB Loadbalancer, ex. bbb.example.com"
    )
    parser.add_argument(
        "-c",
        "--check",
        action="store",
        dest="check",
        required=True,
        choices=["serverStates"],
        help="Specify the check that should be executed"
    )
    parser.add_argument(
        "--warning-threshold",
        dest="warn",
        type=float,
        default=1,
        help="Warning when this number is reached",
    )
    parser.add_argument(
        "--critical-threshold",
        dest="crit",
        type=float,
        default=0,
        help="Critical when this number is reached",
    )

    args = parser.parse_args()

    args.host = f"https://{args.host}/monitoring/"
    if args.check == "serverStates":
        enabled = get_request(args, "getServers")["servers"]["enabled"]
        if enabled > args.warn:
            print(f"OK - {enabled} servers enabled")
            exit(0)
        elif enabled > args.crit:
            print(f"WARNING - {enabled} servers enabled")
            exit(1)
        else:
            print(f"CRITICAL - {enabled} servers enabled")
            exit(2)


if __name__ == "__main__":
    main()
