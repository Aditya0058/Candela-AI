import subprocess
import os
import time
import webbrowser
import sys

color='\033[0;33m' # yellow
NC='\033[0m' # no color

def start_servers():
    print(f"{color}Starting candela frontend and backend servers please wait ....{NC}")
    backend_process = subprocess.Popen(
        [sys.executable, "app.py"], 
        cwd="Backend"
    )
    frontend_process = subprocess.Popen(
        "npm run dev",
        cwd="Frontend",
        shell=True 
    )
    print("Waiting for servers to boot up...")
    time.sleep(8) 

    print(f"{color}Opening Candela in your browser cuz i am not lazyy{NC}")
    webbrowser.open("http://localhost:5173")

    print(f"{color}\nFinally, Candela is running! Press Ctrl+C to stop.{NC}")

    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\n Shutting down Candela...")
        backend_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    start_servers()