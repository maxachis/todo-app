#!/usr/bin/env python3
"""
Launch the ToDo app: starts the Django dev server and opens the browser.

Usage:
    python launch.py

First time? After the browser opens, click the install icon in the address bar
(Chrome/Edge) to install the app as a standalone window.
"""

import os
import signal
import subprocess
import sys
import time
import urllib.request
import webbrowser

URL = "http://localhost:8000"
MANAGE_PY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "manage.py")


def wait_for_server(url, timeout=10):
    """Poll until the server responds or timeout is reached."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(url, timeout=1)
            return True
        except Exception:
            time.sleep(0.3)
    return False


def main():
    print("Starting ToDo app...")
    server = subprocess.Popen(
        [sys.executable, MANAGE_PY, "runserver", "0.0.0.0:8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    try:
        if wait_for_server(URL):
            print(f"Server ready at {URL}")
            webbrowser.open(URL)
            print(
                "\nTip: To install as a standalone app, click the install icon\n"
                "     in your browser's address bar (Chrome/Edge).\n"
            )
        else:
            print("Warning: server did not respond in time, opening browser anyway.")
            webbrowser.open(URL)

        print("Press Ctrl+C to stop the server.\n")
        server.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.send_signal(signal.SIGINT)
        server.wait(timeout=5)
    finally:
        if server.poll() is None:
            server.terminate()


if __name__ == "__main__":
    main()
