import pytest
import subprocess
import time
import os
import signal
import platform
import atexit
import warnings

server_process = None


def start_flask_server():
    """Start the Flask server as a subprocess."""
    global server_process

    # Determine the path to app.py - adjust as needed
    app_path = os.path.join(os.path.dirname(__file__), "retail", "app.py")

    # Check if app.py exists
    if not os.path.exists(app_path):
        app_path = os.path.join(os.path.dirname(__file__), "app.py")
        if not os.path.exists(app_path):
            warnings.warn(f"Could not find app.py in {app_path}")
            return None

    # Start the Flask server
    if platform.system() == "Windows":
        server_process = subprocess.Popen(
            ["python", app_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
    else:
        server_process = subprocess.Popen(
            ["python", app_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )

    # Give the server time to start up
    time.sleep(3)
    return server_process


def stop_flask_server():
    """Stop the Flask server."""
    global server_process
    if server_process:
        try:
            if platform.system() == "Windows":
                os.kill(server_process.pid, signal.CTRL_BREAK_EVENT)
            else:
                os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
            server_process.wait(timeout=5)
        except Exception as e:
            print(f"Error stopping server: {e}")
            if platform.system() != "Windows":
                try:
                    os.killpg(os.getpgid(server_process.pid), signal.SIGKILL)
                except:
                    pass


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown():
    """Set up the Flask server before all tests and tear it down after."""
    server_proc = start_flask_server()
    if not server_proc:
        warnings.warn("Failed to start Flask server. Tests may fail.")

    yield

    stop_flask_server()


# Register the stop_flask_server function to be called when the Python interpreter exits
atexit.register(stop_flask_server)