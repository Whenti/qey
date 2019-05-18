#!/usr/bin/env python
# based on: https://github.com/cryzed/bin/blob/master/hotstrings

import argparse
import collections
import json
import os
import signal
import subprocess
import sys
import psutil
from datetime import datetime

import Xlib
import Xlib.X
import Xlib.XK
import Xlib.display
import Xlib.ext.record
import Xlib.protocol

HOME = os.path.expanduser("~")
PIDS_PATH = os.path.join(HOME,'.config','qey','pids')
MY_PID = os.path.join(PIDS_PATH, str(os.getpid()))

if not os.path.isdir(PIDS_PATH):
    os.mkdir(PIDS_PATH)

for file in os.listdir(PIDS_PATH):
    PID = int(file)
    p = psutil.Process(PID)
    p.terminate()

os.mknod(MY_PID)

def remove_pidfile():
    os.remove(MY_PID)

import atexit
atexit.register(remove_pidfile)

EXIT_FAILURE = 1
RECORD_CONTEXT_ARGUMENTS = (
    0,
    (Xlib.ext.record.AllClients,),
    ({
         'core_requests': (0, 0),
         'core_replies': (0, 0),
         'ext_requests': (0, 0, 0, 0),
         'ext_replies': (0, 0, 0, 0),
         'delivered_events': (0, 0),
         'device_events': (Xlib.X.KeyPress, Xlib.X.KeyRelease),
         'errors': (0, 0),
         'client_started': False,
         'client_died': False
     },)
)

# Load xkb to access XK_ISO_Level3_Shift
Xlib.XK.load_keysym_group('xkb')
event_field = Xlib.protocol.rq.EventField(None)


def getClipboardData():
    p = subprocess.Popen(['xclip','-selection', 'clipboard', '-o'], stdout=subprocess.PIPE)
    retcode = p.wait()
    data = p.stdout.read()
    return data

def setClipboardData(data):
    p = subprocess.Popen(['xclip','-selection','clipboard'], stdin=subprocess.PIPE)
    p.stdin.write(data)
    p.stdin.close()
    retcode = p.wait()


def parse_event_fields(data, display):
    while data:
        event, data = event_field.parse_binary_value(data, display, None, None)
        yield event


def get_xdg_config_home():
    xdg_config_home = os.getenv('XDG_CONFIG_HOME')
    if xdg_config_home is not None and os.path.isabs(xdg_config_home):
        return xdg_config_home

    return os.path.expanduser('~/.config')


argument_parser = argparse.ArgumentParser()
argument_parser.add_argument('path', metavar='PATH', nargs='?',
                             help='Path to JSON file containing hotstring definitions. Default: %(default)s',
                             default=os.path.join(get_xdg_config_home(), 'hotstrings.json'))
argument_parser.add_argument('--verbose', '-v', action='store_true')
arguments = argument_parser.parse_args()


class RecordHandler:
    MODIFIER_KEY_MASKS = {
        'Shift': Xlib.X.ShiftMask,
        'Lock': Xlib.X.LockMask,
        'Control': Xlib.X.ControlMask,
        'Alt': Xlib.X.Mod1Mask,
        'Mod1': Xlib.X.Mod1Mask,
        'Mod2': Xlib.X.Mod2Mask,
        'Mod3': Xlib.X.Mod3Mask,
        'Mod4': Xlib.X.Mod4Mask,
        'Mod5': Xlib.X.Mod5Mask
    }

    def __init__(self, connection, record_connection, callback):
        self.connection = connection
        self.record_connection = record_connection
        self.callback = callback

        self.alt_gr_pressed = False
        self.alt_gr_keycodes = set(i[0] for i in self.connection.keysym_to_keycodes(Xlib.XK.XK_ISO_Level3_Shift))

    def get_modifier_state_index(self, state):
        pressed = {n: (state & m) == m for n, m in self.MODIFIER_KEY_MASKS.items()}
        index = 0
        if pressed['Shift']:
            index += 1
        if pressed['Alt']:
            index += 2
        if self.alt_gr_pressed:
            index += 4

        return index

    def key_pressed(self, event):
        if event.detail in self.alt_gr_keycodes:
            self.alt_gr_pressed = True

        keysym = self.connection.keycode_to_keysym(event.detail, self.get_modifier_state_index(event.state))
        character = self.connection.lookup_string(keysym)
        if character:
            self.callback(character)

    def key_released(self, event):
        if event.detail in self.alt_gr_keycodes:
            self.alt_gr_pressed = False

    def __call__(self, reply):
        if not reply.category == Xlib.ext.record.FromServer:
            return
        for event in parse_event_fields(reply.data, self.record_connection.display):
            if event.type == Xlib.X.KeyPress:
                self.key_pressed(event)
            else:
                self.key_released(event)

