# Thoth members:
#   Brendan Guillory
#   Cameron Robertson
#   Christian Evans
#   Cody Woessner
#   Drew Young
#   Frankie Lavall
#   Tristen Barton

# for sys.stdin.readline() and sys.argv
import sys

# the letters we will accept in our key
# A = 65, Z = 90, a = 97, z = 122
# ENCODABLE_CHARS = "ABC...XYZabc...xyz"
ENCODABLE_CHARS = "".join([chr(i) for i in range(65, 91)]
    + [chr(i) for i in range(97, 123)])

# "ABC...XYZ".
# indexing into this string gives us the alphebet number of a letter
UPPER_ALPHABET = "".join([chr(i) for i in range(65, 91)])


# given a string and key, return an encoded/decoded message according to the operation variable
def vigenere(text, key):
    current_key_letter = 0
    output = ""

    for letter in text:
        # only change letters. No special characters.
        if letter in ENCODABLE_CHARS:
            # capital or lowercase?
            capital = True if ord(letter) < 91 else False

            # text_letter and key_letter are numbers 0-25.
            # the shift described by key_letter will be eventually
            # combined with text_letter in the out_letter variable
            text_letter = UPPER_ALPHABET.index(letter.upper())
            key_letter = UPPER_ALPHABET.index(key[current_key_letter % len(key)].upper())

            # another number 0-25 indicating which letter the output should be
            if operation == "encode":
                out_letter = (text_letter + key_letter) % 26
            else:
                out_letter = (text_letter - key_letter + 26) % 26

            # convert out_letter to a real character and make it cap/lower
            output += chr(out_letter + 65) if capital else chr(out_letter + 97)

            # increment which key letter we are using
            current_key_letter += 1
        else:
            # the letter was not a letter. Ignore.
            output += letter

    return output

def print_help():
    print("Please provide either an encryption or decryption key.")
    print(f"Example: python3 {sys.argv[0]} -e mykey")
    print(f"Example: python3 {sys.argv[0]} -d myotherkey")

# check for correct number of args
if len(sys.argv) < 3:
    print("Improper arguments supplied.")
    print_help()
    exit(0)

# get key without special characters
key = "".join([i for i in sys.argv[2] if i in ENCODABLE_CHARS])

# are we encoding or decoding?
# store this in the operation variable
operation = None
if sys.argv[1].lower() == "-e":
    operation = "encode"
elif sys.argv[1].lower() == "-d":
    operation = "decode"

# we didn't get a -d or -e
# print help and exit
if operation == None:
    print_help()
    exit(0)

while True:
    # read the next line
    line = sys.stdin.readline()

    # line = false if EOF has been reached
    if line:
        # rstrip() removes \n, etc.
        print(vigenere(line.strip(), key))
    else:
        sys.exit(0)
