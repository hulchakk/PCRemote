from flask import Flask, request, render_template

from utils import BINDS, system_sleep

app = Flask(__name__)

VALID_REMOTES = ("media",)


@app.route("/partials/<remote_type>")
def get_partial(remote_type):
    if remote_type in VALID_REMOTES:
        return render_template(f"partials/{remote_type}.html")

    return "Not found", 404


@app.route("/api/keyboard", methods=["POST"])
def keyboard():
    try:
        data = request.get_json()

        BINDS[data["key"]]()

        return {"status": "ok"}

    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.route("/api/system_sleep", methods=["POST"])
def system():
    try:
        system_sleep()
        return {"status": "ok"}

    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, threaded=True, debug=True)
