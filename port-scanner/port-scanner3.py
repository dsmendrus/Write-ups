import socket
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description="Simple TCP Port Scanner")
parser.add_argument("target", help="Target IP address")
parser.add_argument("--start", type=int, default=1, help="Start port (default: 1)")
parser.add_argument("--end", type=int, default=100, help="End port (default: 100)")
args = parser.parse_args()

target = args.target
start_port = args.start
end_port = args.end

print(f"\nScanning target: {target}")
print(f"Port range: {start_port} – {end_port}")
print(f"Started at: {datetime.now()}\n")

start_time = datetime.now()

try:
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"[OPEN] Port {port}")
        sock.close()

except KeyboardInterrupt:
    print("\n[!] Scan interrupted by user.")

except socket.gaierror:
    print("[!] Could not resolve hostname.")

finally:
    duration = datetime.now() - start_time
    print(f"\nScan completed in: {duration}")