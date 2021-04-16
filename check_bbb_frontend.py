#!/usr/bin/env python3
import argparse

import requests
from rc_protocol import get_checksum


def make_request(*args, **kwargs):
    response = requests.get(*args, **kwargs)
    if response.status_code != 200:
        print("UNKNOWN - Request failed with status code: " + str(response.status_code))
        exit(3)
    response = response.json()
    if not response["success"]:
        print("UNKNOWN - Request was not successful")
        exit(3)
    return response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host",
        required=True,
        help="Hostname of bbb-frontend"
    )
    parser.add_argument(
        "--rcp-secret",
        required=True,
        help=""
    )
    parser.add_argument(
        "--meeting-id",
        required=True,
        help=""
    )
    args = parser.parse_args()

    args.host = f"https://{args.host}/api/v1/"
    params = {"meeting_id": args.meeting_id}
    response = make_request(args.host+"viewerCount", params={
        **params,
        "checksum": get_checksum(params, args.rcp_secret, "viewerCount")
    })
    print("OK - "+str(response["value"])+" viewers")
    exit(0)


if __name__ == "__main__":
    main()

