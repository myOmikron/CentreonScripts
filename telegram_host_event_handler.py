#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import requests


def send_message(message, receiver):
    with open('credentials') as fh:
        token = fh.readline()
        if token.endswith('\n'):
            token = token[:-1]
    param_dict = {"text": message,
                  "chat_id": receiver,
                  "parse_mode": "HTML"}
    requests.get('https://api.telegram.org/bot' + token + '/sendMessage', data=param_dict)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', required=True, action='store', dest='name', help='Name of the host')
    parser.add_argument('-s', '--state', required=True, action='store', dest='state', help='State of the host')
    parser.add_argument('-a', '--address', required=True, action='store', dest='address', help='Address of the host')
    parser.add_argument('-o', '--output', required=True, action='store', dest='output', help='Output of the host')
    parser.add_argument('-i', '--id', required=True, action='store', dest='id', help='ID of the chat')
    args = parser.parse_args()

    if args.state == 'UP':
        emoticon = '&#x2714;'
    elif args.state == 'DOWN':
        emoticon = '&#x1f525;'
    elif args.state == 'RECOVERY':
        emoticon = '&#x2934;;'
    elif args.state == 'UNREACHABLE':
        emoticon = '&#x2754;'
    else:
        emoticon = ''

    message = '<b>HOST ' + args.state + ' ALERT</b> ' + emoticon + '\n\n'
    message += 'Host: ' + args.name + '\n'
    message += 'Address: ' + args.address + '\n'
    message += 'Output: ' + args.output + '\n'
    message += 'URL: https://centreon.omikron.dev/centreon/main.php?p=20202&o=hd&host_name=' + args.name
    send_message(message, args.id)


if __name__ == '__main__':
    main()

