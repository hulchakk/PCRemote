import os
import shutil
import subprocess
import sys

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


def move_mouse(dx: int, dy: int):
    sensativity = 1.5
    mouse_controller.move(dx * sensativity, dy * sensativity)


def click_mouse(button_type: str):
    if button_type == "left":
        mouse_controller.click(Button.left, 1)
    elif button_type == "right":
        mouse_controller.click(Button.right, 1)


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
}
