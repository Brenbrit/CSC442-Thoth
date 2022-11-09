# Tutorial: run the program and paste binary. The program will translate to text. It's that easy.
# If your binary is not divisible by 7 or 8, the program will not output anything. If you want
# it to work on your binary anyway, comment out the two if statements at the bottom of the program.

# Thoth members:
#   Brendan Guillory
#   Cameron Robertson
#   Christian Evans
#   Cody Woessner
#   Drew Young
#   Frankie Lavall
#   Tristen Barton

# needed for sys.stdin
import sys

# nonprintable characters
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

# convert a long string of binary to text and print
def decode(line, ascii_encoding=8):
    # big string -> list of 7 or 8-bit strings
    str_byte_data = [line[i:i+ascii_encoding] for i in range(0, len(line), ascii_encoding)]
    # list of strings -> list of ints
    int_byte_data = [str_to_int(byte) for byte in str_byte_data]

    # do we have any nonprintable chars in the input?
    # store the answer in input_contains_nonprintable
    input_contains_nonprintable = False
    for byte in int_byte_data:
        if byte in special_ascii_chars.keys():
            input_contains_nonprintable = True
            break

    # print input with no control characters
    print("".join([chr(byte) for byte in int_byte_data]))

    # if control chars are present, print them in the input too.
    if input_contains_nonprintable:
        print(f"{ascii_encoding}-bit with control chars: ", end="")
        print("".join([special_ascii_chars.get(byte, chr(byte)) for byte in int_byte_data]))


# convert binary (in string form) to int
def str_to_int(byte):
    num = 0
    for i, bit in enumerate(byte[::-1]):
        if bit == '1':
            num += 2 ** i
    return num

for line in sys.stdin:
    # remove EOF, etc.
    line_stripped = line.rstrip()

    if len(line_stripped) % 8 == 0:
        # line may be 8-bit
        print("8-bit: ", end='')
        decode(line_stripped, 8)

    if len(line_stripped) % 7 == 0:
        # line may be 7-bit
        print("7-bit: ", end='')
        decode(line_stripped, 7)
