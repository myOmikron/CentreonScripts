#!/usr/bin/env python3
import argparse
import hashlib
import json

import requests
import xmltodict


def create_bbb_query(action_str, shared_secret, query_str=""):
    return query_str + "&checksum=" if query_str else "checksum=" + \
           str(hashlib.sha1((action_str + query_str + shared_secret).encode("utf-8")).hexdigest())


def make_query(url):
    ret = requests.get(url)
    if ret.status_code != 200:
        print("UNKNOWN - Request failed with status code: " + str(ret.status_code))
        exit(3)
    d = json.loads(json.dumps(xmltodict.parse(ret.text)))
    if d["response"]["returncode"] != "SUCCESS":
        print("UNKNOWN - Request was not successful")
        exit(3)
    return d


def get_api_version(arguments):
    url = f"{arguments.host}"
    d = make_query(url)
    version = d["response"]["version"]
    print(f"OK - API Version: {version}")
    exit(0)


def get_active_conferences(arguments):
    url = f"{arguments.host}getMeetings?{create_bbb_query('getMeetings', arguments.secret)}"
    d = make_query(url)
    if "messageKey" in d["response"]:
        if d["response"]["messageKey"] == "noMeetings":
            print("OK - 0 meetings are running | 'num_meetings'=0[];[100];[100];[0];[100]")
            exit(0)
    meetings = str(len(d["response"]["meetings"]["meeting"])
                   if isinstance(d["response"]["meetings"]["meeting"], list) else 1)
    print(f"OK - {meetings} meetings are running | 'num_meetings'={meetings}[];[100];[100];[0];[100]")
    exit(0)


def get_active_participants(arguments):
    url = f"{arguments.host}getMeetings?{create_bbb_query('getMeetings', arguments.secret)}"
    d = make_query(url)
    if "messageKey" in d["response"]:
        if d["response"]["messageKey"] == "noMeetings":
            print("OK - 0 participants | 'participants'=0[];[1000];[1000];[0];[1000]")
            exit(0)
    if isinstance(d["response"]["meetings"]["meeting"], list):
        participants = sum([int(x["participantCount"]) for x in d["response"]["meetings"]["meeting"]])
    else:
        participants = d["response"]["meetings"]["meeting"]["participantCount"]
    print(f"OK - {participants} participants | 'participants'={participants}[];[1000];[1000];[0];[1000]")
    exit(0)


def get_listener_count(arguments):
    url = f"{arguments.host}getMeetings?{create_bbb_query('getMeetings', arguments.secret)}"
    d = make_query(url)
    if "messageKey" in d["response"]:
        if d["response"]["messageKey"] == "noMeetings":
            print("OK - 0 listener | 'listener'=0[];[1000];[1000];[0];[1000]")
            exit(0)
    if isinstance(d["response"]["meetings"]["meeting"], list):
        listeners = sum([int(x["listenerCount"]) for x in d["response"]["meetings"]["meeting"]])
    else:
        listeners = d["response"]["meetings"]["meeting"]["listenerCount"]
    print(f"OK - {listeners} listeners | 'listeners'={listeners}[];[1000];[1000];[0];[1000]")
    exit(0)


def get_voice_participant_count(arguments):
    url = f"{arguments.host}getMeetings?{create_bbb_query('getMeetings', arguments.secret)}"
    d = make_query(url)
    if "messageKey" in d["response"]:
        if d["response"]["messageKey"] == "noMeetings":
            print("OK - 0 voiceParticipants | 'voiceParticipants'=0[];[1000];[1000];[0];[1000]")
            exit(0)
    if isinstance(d["response"]["meetings"]["meeting"], list):
        voice_participants = sum([int(x["voiceParticipantCount"]) for x in d["response"]["meetings"]["meeting"]])
    else:
        voice_participants = d["response"]["meetings"]["meeting"]["voiceParticipantCount"]
    print(f"OK - {voice_participants} voiceParticipants | 'voiceParticipants'={voice_participants}[];[1000];[1000];[0];[1000]")
    exit(0)


def get_video_count(arguments):
    url = f"{arguments.host}getMeetings?{create_bbb_query('getMeetings', arguments.secret)}"
    d = make_query(url)
    if "messageKey" in d["response"]:
        if d["response"]["messageKey"] == "noMeetings":
            print("OK - 0 videoParticipants | 'videoParticipants'=0[];[1000];[1000];[0];[1000]")
            exit(0)
    if isinstance(d["response"]["meetings"]["meeting"], list):
        video_participants = sum([int(x["videoCount"]) for x in d["response"]["meetings"]["meeting"]])
    else:
        video_participants = d["response"]["meetings"]["meeting"]["videoCount"]
    print(f"OK - {video_participants} videoParticipants | 'videoParticipants'={video_participants}[];[1000];[1000];[0];[1000]")
    exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-S",
        "--secret",
        action="store",
        dest="secret",
        required=True,
        help="Shared Secret of BBB Server"
    )
    parser.add_argument(
        "-H",
        "--host",
        action="store",
        dest="host",
        required=True,
        help="Hostname of BBB, ex. bbb.example.com"
    )
    parser.add_argument(
        "-c",
        "--check",
        action="store",
        dest="check",
        required=True,
        choices=["activeConferences", "apiVersion", "activeParticipantsCount", "listenerCount",
                 "voiceParticipantsCount", "videoCount"],
        help="Specify the check that should be executed"
    )

    args = parser.parse_args()

    args.host = f"https://{args.host}/bigbluebutton/api/"
    if args.check == "activeConferences":
        get_active_conferences(args)
    elif args.check == "apiVersion":
        get_api_version(args)
    elif args.check == "activeParticipantsCount":
        get_active_participants(args)
    elif args.check == "listenerCount":
        get_listener_count(args)
    elif args.check == "voiceParticipantsCount":
        get_voice_participant_count(args)
    elif args.check == "videoCount":
        get_video_count(args)
