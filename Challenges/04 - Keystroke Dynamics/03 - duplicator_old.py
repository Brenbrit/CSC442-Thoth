# Thoth members:
#   Brendan Guillory
#   Cameron Robertson
#   Christian Evans
#   Cody Woessner
#   Drew Young
#   Frankie Lavall
#   Tristen Barton

# duplicator_old.py: written before the challenge. Change the constant
# below and feed the program a typing profile to have it replicate
# STRING in the provided profile.

STRING = "This is my password"

from pynput.keyboard import Controller, Listener, Key
from time import sleep
from random import uniform
from termios import tcflush, TCIFLUSH
from sys import stdout


ESCAPE_KEY = Key.enter

DEBUG = False

WAIT_TIME = 5

# wait_for_escape: halts the program until listen_key is released.
def wait_for_escape(listen_key):
    with Listener(on_press=None, on_release=lambda x: x != listen_key) as listener:
        listener.join()

password = input()
timings = input()
print(f"Features = {password}")
print(f"Timings = {timings}")

password = password.split(',')
password_str = password[:len(password)//2 + 1]
password_str = "".join(password_str)
print(f"Sample = {password}")

interval_chars = password[len(password) // 2 + 1:]
intervals = {}

timings = timings.split(',')
timings = [float(a) for a in timings]
keypress = timings[:len(timings)//2 + 1]
keyinterval = timings[len(timings) // 2 + 1:]
print(f"KHTs = {keypress}")
print(f"KITs = {keyinterval}")

presses = {}
for index, key in enumerate(keypress):
    presses[password_str[index]] = key

for index, key in enumerate(interval_chars):
    intervals[key] = keyinterval[index]

avg_hold = 0
for i in presses.keys():
    avg_hold += presses[i]
avg_hold /= len(presses.keys())
avg_interval = 0
for i in intervals.keys():
    avg_interval += intervals[i]
avg_interval /= len(intervals.keys())

print(intervals)
print(presses)

print(f"Profile loaded. Press {ESCAPE_KEY} to begin duplicating after {WAIT_TIME} seconds.")
sleep(WAIT_TIME)
print("Starting now.")


keyboard = Controller()
for index, key in enumerate(STRING):
    if DEBUG:
        print(f"Pressing {key}")
    keyboard.press(key)
    if DEBUG:
        print(f"Sleeping for {presses.get(key, avg_hold)} seconds (pressing).")
    sleep(presses.get(key, avg_hold))
    keyboard.release(key)
    if DEBUG:
        print(f"Releasing {key}")
    if index < len(STRING):
        if DEBUG:
            print(f"Sleeping for {intervals.get(key, avg_interval)} seconds (interval).")
        sleep(intervals.get(key, avg_interval))

tcflush(stdout, TCIFLUSH)
print()
