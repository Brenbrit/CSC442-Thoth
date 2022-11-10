# Tutorial: A modified version of steg.py.
#   Run the program with all the same arguments as steg.py except for interval.
#   The program will loop through lots of intervals and save them all, then you
#   just need to figure out which output files are useful.


import argparse
import sys


# constants!

# sentinel value: bytes which indicate the end of a hidden file.
SENTINEL = bytearray([0x0, 0xff, 0x0, 0x0, 0xff, 0x0])

# help message: prints when user gives bad arguments
HELP_MESSAGE = """python {} -(sr) -(bB) -o<val> [-i<val>] -w<val> [-h<val>]
 -s      store
 -r      retrieve
 -b      bit mode
 -B      byte mode
 -o<val> set offset to <val> (default is 0)
 -i<val> set interval to <val> (default is 1)
 -w<val> set wrapper file to <val>
 -h<val> set hidden file to <val>""".format(sys.argv[0])

# debug prints to stderr as output is printed to stdout.
DEBUG = True


# store_data: given arguments, use steg to hid hidden_file inside wrapper_file.
# data is printed to stdout
def store_data(hidden_file, wrapper_file, bit_mode, offset, interval, sentinel):
    if DEBUG:
        print(f"Storing data from {hidden_file} into {wrapper_file} in {'bit' if bit_mode else 'byte'} mode. Offset = {offset}, interval = {interval}", file=sys.stderr)

    # read wrapper and hidden file bytes
    hidden_file_bytes = file_as_bytearray(hidden_file)
    wrapper_file_bytes = file_as_bytearray(wrapper_file)

    # data_sources: all of the data that we will steg.
    data = hidden_file_bytes + sentinel

    # do we have enough space to hide the file?
    min_wrapper_size = (interval * len(data) * (8 if bit_mode else 1)) + offset
    if len(wrapper_file_bytes) < min_wrapper_size:
        print(f"Wrapper is too small. Size: {len(wrapper_file_bytes)} bytes. Minimum size with given arguments: {min_wrapper_size} bytes.", file=sys.stderr)
        return

    # algorithms directly from rubric
    if bit_mode:
        i = 0
        while i < len(data):
            for _ in range(8):
                wrapper_file_bytes[offset] &= 0xfe
                wrapper_file_bytes[offset] |= ((data[i] & 0x80) >> 7)
                data_src[i] << ((data[i] << 1) & 0xff)
                offset += interval
            i += 1

    else: # byte mode
        i = 0
        while i < len(data):
            wrapper_file_bytes[offset] = data[i]
            offset += interval
            i += 1

    # finally, write data to stdout
    sys.stdout.buffer.write(bytes(wrapper_file_bytes))


# retrieve_data: given arguments, use steg to retrieve a hidden file from wrapper_file.
# data is printed to stdout
def retrieve_data(wrapper_file, bit_mode, offset, interval, sentinel):
    if DEBUG:
        print(f"Retrieving data from {wrapper_file} in {'bit' if bit_mode else 'byte'} mode. Offset = {offset}, interval = {interval}", file=sys.stderr)

    # read wrapper file bytes
    wrapper_file_bytes = file_as_bytearray(wrapper_file)
    extracted_bytes = bytearray()

    if bit_mode:
        while offset < len(wrapper_file_bytes):
            b = 0

            for j in range(8):
                b |= (wrapper_file_bytes[offset] & 0x01)
                # Steganography algorithms are copied from the rubric, including this if statement.
                # For this implementation, this statement will always be true.
                if j < 7:
                    b = ((b << 1) & 0xff)
                    offset += interval

            # big vs. little endian does not matter here since we only use one bit.
            extracted_bytes += b.to_bytes(1, 'little')
            offset += interval

            # check if we've read sentinel bytes
            if len(extracted_bytes) > len(sentinel) and extracted_bytes[len(extracted_bytes) - len(sentinel):] == sentinel:
                break

    else: # byte mode
        while offset < len(wrapper_file_bytes):
            b = wrapper_file_bytes[offset]

            # big vs. little endian does not matter here since we only use one bit.
            extracted_bytes += b.to_bytes(1, 'little')
            offset += interval

            # check if we've read sentinel bytes
            if len(extracted_bytes) > len(sentinel) and extracted_bytes[len(extracted_bytes) - len(sentinel):] == sentinel:
                break

    # remove sentinel bytes
    extracted_bytes = extracted_bytes[:-1 * len(sentinel)]
    # write data to stdout
    # sys.stdout.buffer.write(bytes(extracted_bytes))
    return bytes(extracted_bytes)


# given a file location, return a bytearray of all the file's bytes.
def file_as_bytearray(file_loc):
    with open(file_loc, 'rb') as file:
        file_bytes = bytearray(file.read())
    return file_bytes


# run at the beginning of the program. Makes sure arguments don't conflict.
def verify_valid_args(args):
    error_messages = []

    # (s and r) and (b and B) are mutually exclusive. Enforce this!
    if args["s"] and args["r"]:
        error_messages.append("Please specify either -s or -r: you cannot use both.")
    if args["b"] and args["B"]:
        error_messages.append("Please specify either -b or -B: you cannot use both.")

    # verify at least one of (s or r) and (b or B) are present. If not, exit!
    if not (args["s"] or args["r"]):
        error_messages.append("Either -s or -r expected")
    if not (args["b"] or args["B"]):
        error_messages.append("Either -b or -B expected")

    # if we're storing data, we must have a hidden file.
    if args["s"] and not args["h"]:
        error_messages.append("Program operating in store mode but no hidden file provided. Please use -h.")

    # we always need a wrapper file.
    if not args["w"]:
        error_messages.append("Wrapper file not provided. Please specify one with the -w switch.")

    if len(error_messages) == 0:
        # user gave good arguments!
        return
    else:
        # user did not give good arguments. Print help and errors, then exit.
        print(HELP_MESSAGE + "\n", file=sys.stderr)
        for error in error_messages:
            print(f"{sys.argv[0]}: error: {error}", file=sys.stderr)
        exit(0)


# main code!

# provide arguments to argparse.ArgumentParser
all_args = argparse.ArgumentParser(add_help=False, usage=HELP_MESSAGE)
all_args.add_argument("-s", help="Store data inside a file", action='store_true')
all_args.add_argument("-r", help="Retrieve steg'd data from a file", action='store_true')
all_args.add_argument("-b", help="Use bit mode", action='store_true')
all_args.add_argument("-B", help="Use byte mode", action='store_true')
all_args.add_argument("-o", help="Specify offset (default is 0)", type=int, default=0)
all_args.add_argument("-i", help="Specify interval (default is 1)", type=int, default=1)
all_args.add_argument("-w", help="Specify wrapper file", type=str, required=True)
all_args.add_argument("-h", help="Specify hidden file", type=str)

args = vars(all_args.parse_args())
if DEBUG:
    print("Arguments: " + str(args), file=sys.stderr)
verify_valid_args(args)

bit_mode = args["b"]
offset = args["o"]
interval = args["i"]
wrapper_file = args["w"]
hidden_file = args["h"]

if args["s"]: # store
    store_data(hidden_file, wrapper_file, bit_mode, offset, interval, SENTINEL)
else: # retrieve
    for i in range(12):
        try:
            interval = 2**i
            print(f"Retrieving file with interval {i}")
            data = retrieve_data(wrapper_file, bit_mode, offset, interval, SENTINEL)

            with open(wrapper_file + "_interval_" + str(interval), 'wb') as f:
                f.write(data)
        except Exception as e:
            print(f"Program encountered an error on interval {2**i}. This may or may not be intended. Files are still saved.")
            print(e)
            break
