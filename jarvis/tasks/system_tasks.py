import datetime
import os
import subprocess
import platform

def get_time():
    """Returns the current time as a string."""
    return datetime.datetime.now().strftime("%I:%M %p")

def get_date():
    """Returns the current date as a string."""
    return datetime.datetime.now().strftime("%A, %B %d, %Y")

def convert_time(value, unit_from, unit_to):
    """
    Converts time units.
    Supported: seconds, minutes, hours
    """
    value = float(value)
    # Convert everything to seconds first
    seconds = 0
    if unit_from == 'seconds':
        seconds = value
    elif unit_from == 'minutes':
        seconds = value * 60
    elif unit_from == 'hours':
        seconds = value * 3600
    
    # Convert to target
    result = 0
    if unit_to == 'seconds':
        result = seconds
    elif unit_to == 'minutes':
        result = seconds / 60
    elif unit_to == 'hours':
        result = seconds / 3600
        
    return f"{value} {unit_from} is {result:.2f} {unit_to}"

def system_power_control(action):
    """
    Handles system shutdown, restart, logout.
    Requires user confirmation in the main loop before calling.
    """
    system = platform.system()
    
    if system == "Windows":
        if action == "shutdown":
            os.system("shutdown /s /t 10")
            return "Shutting down system in 10 seconds."
        elif action == "restart":
            os.system("shutdown /r /t 10")
            return "Restarting system in 10 seconds."
        elif action == "logout":
            os.system("shutdown /l")
            return "Logging out..."
    else:
        return "Power control only supported on Windows for this demo."
    return "Invalid power command."

def execute_system_command(command_name):
    """
    Executes a system command based on the name.
    """
    command_name = command_name.lower()
    
    try:
        if "notepad" in command_name:
            subprocess.Popen(['notepad.exe'])
            return "Opening Notepad"
        elif "calculator" in command_name or "calc" in command_name:
            subprocess.Popen(['calc.exe'])
            return "Opening Calculator"
        elif "cmd" in command_name or "terminal" in command_name:
            subprocess.Popen(['start', 'cmd'], shell=True)
            return "Opening Command Prompt"
        else:
            return "System command not recognized"
    except Exception as e:
        return f"Error executing command: {e}"
