# Thoth members:
#   Brendan Guillory
#   Cameron Robertson
#   Christian Evans
#   Cody Woessner
#   Drew Young
#   Frankie Lavall
#   Tristen Barton

# mime.py: listens for user input until a specified key (ESCAPE_KEY) is pressed,
# then repeats that user input once.
# If an argument is supplied, the program reads the key event list from that argument.

from pynput.keyboard import Listener, Key, Controller
from termios import tcflush, TCIFLUSH
from sys import stdin, stdout, argv
from time import time, sleep
import pickle

# constants!

# key that signifies the end of input
ESCAPE_KEY = Key.enter
# amount of seconds to wait in-between pressing ESCAPE_KEY and repeating text
SLEEP_SECONDS = 5
# Should we save input data so that the program can use it later?
SAVE_DATA = True

# "enums" - make reading code easier.
KEY_PRESSED = True
KEY_RELEASED = False

# wait_for_escape: halts the program until listen_key is released.
def wait_for_escape(listen_key):
    with Listener(on_press=None, on_release=lambda x: x != listen_key) as listener:
        listener.join()

def read_key_events():

    print(f"Please press {ESCAPE_KEY} to begin reading keystrokes.")
    wait_for_escape(ESCAPE_KEY)

    # each item is a tuple: (KEY_PRESSED or KEY_RELEASED, key, time delta)
    # time delta == current time - start time
    key_event_list = []

    # pressing and releasing simply add each key event to key_event_list.
    # releasing also checks for ESCAPE_KEY.
    def pressing(key):
        key_event_list.append((KEY_PRESSED, key, time() - start_time))
        print(key, end='')

    def releasing(key):
        key_event_list.append((KEY_RELEASED, key, time() - start_time))
        print(key, end='')

        if key == ESCAPE_KEY:
            print()
            return False

    with Listener(on_press=pressing, on_release=releasing) as listener:
        start_time = time()
        listener.join()
    tcflush(stdin, TCIFLUSH)

    return key_event_list

def in_between(key_event_list):

    # print out total repetition time (not necessary, but looks nice :3 )
    total_time = 0
    if len(key_event_list) > 0:
        _, _, total_time = key_event_list[-1]

    print(f"\nFinished reading input. Text will be repeated 5 seconds after you press {ESCAPE_KEY}.")
    print("Recounting text will take exactly {:.3f} seconds.".format(total_time))
    # following lines simply delay program until ESCAPE_KEY is released
    wait_for_escape(ESCAPE_KEY)
    sleep(SLEEP_SECONDS)
    print("Starting now.")

def write_key_events(key_event_list):

    keyboard = Controller()

    start_time = time()
    for event_type, key, time_delta in key_event_list:

        # wait for proper time
        if time_delta - time() + start_time > 0:
            sleep(time_delta - time() + start_time)

        # press/release key
        if event_type == KEY_PRESSED:
            keyboard.press(key)
        else:
            keyboard.release(key)

    tcflush(stdout, TCIFLUSH)
    print()

if len(argv) > 1:
    for p in argv[1:]:
        with open(p, 'rb') as pickle_data:
            key_event_list = pickle.load(pickle_data)
    exit(0)

key_event_list = read_key_events()

if SAVE_DATA:
    # write key events to disk. No need to wait and listen to input longer if we mess up.
    pickle_name = "mime-" + str(int(time())) + ".pickle"
    with open(pickle_name, 'wb') as pickle_data:
        pickle.dump(key_event_list, pickle_data)
    print("Wrote key data to disk for security.")

in_between(key_event_list)
write_key_events(key_event_list)
