#!/usr/bin/env python3
"""
Advanced Honeypot and Attack Analysis System
----------------------------------------------
Features:
- Simulates a vulnerable SSH service (fake banner) to lure attackers.
- Logs all attacker interactions with timestamps and session details.
- Supports multi-threaded handling of multiple concurrent connections.
- Designed for forensic analysis of attacker behavior.

Usage (requires root privileges):
  sudo python advanced_honeypot.py --port 2222
"""

import socket, threading, argparse, time, logging

# Configure logging with file output.
logging.basicConfig(filename="advanced_honeypot.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def handle_client(conn, addr):
    """
    Handles incoming connection, simulating an SSH banner and logging received data.
    """
    logging.info(f"Connection from {addr}")
    try:
        # Simulate SSH banner
        conn.sendall(b"SSH-2.0-OpenSSH_7.4\r\n")
        data = conn.recv(1024)
        log_entry = f"{time.ctime()} - {addr} sent: {data.decode(errors='ignore')}\n"
        with open("advanced_honeypot.log", "a") as f:
            f.write(log_entry)
    except Exception as e:
        logging.error(f"Error handling client {addr}: {e}")
    finally:
        conn.close()

def start_honeypot(port):
    """
    Starts the honeypot on the specified port.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", port))
    s.listen(5)
    print(f"Advanced Honeypot listening on port {port}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

def main_honeypot():
    parser = argparse.ArgumentParser(description="Advanced Honeypot and Attack Analysis System")
    parser.add_argument("--port", type=int, default=2222, help="Port for honeypot (default: 2222)")
    args = parser.parse_args()
    start_honeypot(args.port)

if __name__ == "__main__":
    main_honeypot()