def verbose(*args, **kwargs):
    if arguments.verbose:
        print(*args, **kwargs)

class HotstringProcessor:
    BACKSPACE_CHARACTER = '\x08'
    ENTER_CHARACTER = '\x0D'
    SPACE_CHARACTER = '\x20'
    CTRL_V = (55,5)
    EMPTY_CHAR = '\x00'

    def __init__(self, hotstrings, connection, queue_size):
        self.hotstrings = hotstrings
        self.connection = connection
        self.queue = collections.deque(maxlen=queue_size)
        self.root_window = self.connection.screen().root

        self._default_key_press_event_arguments = dict(time=Xlib.X.CurrentTime, root=self.root_window,
                                                       child=Xlib.X.NONE, root_x=0, root_y=0, event_x=0, event_y=0,
                                                       same_screen=1)
        self._default_key_release_event_arguments = self._default_key_press_event_arguments

    def make_key_press_event(self, detail, state, window, **kwargs):
        arguments = self._default_key_press_event_arguments.copy()
        arguments.update(kwargs)
        return Xlib.protocol.event.KeyPress(detail=detail, state=state, window=window, **arguments)

    def make_key_release_event(self, detail, state, window, **kwargs):
        arguments = self._default_key_release_event_arguments.copy()
        arguments.update(kwargs)
        return Xlib.protocol.event.KeyRelease(detail=detail, state=state, window=window, **arguments)

    def string_to_keycodes(self, string_):
        for character in string_:
            code_point = ord(character)

            keycodes = tuple(self.connection.keysym_to_keycodes(code_point) or
                             self.connection.keysym_to_keycodes(0xFF00 | code_point))
            keycode = keycodes[0] if keycodes else None

            if not keycode:
                verbose('No keycode found for: %r.' % character, file=sys.stderr)
                continue

            yield keycode

    def type_keycode(self, keycode, window):
        detail, state = keycode
        window.send_event(self.make_key_press_event(detail, state, window))
        window.send_event(self.make_key_release_event(detail, state, window))

    def type_keycodes(self, keycodes, window):
        for keycode in keycodes:
            self.type_keycode(keycode, window)

        self.connection.flush()

    def __call__(self, character):
        if character == self.BACKSPACE_CHARACTER and self.queue:
            self.queue.pop()
        elif character != self.EMPTY_CHAR:
            self.queue.append(character)

        queue_string = ''.join(self.queue)
        backspace = tuple(self.string_to_keycodes(self.BACKSPACE_CHARACTER))
        window = self.connection.get_input_focus().focus
        for hotstring, (action, *arguments) in self.hotstrings.items():
            if not queue_string.endswith(hotstring+self.SPACE_CHARACTER):
                continue

            if action == 'replace':
                replacement = arguments[0]
            elif action == 'run':
                replacement = eval(arguments[0])
            else:
                verbose('Unrecognized action: %r.' % action)
                continue

            clipboard = getClipboardData()
            setClipboardData(replacement.encode())

            self.type_keycodes(backspace * (len(hotstring)+1), window)
            self.type_keycodes([self.CTRL_V], window)
            self.queue.clear()

            # Reset clipboard
            #setClipboardData(clipboard)

            return


def main():
    path = os.path.expanduser(arguments.path)
    if not os.path.exists(path):
        argument_parser.exit(EXIT_FAILURE, path + ': No such file or directory.\n')

    connection = Xlib.display.Display()
    record_connection = Xlib.display.Display()

    if not record_connection.has_extension('RECORD'):
        argument_parser.exit(EXIT_FAILURE, 'X Record Extension Library not found.\n')

    with open(path) as file:
        hotstrings = json.load(file)

    if not hotstrings:
        argument_parser.exit(EXIT_FAILURE, 'No hotstrings defined.\n')

    record_context = record_connection.record_create_context(*RECORD_CONTEXT_ARGUMENTS)
    hotstring_processor = HotstringProcessor(hotstrings, connection, max(len(k) for k in hotstrings.keys())+1)
    record_handler = RecordHandler(connection, record_connection, hotstring_processor)

    def clean_up(*args):
        record_connection.record_free_context(record_context)
        record_connection.close()
        connection.close()
        argument_parser.exit()

    for signal_ in signal.SIGINT, signal.SIGTERM:
        signal.signal(signal_, clean_up)

    verbose('Listening for hotstrings...')
    record_connection.record_enable_context(record_context, record_handler)


if __name__ == '__main__':
    main()
