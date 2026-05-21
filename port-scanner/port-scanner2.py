import socket
import argparse

parser = argparse.ArgumentParser(description="Simple TCP Port Scanner")
parser.add_argument("target", help="Target IP address")

args = parser.parse_args()

target = args.target

print(f"\nScanning target: {target}\n")

for port in range(1, 101):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    result = sock.connect_ex((target, port))

    if result == 0:
        print(f"[OPEN] Port {port}")

    sock.close()