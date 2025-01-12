import psutil
import subprocess

def close_applications():
    # Get the list of running processes
    running_processes = [proc for proc in psutil.process_iter() if proc.pid != 0]

    # Terminate each running process
    for proc in running_processes:
        try:
            proc.terminate()
        except psutil.AccessDenied:
            # Skip terminating processes with insufficient permissions
            pass

    # Wait for the processes to terminate
    psutil.wait_procs(running_processes)

    print("All applications closed.")

def shut_down():
    # Shut down the computer
    subprocess.call(["shutdown", "/s", "/t", "0"])

# Closing applications
close_applications()

# Shutting down the computer
shut_down()
