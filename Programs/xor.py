# Tutorial: Given a file and a key file (KEY_LOC below), return
#   (file xor key). Directly from rubric. Make sure to redirect output.

# constants!
# The location for the key file
KEY_LOC = "key"

# for sys.stdin and sys.stdout
import sys

# input_bytes and key file => output bytes
def process_input(input_bytes):
    # read inupt and key as bytearray
	m = bytearray(input_bytes)
	k = bytearray(read_key_bytes())

    # check that sizes are equal
	if len(m) != len(k):
		print("Sizes of input and key are different: ", end='')
		print(f"len(message) = {len(m)}, len(key) = {len(k)}.")

    # actual xor operation
	result_bytes = []
	for i in range(len(m)):
		result_bytes.append(m[i] ^ k[i])

    # output, and then we're done
	sys.stdout.buffer.write(bytes(result_bytes))

# key file => bytes object
def read_key_bytes():
	with open(KEY_LOC, 'rb') as key_file:
		data = key_file.read()
	return data


# main code
process_input(sys.stdin.buffer.read())
