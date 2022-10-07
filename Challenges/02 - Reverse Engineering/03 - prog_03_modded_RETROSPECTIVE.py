# prog_03_modded_RETROSPECTIVE.py: the third edition of Thoth's Program 03 for CSC 442-001.
#
# Version 1: program deciphers the message from a single FTP folder's contents.
# Version 2: program recursively deciphers the message from every available folder
#            on an FTP server, ignoring hidden folders.
# Version 3: program recursively deciphers the message from every available folder
#            on an FTP server.
#
# Usage: simply modify the FTP login information immediately below this comment and execute.

# constants
IP = "192.168.1.1"
PORT = 21
USER = "osiris"
PASSWORD = "EncryptionGods"
FOLDER = ""
USE_PASSIVE = True

# DEBUG: very verbose. Lists data about connecting, etc.
DEBUG = True
# PRINT_FILES: prints the output of each "ls" command.
PRINT_FILES = False

# IGNORE_SPECIALS: if a decoded message has an ascii
# character 0-31, don't show it.
IGNORE_SPECIALS = False

# any decoded message below MIN_LEN won't be shown.
MIN_LEN = 0

# ftplib: for connecting to the remote file server.
import ftplib

special_ascii_chars = {
        0:	"[NUL]",    # null
        1:	"[SOH]",    # start of header
        2:	"[STX]",    # start of text
        3:	"[ETX]",    # end of text
        4:	"[EOT]",    # end of transmission
        5:	"[ENQ]",    # enquiry
        6:	"[ACK]",    # acknowledge
        7:	"[BEL]",    # bell
        8:	"[BS]",     # backspace
        9:	"[HT]",     # horizontal tab
        10:	"[LF]",     # line feed
        11:	"[VT]",     # vertical tab
        12:	"[FF]",     # form feed
        13:	"[CR]",     # carriage return
        14:	"[SO]",     # shift out
        15:	"[SI]",     # shift in
        16:	"[DLE]",    # data link escape
        17:	"[DC1]",    # device control 1
        18:	"[DC2]",    # device control 2
        19:	"[DC3]",    # device control 3
        20:	"[DC4]",    # device control 4
        21:	"[NAK]",    # negative acknowledge
        22:	"[SYN]",    # synchronous idle
        23:	"[ETB]",    # end of transmission block
        24:	"[CAN]",    # cancel
        25:	"[EM]",     # end of medium
        26:	"[SUB]",    # substitute
        27:	"[ESC]",    # escape
        28:	"[FS]",     # file separator
        29:	"[GS]",     # group separator
        30:	"[RS]",     # record separator
        31:	"[US]",     # unit separator
        }


# to_bin: converts perms ("drw-r-xrwx") to a binary string ("1110101111").
# If a character is '-', add a '0'. Else, add a '1'.
def to_bin(chars):

    return "".join(['0' if c == '-' else '1' for c in chars])


# method_7: decode message from file permissions using method 7
def method_7(files, directory):

    # to_output: stores the decoded message as we go along
    to_output = ""

    for file in files:

        if file[:3] != "---":
            # one of the first three bits were set.
            # Ignore!
            continue

        # convert file permissions to decimal number
        dec = int(to_bin(file[3:10]), 2)

        # if option is set, throw out any decimals 0-31
        if IGNORE_SPECIALS and dec in special_ascii_chars.keys():
            to_output = ""
            break
        to_output += special_ascii_chars.get(dec, chr(dec))

    # print result
    if to_output != "" and len(to_output) >= MIN_LEN:
        print("Method 07, dir " + directory + ":\n    ", end='')
        print(to_output)
        print()


# method_10: decode message from file permissions using method 7
def method_10(files, directory):

    # to_output: stores the decoded message as we go along
    to_output = ""

    # build bit string
    bit_string = ""
    for file in files:
        # [:10] == first 10 characters
        bit_string += to_bin(file[:10])

    # convert bit string to text in 7-bit parts
    for i in range(0, len(bit_string), 7):

        # convert bits to decimal number
        dec = int(bit_string[i:i+7], 2)

        # if option is set, throw out any decimals 0-31
        if IGNORE_SPECIALS and dec in special_ascii_chars.keys():
            to_output = ""
            break

        to_output += special_ascii_chars.get(dec, chr(dec))

    # print result
    if to_output != "" and len(to_output) >= MIN_LEN:
        print("Method 10, dir " + directory + ":\n    ", end='')
        print(to_output)
        print()


# decode_files: given a list of files and a directory they came from,
# decode covert messages in file permissions based on  constants at the
# top of this file. Does not return anything, but prints results.
def decode_files(files, directory):

    # We don't know whether the message is encoded with method
    # 7 or 10. Run both.

    # These functions are separated because they work in fairly
    # different ways. method_10 is a bit more complicated.

    method_7(files, directory)
    method_10(files, directory)


def ftp_recurse(directory):
    # try to cwd (sometimes this doesn't work)
    if DEBUG:
        print(f"cwd {directory}", end='')
    try:
        ftp.cwd(directory)
        # no error with "ls"
        if DEBUG:
            print(" success.")
    except ftplib.error_perm:
        # we didn't have perms to run "ls". The answer likely isn't here.
        if DEBUG:
            print(" failure.")
        return

    # write down the files in a directory
    files = []
    ftp.dir("-a", files.append)

    # remove . and ..
    files_cleaned = []
    for file_listing in files:
        if file_listing.split()[-1] not in [".", ".."]:
            files_cleaned.append(file_listing)

    files = files_cleaned

    file_lists.append((directory, files))

    # print the file listing if requested
    if PRINT_FILES:
        for file in files:
            print(file)

    # recurse
    for entry in files:
        if entry[0] == 'd':
            # d == directory
            ftp_recurse(directory + entry.split()[-1] + '/')


# Main code!

if DEBUG:
    print("Connecting to FTP server.")

# connect
ftp = ftplib.FTP()
ftp.connect(IP, PORT)
if DEBUG:
    print("Connection successful. Logging in.")
ftp.login(USER, PASSWORD)
ftp.set_pasv(USE_PASSIVE)

if DEBUG:
    print("Connection to server successful. Beginning scan.")

# (dir, [files])
file_lists = []

# read all files and store in file_lists
ftp_recurse(FOLDER)

# disconnect
ftp.quit()

if DEBUG:
    print("Scan complete. Beginning analysis.\n")

# scan each directory's listgng
for directory, files in file_lists:
    decode_files(files, directory)
