import socket
from multiprocessing import Process

from app import app, socketio

_server_process = None


def _serve(host: str, port: int):
    socketio.run(
        app,
        host=host,
        port=port,
        debug=False,
        use_reloader=False,
    )


def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def is_server_running() -> bool:
    global _server_process
    return _server_process is not None and _server_process.is_alive()


def start_server(port: int = 8000, host: str = "0.0.0.0"):
    global _server_process

    if is_server_running():
        return "already_running"

    if is_port_in_use(port):
        raise RuntimeError(f"Port {port} is already in use")

    _server_process = Process(target=_serve, args=(host, port), daemon=True)
    _server_process.start()
    return "started"


def stop_server():
    global _server_process

    if not is_server_running():
        return "not_running"

    _server_process.terminate()
    _server_process.join(timeout=3)

    if _server_process.is_alive():
        _server_process.kill()
        _server_process.join(timeout=1)

    _server_process = None
    return "stopped"
