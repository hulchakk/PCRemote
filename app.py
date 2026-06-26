from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from utils import BINDS, system_sleep, click_mouse, move_mouse, type_text, scroll_mouse

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345"
socketio = SocketIO(app, cors_allowed_origins="*")

VALID_REMOTES = ("media", "touchpad", "text")


@app.route("/partials/<remote_type>")
def get_partial(remote_type):
    if remote_type in VALID_REMOTES:
        return render_template(f"partials/{remote_type}.html")
    return "Not found", 404


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("keyboard")
def handle_keyboard(data):
    try:
        key = data.get("key")
        if key in BINDS:
            BINDS[key]()
            emit("response", {"status": "ok"})
    except Exception as e:
        emit("response", {"status": "error", "message": str(e)})


@socketio.on("text")
def handle_text(data):
    try:
        text = data.get("text")
        type_text(text)
    except Exception as e:
        emit("response", {"status": "error", "message": str(e)})


@socketio.on("system_sleep")
def handle_system_sleep(data):
    try:
        system_sleep()
        emit("response", {"status": "ok"})
    except Exception as e:
        emit("response", {"status": "error", "message": str(e)})


@socketio.on("mouse_move")
def handle_mouse_move(data):
    try:
        dx = data.get("dx", 0)
        dy = data.get("dy", 0)
        move_mouse(dx, dy)
    except Exception as e:
        print(f"Mouse move error: {e}")


@socketio.on("mouse_click")
def handle_mouse_click(data):
    try:
        button = data.get("button", "left")
        click_mouse(button)
    except Exception as e:
        print(f"Mouse click error: {e}")


@socketio.on("mouse_scroll")
def handle_mouse_scroll(data):
    try:
        dx = data.get("dx", 0)
        dy = data.get("dy", 0)
        scroll_mouse(dx, dy)
    except Exception as e:
        print(f"Mouse scroll error: {e}")
