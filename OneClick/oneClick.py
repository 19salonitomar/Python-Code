import psutil
import subprocess

def close_applications():
    # Get the list of running processes
    running_processes = [proc.name() for proc in psutil.process_iter()]

    # Terminate each running process
    for proc in psutil.process_iter():
        proc.terminate()

    # Wait for the processes to terminate
    psutil.wait_procs(psutil.process_iter())

    print("All applications closed.")

def shut_down():
    # Shut down the computer
    subprocess.call(["shutdown", "/s", "/t", "0"])

# Closing applications
close_applications()

# Shutting down the computer
shut_down()
