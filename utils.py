from pynput.keyboard import Controller as KeyboardController, Key, KeyCode

keyboard_controller = KeyboardController()


def press_key(key: Key | str):
    if isinstance(key, str):
        keyboard_controller.press(KeyCode.from_char(key))
    else:
        keyboard_controller.press(key)
    keyboard_controller.release(key)


BINDS = {
    "left": lambda: press_key(Key.left),
    "right": lambda: press_key(Key.right),
    "up": lambda: press_key(Key.up),
    "down": lambda: press_key(Key.down),
    "space": lambda: press_key(Key.space),
    "esc": lambda: press_key(Key.esc),
    "fullscreen": lambda: press_key("f"),
}
