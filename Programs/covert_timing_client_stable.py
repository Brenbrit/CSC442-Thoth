# Tutorial: Simply change the IP and port below and run the program.
#   First, the program will connect to the server and determine the timings.
#     Press Ctrl+C to finish this process.
#   Second, the program will read the server's covert information over and over.
#     Press Ctrl+C to finish this process.


# Constants!

IP = "138.47.99.64"
PORT = 21

# enables debugging output
DEBUG = False

# number of bits per character
MSG_BITS = 8

# treats packets with more than one character as errors.
ONLY_SINGLE_CHARS = True


import socket
from sys import stdout
from time import time
from binascii import unhexlify
from datetime import datetime
import pyperclip


# cutoff value: delays equal or higher than this are 1.
# Delays lower to this are 0.
# This can be manually set (as it is for prog_04), but this program
# will determine it though data analysis.
# CUTOFF = (0.1 + 0.025)/2 # seconds

# Grabs and decodes a message from the server. Almost an exact copy of prog_04_client.py
def get_msg(cutoff):

    # create the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the server
    s.connect((IP, PORT))

    # placeholder string which holds covert bits ('0' or '1')
    covert_bits = ""

    # receive data until EOF
    print("Overt message: ", end='')
    data = s.recv(4096).decode()
    while (data.rstrip("\n") != "EOF"):
        # output the data
        stdout.write(data)
        stdout.flush()
        # start the "timer", get more data, and end the "timer"
        t0 = time()
        data = s.recv(4096).decode()
        t1 = time()
        # calculate the time delta (and output if debugging)
        delta = round(t1 - t0, 3)

        # did we drop any packets?
        if ONLY_SINGLE_CHARS:
            covert_bits += '?' * (len(data) - 1)

        # translate delta to 0 or 1
        if delta < cutoff:
            # zero
            covert_bits += '0'
        else:
            covert_bits += '1'

        if (DEBUG):
            stdout.write(" {} -> {}\n".format(delta, covert_bits[-1]))
            stdout.flush()

    # close the connection to the server
    s.close()
    print()

    if DEBUG:
        print("Binary: " + "".join(covert_bits))

    return decode_message(covert_bits, MSG_BITS)

# A naive algorithm which returns the two modes of a set of data.
# There exist more mathematically compotent ways to do this, but those are
# likely not necessary for this program.
def determine_bimodal_medians(deltas):

    deltas.sort()

    first_half_deltas = deltas[:len(deltas)//2]
    second_half_deltas = deltas[len(deltas)//2:]

    first_mid = len(first_half_deltas) // 2
    first_median = (first_half_deltas[first_mid] + first_half_deltas[~first_mid]) / 2

    second_mid = len(second_half_deltas) // 2
    second_median = (second_half_deltas[second_mid] + second_half_deltas[~second_mid]) / 2

    return (first_median, second_median)


def determine_cutoff():

    # initialize delta list and two peaks
    deltas = []
    first_peak = -1
    second_peak = -1

    try:
        while True:
            # create the socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # connect to the server
            s.connect((IP, PORT))

            print("Determining timing cutoff point. Press Ctrl+C to end this process.")

            # receive data until EOF
            data = s.recv(4096).decode()
            while (data.rstrip("\n") != "EOF"):
                # start the "timer", get more data, and end the "timer"
                t0 = time()
                data = s.recv(4096).decode()
                t1 = time()
                # calculate the time delta (and output if debugging)
                delta = round(t1 - t0, 3)

                # did we drop any packets?
                if ONLY_SINGLE_CHARS and len(data) > 1:
                    continue

                deltas.append(delta)

                # estimated peaks based off of data so far
                if len(deltas) < 2:
                    continue

                first_peak, second_peak = determine_bimodal_medians(deltas)

                print(f"Peaks so far: {first_peak}, {second_peak}")
                estimated_cutoff = (second_peak + first_peak) / 2
                print("Estimated cutoff so far: {:.3f}".format(estimated_cutoff))
                print("Ctrl+C to accept this value or wait for more precise results.")

            # close the connection to the server
            s.close()

    except KeyboardInterrupt:
            print(f"\nCtrl+C read. Most likely peaks so far: {first_peak}, {second_peak}")
            estimated_cutoff = (second_peak + first_peak) / 2
            print("Cutoff to be used: {:.3f}\n".format(estimated_cutoff))
            return estimated_cutoff

def decode_message(covert_bits, bit_num):

    output = ""

    # translate covert messagae to ascii and store output
    for i in range(0, len(covert_bits), bit_num):
        if '?' not in covert_bits[i:i+bit_num]:
            output += chr(int(covert_bits[i:i+bit_num], 2))
        else:
            output += '?'

    return output

def likely_letters(stable_msg):
    to_return = ""
    letter_num = 0
    while letter_num in stable_msg.keys():

        if DEBUG == True:
            print(f"{str(letter_num).zfill(3)}: ", end='')

        # remove question marks
        stable_msg[letter_num].pop("?", None)

        # print ? if no other letters exist
        if len(stable_msg[letter_num].keys()) == 0:
            to_return += "?"
            letter_num += 1
            if DEBUG == True:
                print(" {}")
            continue

        # a letter other than ? exists! Print it.
        most_common_letter = max(stable_msg[letter_num], key=stable_msg[letter_num].get)
        to_return += most_common_letter
        if DEBUG == True:
            print(stable_msg[letter_num])
        letter_num += 1

    return to_return

def add_message_data(stable_msg, msg):
    for index, char in enumerate(msg):
        if stable_msg.get(index) == None:
            stable_msg[index] = {char: 1}
        else:
            if char in stable_msg[index].keys():
                stable_msg[index][char] += 1
            else:
                stable_msg[index][char] = 1

def decode_message_stable(cutoff):

    # stable_msg: a dictionary of dictionaries
    # each sub-dict represents the responses we've gotten for that letter.
    # example: {"c": 4, "e", 1} ==> c
    stable_msg = {}
    iteration = 1
    while True:
        print(f"Beginning iteration {iteration}.")
        try:
            next_msg = get_msg(cutoff)
            add_message_data(stable_msg, next_msg)

            print(f"Message at the end of iteration {iteration}: ", end='')
            print(likely_letters(stable_msg))
            print()

        except KeyboardInterrupt:
            to_copy = "Covert message: " + likely_letters(stable_msg)
            formatted_time = datetime.now().strftime("%H:%M:%S")
            to_copy += "\nTime: " + formatted_time

            pyperclip.copy(to_copy)
            print("\n" + to_copy)
            print("\nText copied to clipboard!")
            exit(0)

        iteration += 1


if __name__ == "__main__":
    # is CUTOFF already set?
    if "CUTOFF" in locals() or "CUTOFF" in globals():
        decode_message_stable(CUTOFF)

    else:
        # determine cutoff through math and experimentation
        cutoff = determine_cutoff()
        decode_message_stable(cutoff)
