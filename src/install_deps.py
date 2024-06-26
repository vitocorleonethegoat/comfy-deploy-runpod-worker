import json
import requests
import time
import subprocess

import torch

print("Torch version:",torch.__version__)
print("Is CUDA enabled?",torch.cuda.is_available())

command = ["python3", "/comfyui/main.py", "--disable-auto-launch", "--disable-metadata", "--cpu"]
# Start the server
server_process = subprocess.Popen(command)

def check_server(url, retries=50, delay=500):
    for i in range(retries):
        try:
            response = requests.head(url)

            # If the response status code is 200, the server is up and running
            if response.status_code == 200:
                print(f"builder - API is reachable")
                return True
        except requests.RequestException as e:
            # If an exception occurs, the server may not be ready
            pass

        # Wait for the specified delay before retrying
        time.sleep(delay / 1000)

    print(
        f"builder- Failed to connect to server at {url} after {retries} attempts."
    )
    return False

check_server("http://127.0.0.1:8188")

url = "http://127.0.0.1:8188/customnode/install"
headers = {"Content-Type": "application/json"}

# Load JSON array from deps.json
with open('deps.json') as f:
    packages = json.load(f)

# Make a POST request for each package
for package in packages:
    response = requests.request("POST", url, json=package, headers=headers)
    print(response.text)

# Close the server
server_process.terminate()
print("Finished installing dependencies.")