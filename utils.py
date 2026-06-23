import os
import shutil
import socket
import subprocess
import sys

from pynput import keyboard
from pynput.keyboard import Controller as KeyboardController, Key, KeyCode
from pynput.mouse import Controller as MouseController, Button

keyboard_controller = KeyboardController()
mouse_controller = MouseController()


def system_sleep():
    if sys.platform.startswith("win"):
        subprocess.run(
            ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], check=True
        )
    elif sys.platform == "darwin":
        subprocess.run(["pmset", "sleepnow"], check=True)
    else:
        if shutil.which("systemctl"):
            cmd = ["systemctl", "suspend"]
            if os.name != "nt" and shutil.which("sudo"):
                cmd = ["sudo"] + cmd
            subprocess.run(cmd, check=True)
        elif shutil.which("pm-suspend"):
            cmd = ["pm-suspend"]
            if os.name != "nt" and shutil.which("sudo"):
                cmd = ["sudo"] + cmd
            subprocess.run(cmd, check=True)
        else:
            raise RuntimeError(
                "No known suspend command found (systemctl or pm-suspend)."
            )


def press_key(key: Key | str):
    if isinstance(key, str):
        keyboard_controller.press(KeyCode.from_char(key))
    else:
        keyboard_controller.press(key)
    keyboard_controller.release(key)


def press_key_combination(first: Key | str, second: Key | str):
    if isinstance(first, str):
        first = KeyCode.from_char(first)
    if isinstance(second, str):
        second = KeyCode.from_char(second)
    with keyboard_controller.pressed(first):
        keyboard_controller.press(second)
        keyboard_controller.release(second)


def move_mouse(dx: int, dy: int):
    mouse_controller.move(dx * SENSATIVITY, dy * SENSATIVITY)


def click_mouse(button_type: str):
    if button_type == "left":
        mouse_controller.click(Button.left, 1)
    elif button_type == "right":
        mouse_controller.click(Button.right, 1)


def type_text(text: str):
    if not isinstance(text, str):
        return
    keyboard_controller.type(text)


def clear_text():
    BINDS["select"]()
    BINDS["delete"]()


SENSATIVITY = 1.8

BINDS = {
    "left": lambda: press_key(Key.left),
    "right": lambda: press_key(Key.right),
    "up": lambda: press_key(Key.up),
    "down": lambda: press_key(Key.down),
    "space": lambda: press_key(Key.space),
    "esc": lambda: press_key(Key.esc),
    "fullscreen": lambda: press_key("f"),
    "vol-up": lambda: press_key(Key.media_volume_up),
    "vol-down": lambda: press_key(Key.media_volume_down),
    "mute": lambda: press_key(Key.media_volume_mute),
    "delete": lambda: press_key(Key.backspace),
    "enter": lambda: press_key(Key.enter),
    "back": lambda: press_key_combination(Key.cmd, Key.left),
    "forward": lambda: press_key_combination(Key.cmd, Key.right),
    "refresh": lambda: press_key_combination(Key.cmd, "r"),
    "undo": lambda: press_key_combination(Key.cmd, "z"),
    "redo": lambda: press_key_combination(Key.cmd, "y"),
    "clear": clear_text,
    "select": lambda: press_key_combination(Key.cmd, "a"),
}


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
