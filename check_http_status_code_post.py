#!/usr/bin/env python3

import requests
import argparse
import sys


def main(arguments):
    response = requests.post(arguments.url)
    if response.status_code == 200:
        print("SERVICE STATUS: OK - Received Status code 200") 
        sys.exit(0)
    else:
        print("SERVICE STATUS: CRITICAL - Received Status code", response.status_code, "|")
        print(response.text)
        sys.exit(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", action="store", dest="url", help="URL of the specified website")
    args = parser.parse_args()
    main(args) 
