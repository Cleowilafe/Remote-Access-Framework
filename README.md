# Remote-Access-Framework

## truss.py

### Description

The `truss.py` is a Python script that implements a reverse shell, allowing remote access to the victim's system. The script uses sockets to connect to a specified IP address and port, providing functionalities such as camera video capture, keylogging, file reading, and command execution.

### Features

- **Remote Connection**: Connects to a defined IP and port for communication with the attacker.
- **Video Capture**: Allows the attacker to access the victim's camera through the `showcam` command.
- **Keylogger**: Logs keystrokes and saves the information to a `logs.txt` file, activated by the `keylogger` command.
- **File Reading**: The `cat <filename>` command allows the attacker to read the contents of text files on the victim's machine.
- **Command Execution**: Executes system commands and returns the output to the attacker.
- **Log Sending**: The `getlogs` command sends the contents of the log file to the attacker.

### Requirements

- Python 3.x
- Libraries:
  - `socket`
  - `subprocess`
  - `pynput`
  - `cv2` (OpenCV)
  - `threading`
  - `time`

### Usage

1. **Configuration**:
   - Open the `truss.py` script in a text editor.
   - Locate the variables `RHOST` and `RPORT` at the top of the script. 
   - Set `RHOST` to the IP address of the attacker's machine (e.g., `RHOST = '192.168.1.10'`).
   - Set `RPORT` to the port number that will be used for the connection (e.g., `RPORT = 4444`).

2. **Execution**:
   - Open a terminal on the victim's machine.
   - Navigate to the directory where `truss.py` is located using the `cd` command:
     ```bash
     cd /path/to/directory
     ```
   - Run the script using Python:
     ```bash
     python truss.py
     ```
   - Ensure that the attacker's listener is set up to accept incoming connections on the specified port.

3. **Setting Up the Listener** (on the attacker's machine):
   - Open a terminal and run a listener program (e.g., using `netcat`):
     ```bash
     nc -lvnp 4444
     ```
   - Replace `4444` with the same port number used in the `RPORT` variable.

4. **Using Commands**:
   - Once the connection is established, you can input commands directly into the listener terminal:
     - Use `showcam` to access the victim's camera feed.
     - Use `keylogger` to start logging keystrokes.
     - Use `getlogs` to retrieve the log file content.
     - Use `cat <filename>` to read specific files on the victim's machine.
     - Use `exit` to close the connection.
### Available Commands

- `showcam`: Captures and displays the camera feed.
- `keylogger`: Starts logging keystrokes.
- `getlogs`: Sends the log file content to the attacker.
- `cat <filename>`: Reads and sends the specified file's content.
- `exit`: Terminates the connection.

### Legal Considerations

This script should only be used in controlled environments and with explicit permission. Unauthorized use of remote access tools can result in serious legal consequences.
