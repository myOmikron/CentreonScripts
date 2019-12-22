#!/usr/bin/env python3

import argparse
import sys
import io
import paramiko


if __name__  == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--hostname", action="store", dest="host_name", help="Name of the host to connect to")
    parser.add_argument("-u", "--username", action="store", dest="user_name", help="Name of the user to connect with")
    parser.add_argument("-p", "--port", action="store", dest="port", help="Port to connect to")
    parser.add_argument("-P", "--process", action="store", dest="process", help="Process to search")
    args = parser.parse_args()

    try:
        client = paramiko.client.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        
        with open("/var/lib/centreon-engine/.ssh/id_rsa") as fh:
            string = fh.read()
            keyfile = io.StringIO(string)
            read_private_key = paramiko.RSAKey.from_private_key(keyfile)

        client.connect(args.host_name, username=args.user_name, pkey=read_private_key)
        client.exec_command("ps -aux | grep " + args.process)
    except paramiko.AuthenticationException:
        print("SERVICE STATUS: Critical - Authentication error")
        sys.exit(2)
    except:
        print("SERVICE STATUS: Critical - Unkown Error")
        sys.exit(2)
    client.close()

