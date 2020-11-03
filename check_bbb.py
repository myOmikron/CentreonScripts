#!/usr/bin/env python3

import argparse
import hashlib

import requests
import xmltodict
import json


def create_bbb_query(action_str, shared_secret, query_str=""):
    return query_str + "&checksum=" + \
           str(hashlib.sha1((action_str + query_str + shared_secret).encode("utf-8")).hexdigest())


def num_meetings(arguments):
    ret = requests.get(arguments.url + "getMeetings?" + create_bbb_query("getMeetings", arguments.secret))
    if ret.status_code != 200:
        print("UNKNOWN - Request failed with status code: " + str(ret.status_code))
        exit(3)
    d = json.loads(json.dumps(xmltodict.parse(ret.text)))
    if d["response"]["returncode"] != "SUCCESS":
        print("UNKNOWN - Request was not successful")
    if "messageKey" in d["response"]:
        if d["response"]["messageKey"] == "noMeetings":
            print("OK - 0 meetings are running | " + "'num_meetings'=0[];[100];[100];[0];[100]")
            exit(0)
    meetings = str(len(d["response"]["meetings"]["meeting"])
                   if isinstance(d["response"]["meetings"]["meeting"], list) else 1)
    print("OK - " + meetings + " meetings are running | " + "'num_meetings'=" + meetings + "[];[100];[100];[0];[100]")
    exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-U", "--url", required=True, action="store", dest="url", help="URL of API to connect to")
    parser.add_argument("-S", "--secret", required=True, action="store", dest="secret", help="Secret of BBB Server")
    parser.add_argument("-A", "--action", required=True, action="store", dest="action", nargs="?",
                        choices=["num_meetings"], help="API action to send")

    args = parser.parse_args()

    if args.action == "num_meetings":
        num_meetings(args)
