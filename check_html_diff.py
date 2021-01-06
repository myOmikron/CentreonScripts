#!/usr/bin/env python3
import argparse
import requests


def main(arguments):
    try:
        with open(arguments.file, "r") as f:
            old = f.read().strip()
        new = requests.get(arguments.url, headers={"user-agent": "curl/7.74.0"}).text.strip().replace("\r\n", "\n")
        with open(arguments.file, "w") as f:
            f.write(new)
        if old != new:
            print(f"There are updates at {arguments.url}")
            exit(1)
        else:
            print("Nothing changed")
            exit(0)
    except FileNotFoundError:
        new = ""
        try:
            new = requests.get(arguments.url).text.strip()
        except requests.exceptions.ConnectionError:
            print(f"STATUS Critical - Could not connect")
            exit(2)
        with open(arguments.file, "w") as f:
            f.write(new)
        print("STATUS OK - Creating Buffer ...")
        exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-U",
        "--url",
        action="store",
        dest="url",
        required=True,
        help="The URL to check"
    )
    parser.add_argument(
        "-f",
        "--file",
        action="store",
        dest="file",
        required=True,
        help="The path to the file to write the buffer to"
    )
    args = parser.parse_args()
    main(args)
