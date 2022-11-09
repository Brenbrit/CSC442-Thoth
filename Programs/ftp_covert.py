# Thoth members:
#   Brendan Guillory
#   Cameron Robertson
#   Christian Evans
#   Cody Woessner
#   Drew Young
#   Frankie Lavall
#   Tristen Barton

# METHOD: please set to 7 or 10 (bits)
METHOD = 7

# Example: Egypt

# decoding:
# E = 69 = 001 000 101 = 105
#          --x --- r-x
# g = 103 = 001 100 111 = 147
#           --x r-- rwx
# y = 121 = 001 111 001 = 171
#           --x rwx --x
# p = 112 = 001 110 000 = 160
#           --x rw- ---
# t = 116 = 001 110 100 = 164
#           --x rw- r--

# can be derived from:
# touch file1 && chmod 105 file1
# touch file2 && chmod 147 file2
# touch file3 && chmod 171 file3
# touch file4 && chmod 160 file4
# touch file5 && chmod 164 file5

from ftplib import FTP

# constants
IP = "138.47.99.64"
PORT = 21
USER = "anonymous"
PASSWORD = ""
FOLDER = ""
USE_PASSIVE = True

# connect
ftp = FTP()
ftp.connect(IP, PORT)
ftp.login(USER, PASSWORD)
ftp.set_pasv(USE_PASSIVE)

# change to proper directory
ftp.cwd(FOLDER)

# write down all the files and folders
files = []
ftp.dir(files.append)

# disconnect
ftp.quit()

# function that converts perms ("drw-r-xrwx")
# to a binary string ("1110101111")
def to_bin(chars):
    to_return = ""
    for char in chars:
        if char == '-':
            to_return += '0'
        else:
            to_return += '1'
    return to_return

# a string which stores the covert message
to_output = ""

# if the METHOD is 7, each file converts to exactly one character.
# Easy!
if METHOD == 7:
    for file in files:
        # make sure the first 3 bits aren't set (ignore if they are)
        if file[:3] != "---":
            continue

        # add character to to_output
        to_output += chr(int(to_bin(file[3:10]), 2))

elif METHOD == 10:
    # if METHOD is 10, then we have to build a long bit string
    # before converting to ascii.

    # build bit string
    bit_string = ""
    for file in files:
        bit_string += to_bin(file[:10])

    # convert bit string to text in 7-bit parts
    for i in range(0, len(bit_string), 7):
        to_output += chr(int(bit_string[i:i+7], 2))

# finally, print output
# print "[NO_DATA]" in case string was empty
print(to_output if to_output != "" else "[NO DATA]")
