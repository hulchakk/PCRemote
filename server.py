import socket
from multiprocessing import Process

from app import app

server = None


def _serve(host: str, port: int):
    app.run(host=host, port=port, threaded=True, debug=False)


def start_server(port: int):
    global server
    if not is_server_running():
        if not is_port_in_use(port):
            server = Process(target=_serve, args=("0.0.0.0", port), daemon=True)
            server.start()
            return
        else:
            raise Exception("Port already in use")
    raise Exception("Server already running")


def stop_server():
    global server
    if is_server_running():
        server.terminate()
        server.join()
        server = None


def is_server_running() -> bool:
    if server:
        return True
    else:
        return False


def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0
