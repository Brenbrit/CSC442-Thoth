# Thoth members:
#   Brendan Guillory
#   Cameron Robertson
#   Christian Evans
#   Cody Woessner
#   Drew Young
#   Frankie Lavall
#   Tristen Barton

# duplicator_new.py: paste a typing profile in list form in the "password"
# and "timings" variables below. The program will then wait for you to press
# ESCAPE_KEY, and will type out the provided password with the provided timings.

from pynput.keyboard import Controller, Listener, Key
from time import sleep

# constants!

# the key that must be pressed to begin the second half of the program.
ESCAPE_KEY = Key.enter

# extra prints
DEBUG = True

# time to wait after pressing ESCAPE_KEY
WAIT_TIME = 8

# wait_for_escape: halts the program until listen_key is released.
def wait_for_escape(listen_key):
    with Listener(on_press=None, on_release=lambda x: x != listen_key) as listener:
        listener.join()

password = ['C', 'a', 'n', ' ', 'y', 'o', 'u', ' ', 'b', 'e', 'l', 'i', 'e', 'v', 'e', ' ', 'c', 'y', 'b', 'e', 'r', 's', 't', 'o', 'r', 'm', ' ', 'i', 's', ' ', 'i', 'n', ' ', 't', 'w', 'o', ' ', 'w', 'e', 'e', 'k', 's', '?', 'Ca', 'an', 'n ', ' y', 'yo', 'ou', 'u ', ' b', 'be', 'el', 'li', 'ie', 'ev', 've', 'e ', ' c', 'cy', 'yb', 'be', 'er', 'rs', 'st', 'to', 'or', 'rm', 'm ', ' i', 'is', 's ', ' i', 'in', 'n ', ' t', 'tw', 'wo', 'o ', ' w', 'we', 'ee', 'ek', 'ks', 's?']
password_str = "".join(password[:len(password)//2 + 1])
print(f"Sample = {password}")

timings = ['0.13', '0.27', '0.22', '0.17', '0.19', '0.25', '0.24', '0.28', '0.15', '0.41', '0.47', '0.32', '0.49', '0.29', '0.37', '0.25', '0.46', '0.40', '0.26', '0.40', '0.13', '0.15', '0.24', '0.21', '0.39', '0.18', '0.44', '0.39', '0.41', '0.34', '0.30', '0.13', '0.24', '0.43', '0.29', '0.30', '0.45', '0.32', '0.49', '0.46', '0.26', '0.37', '0.22', '0.30', '0.49', '0.39', '0.22', '0.21', '0.19', '0.27', '0.18', '0.11', '0.27', '0.23', '0.26', '0.39', '0.48', '0.19', '0.29', '0.29', '0.30', '0.32', '0.30', '0.39', '0.42', '0.17', '0.42', '0.48', '0.47', '0.32', '0.31', '0.38', '0.44', '0.27', '0.39', '0.17', '0.27', '0.41', '0.24', '0.22', '0.15', '0.33', '0.48', '0.46', '0.36']

# convert to float
timings = [float(a) for a in timings]

keypress = timings[:len(timings)//2 + 1]
keyinterval = timings[len(timings) // 2 + 1:]

print(f"KHTs = {keypress}")
print(f"KITs = {keyinterval}")

print(f"Profile loaded. Press {ESCAPE_KEY} to begin duplicating after {WAIT_TIME} seconds.")
sleep(WAIT_TIME)
print("Starting now.")

keyboard = Controller()
for i, key in enumerate(password_str):
    keyboard.press(key)
    sleep(timings[i])
    keyboard.release(key)
    if i < len(keyinterval): # last key has no interval
        if DEBUG:
            print(f"{key} hold={timings[i]} interval={keyinterval[i]}")
        sleep(keyinterval[i])
    elif DEBUG:
        print(f"{key} hold={timings[i]} interval=None")
print("Done")
keyboard.press(Key.enter)
keyboard.release(Key.enter)
