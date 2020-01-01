#!/usr/bin/env python3
# k5923d.py
#
# Copyright 2020 StanGenchev
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name(s) of the above copyright
# holders shall not be used in advertising or otherwise to promote the sale,
# use or other dealings in this Software without prior written
# authorization.

from pathlib import Path
import argparse
import logging
import daemon
from daemon import pidfile
from evdev import InputDevice
from evdev import list_devices
from evdev import UInput
from evdev import ecodes

debug_p = False
daemon_path = "/var/lib/k5923_daemon"

def monitor_events(logf):
    active_keys = []
    key_input = UInput()
    device_path = ""
    devices = [InputDevice(path) for path in list_devices()]
    for device in devices:
        if device.info.vendor == 6127 and device.info.product == 24646 and "input0" in device.phys:
            device_path = device.path

    def inject_input(*args):
        if len(args) > 0:
            for key in args:
                key_input.write(ecodes.EV_KEY, key, 1)
            for key in args:
                key_input.write(ecodes.EV_KEY, key, 0)
            key_input.syn()

    if device_path != "":
        device = InputDevice(device_path)
        device.grab()
        for event in device.read_loop():
            if event.type == ecodes.EV_KEY:
                if event.value == 1:
                    active_keys.append(event.code)
                elif event.value == 0:
                    if len(active_keys) == 1:
                        # Pinch in/out
                        if active_keys[0] == 29:
                            inject_input(ecodes.KEY_LEFTCTRL)
                        # 4 Finger swipe up
                        elif active_keys[0] == 125:
                            inject_input(ecodes.KEY_LEFTMETA, ecodes.KEY_PAGEDOWN)
                        # 3 Finger swipe down
                        elif active_keys[0] == 109:
                            inject_input(ecodes.KEY_LEFTMETA)
                        # 3 Finger swipe up
                        elif active_keys[0] == 104:
                            inject_input(ecodes.KEY_LEFTMETA, ecodes.KEY_UP)
                    elif len(active_keys) == 2:
                        # Top to Bottom edge Swipe
                        if [56, 62] == active_keys:
                            inject_input(ecodes.KEY_LEFTALT, ecodes.KEY_F4)
                        # Rotate Clockwise
                        elif [29, 52] == active_keys:
                            inject_input(ecodes.KEY_LEFTCTRL, ecodes.KEY_R)
                        # Rotate Counterclockwise
                        elif [29, 51] == active_keys:
                            inject_input(ecodes.KEY_LEFTSHIFT, ecodes.KEY_LEFTCTRL, ecodes.KEY_R)
                        # 3 Finger swipe left
                        elif [56, 105] == active_keys:
                            inject_input(ecodes.KEY_LEFTMETA, ecodes.KEY_LEFT)
                        # 3 Finger swipe right
                        elif [56, 106] == active_keys:
                            inject_input(ecodes.KEY_LEFTMETA, ecodes.KEY_RIGHT)
                        # 4 Finger swipe down
                        elif [125, 32] == active_keys:
                            inject_input(ecodes.KEY_LEFTMETA, ecodes.KEY_PAGEUP)
                        # 4 Finger swipe right
                        elif [125, 38] == active_keys:
                            inject_input(ecodes.KEY_LEFTMETA, ecodes.KEY_L)
                    elif len(active_keys) == 3:
                        # Left edge swipe
                        if [29, 125, 14] == active_keys:
                            inject_input(ecodes.KEY_LEFTMETA, ecodes.KEY_A)
                        # Right edge swipe
                        elif [56, 125, 193] == active_keys:
                            inject_input(ecodes.KEY_LEFTMETA, ecodes.KEY_TAB)
                        # Top edge swipe
                        elif [29, 125, 193] == active_keys:
                            inject_input(ecodes.KEY_LEFTMETA, ecodes.KEY_DOWN)
                    active_keys.clear()
    else:
        key_input.close()


def start_daemon(pidf, logf):
    ### This launches the daemon in its context
    global debug_p
    global daemon_path

    if debug_p:
        print("k5923_daemon: entered run()")
        print("k5923_daemon: pidf = {}    logf = {}".format(pidf, logf))
        print("k5923_daemon: about to start daemonization")

    ### XXX pidfile is a context
    with daemon.DaemonContext(
        working_directory=daemon_path,
        umask=0o002,
        pidfile=pidfile.TimeoutPIDLockFile(pidf),
        ) as context:
        monitor_events(logf)


if __name__ == "__main__":
    Path(daemon_path).mkdir(parents=True, exist_ok=True)
    parser = argparse.ArgumentParser(description="Daemon for monitoring and controlling the input from a Lenovo K5923 touchpad.")
    parser.add_argument('-p', '--pid-file', default='/var/run/k5923_daemon.pid')
    parser.add_argument('-l', '--log-file', default='/var/log/k5923_daemon.log')
    args = parser.parse_args()
    start_daemon(pidf=args.pid_file, logf=args.log_file)
