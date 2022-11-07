# Thoth members:
#   Brendan Guillory
#   Cameron Robertson
#   Christian Evans
#   Cody Woessner
#   Drew Young
#   Frankie Lavall
#   Tristen Barton

# prog_05 - TimeLock: given an epoch as input and the current system time,
#   return a password.

import datetime as dt
from time import time
import sys
from hashlib import md5
import pytz

# how long should a code be valid for?
VALID_SECONDS = 60

# code formatting!
# negative numbers mean starting from the end.
# positive numbers mean starting from the beginning.
LETTERS_FIRST = True
NUM_LETTERS = 2
NUM_NUMBERS = -2

DEBUG = False
#DEBUG_SYSTEM_TIME = "2017 04 26 15 14 30"
#DEBUG_EPOCH_TIME = "1974 06 01 08 57 23"

# calculate_code: takes in a datetime. Returns a code.
def calculate_code(epoch_time):
    # get current time
    current_time = dt.datetime.now() # system time (utc)

    if "DEBUG_SYSTEM_TIME" in globals():
        current_time = dt.datetime.strptime(DEBUG_SYSTEM_TIME, "%Y %m %d %H %M %S")

    # convert both times to UTC
    current_time.replace(tzinfo=pytz.UTC)
    epoch_time.replace(tzinfo=pytz.UTC)

    # convert both times to integers
    current_timestamp = current_time.timestamp()
    epoch_timestamp = epoch_time.timestamp()

    # calculate time difference and round
    time_difference = int(current_timestamp - epoch_timestamp)
    time_difference -= (time_difference % VALID_SECONDS)

    # convert to string then to bytes
    time_difference_enc = str(time_difference).encode()

    dbl_hash = md5(md5(time_difference_enc).hexdigest().encode()).hexdigest()

    if DEBUG:
        print("Current time: " + str(current_time))
        print("Epoch time: " + str(epoch_time))
        print(f"Seconds between current and epoch (rounded to nearest {VALID_SECONDS} seconds): {time_difference}")
        print("Double hash: " + str(dbl_hash))

    return md5_to_code(dbl_hash)


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

    return code

if "DEBUG_EPOCH_TIME" in globals():
    epoch = dt.datetime.strptime(DEBUG_EPOCH_TIME, "%Y %m %d %H %M %S")
    print(calculate_code(epoch))
    exit(0)

for line in sys.stdin:
    # remove EOF, etc.
    line_stripped = line.rstrip()

    # convert input to datetime
    epoch = dt.datetime.strptime(line_stripped, "%Y %m %d %H %M %S")

    print(calculate_code(epoch))
