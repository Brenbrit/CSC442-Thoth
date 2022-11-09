# prog_05 - TimeLock: given an epoch as input and the current system time,
#   return a password.

import datetime as dt
from time import time
import sys
import socket
from hashlib import md5
import pytz
import pyperclip

# challenge stipulation: how should we find the middle
# of an even-length hash?
import math
#tiebreaker_op = math.floor
tiebreaker_op = math.ceil

TIME_SERVER = ("138.47.99.64", 54321)

DEBUG = True
DEBUG_EPOCH_TIME = "2022 10 28 11 00 00"

EPOCH_TIME_FORMAT = "%Y %m %d %H %M %S"
SERVER_TIME_FORMAT = "%a %d %b %Y %H:%M:%S"

SERVER_RESPONSE_BEGIN = 0
SERVER_RESPONSE_END = 24

# how long should a code be valid for?
VALID_SECONDS = 60

# code formatting!
# negative numbers mean starting from the end.
# positive numbers mean starting from the beginning.
LETTERS_FIRST = True
NUM_LETTERS = 2
NUM_NUMBERS = -2


def md5_to_code(input_hash):
    code = ""

    # find letters
    hash_letters = "".join([ch for ch in input_hash if ch.isalpha()])
    letter_order = NUM_LETTERS // abs(NUM_LETTERS)
    code += hash_letters[::letter_order][:abs(NUM_LETTERS)]

    # find numbers
    hash_numbers = "".join([ch for ch in input_hash if ch.isnumeric()])
    number_order = NUM_NUMBERS // abs(NUM_NUMBERS)
    code += hash_numbers[::number_order][:abs(NUM_NUMBERS)]

    # challenge stipulation (using int division)
    # code += input_hash[tiebreaker_op(len(input_hash)//2)]

    return code

# assuming TIME_SERVER is set, return the time server's message.
def get_server_time():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect(TIME_SERVER)
    server_time = s.recv(8192).decode().rstrip()[SERVER_RESPONSE_BEGIN: SERVER_RESPONSE_END]
    #                    ^^^^ arbitrarily chosen bit length
    s.close()

    if DEBUG:
        print("  Server response: " + server_time)
    return server_time

# calculate_code: takes in a datetime. Returns a code.
def calculate_code(epoch_time):
    # get current time
    current_time = dt.datetime.now() # system time (utc)

    if "TIME_SERVER" in globals():
        server_time = get_server_time().rstrip()
        print("Server time: " + server_time)
        # Dr. Timo's time server returns times in the following format
        #   Fri 28 Oct 2022 04:04:10 PM
        current_time = dt.datetime.strptime(server_time, SERVER_TIME_FORMAT)

    # convert both times to UTC
    current_time.replace(tzinfo=pytz.UTC)
    epoch_time.replace(tzinfo=pytz.UTC)

    # convert both times to integers
    current_timestamp = current_time.timestamp()
    epoch_timestamp = epoch_time.timestamp()

    # calculate time difference and round
    time_difference = int(current_timestamp - epoch_timestamp)
    valid_seconds_left = VALID_SECONDS - (time_difference % VALID_SECONDS)
    time_difference -= (time_difference % VALID_SECONDS)

    # convert to string then to bytes
    time_difference_enc = str(time_difference).encode()

    dbl_hash = md5(md5(time_difference_enc).hexdigest().encode()).hexdigest()

    if DEBUG:
        print("Current time: " + str(current_time))
        print("Epoch time: " + str(epoch_time))
        print(f"Seconds between current and epoch (rounded to nearest {VALID_SECONDS} seconds): {time_difference}")
        print("Double hash: " + str(dbl_hash))
        print(f"Code will be valid for {valid_seconds_left} more seconds")

    code = md5_to_code(dbl_hash)
    password = "disintuitive" + code
    pyperclip.copy(password)
    print("Copied " + password + " to clipboard.")

    return code



if "DEBUG_EPOCH_TIME" in globals():
    epoch = dt.datetime.strptime(DEBUG_EPOCH_TIME, EPOCH_TIME_FORMAT)
    print(calculate_code(epoch))
    exit(0)

# for the challenge, this part of the program was never run
# because the epoch time was provided.
for line in sys.stdin:
    # remove EOF, etc.
    line_stripped = line.rstrip()

    # convert input to datetime
    epoch = dt.datetime.strptime(line_stripped, EPOCH_TIME_FORMAT)

    code = calculate_code(epoch)
    print("Timelock code: " + code)
