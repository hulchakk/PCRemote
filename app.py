from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from utils import BINDS, system_sleep

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345"
socketio = SocketIO(app, cors_allowed_origins="*")

VALID_REMOTES = ("media",)


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


@socketio.on("system_sleep")
def handle_system_sleep(data):
    try:
        system_sleep()
        emit("response", {"status": "ok"})
    except Exception as e:
        emit("response", {"status": "error", "message": str(e)})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)
