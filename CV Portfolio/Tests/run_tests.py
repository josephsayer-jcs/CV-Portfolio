import subprocess
import sys
from datetime import time

import requests

## ------------------------- LAUNCH SERVER -------------------------------- ##
print("Setting up server")

subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)

subprocess.run(
    [".venv/Scripts/python.exe", "-m", "pip", "install", "-r", "../qa_ecommerce_demo/requirements.txt"],
    check=True
)

subprocess.run(
    [".venv/Scripts/python.exe", "../qa_ecommerce_demo/seed.py"],
    check=True
)

server = subprocess.Popen(
    [
        "..\\qa_ecommerce_demo\\.venv\\Scripts\\python.exe",
        "..\\qa_ecommerce_demo\\run.py"
    ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

## ------------------------------ WAIT FOR SERVER TO BE READY -------------------------------- ##
print("Waiting for server to be live")

BASE_URL = "http://localhost:5000"

def wait_for_server(timeout=30):
    counter = 0

    while counter < timeout:
        try:
            response = requests.get(BASE_URL)

            if response.status_code < 500:
                print("Server is ready!")
                return True

        except requests.ConnectionError:
            pass

        print("Waiting for server...")
        time.sleep(1)
        counter += 1

    return False

if wait_for_server():
    print("Run the tests!")
else:
    print("Server failed to start.")

## ------------------------------- RUN PYTESTS --------------------------------------- ##
print("Running tests")

api_result = subprocess.run(
    [sys.executable, "-m", "pytest"]
)

## --------------------------------- END SERVER -------------------------------------- ##
print("Stopping Flask server...")

subprocess.run(
    ["taskkill", "/F", "/T", "/PID", str(server.pid)],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

server.wait()

print("Flask server stopped.")