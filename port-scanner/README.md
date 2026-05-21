# Port Scanner

A series of progressively more capable TCP port scanners built from scratch in Python. This project was created for educational purposes — to understand how port scanning works at the socket level, not to replace tools like Nmap.

---

## Why Build a Port Scanner From Scratch?

Tools like Nmap abstract away all the underlying mechanics. Building one manually forces you to understand:
- How TCP connections are established (and what "open" actually means)
- How sockets work at the code level
- Why timeout values matter
- How CLI tools are structured with argument parsing

---

## Project Structure

```
port-scanner/
├── port-scanner1/    # Basic scanner — fixed range, hardcoded target
├── port-scanner2/    # CLI arguments via argparse
└── port-scanner3/    # Custom port range + scan timer
```

---

## port-scanner1 — Basic Scanner

The simplest possible implementation. Scans ports 1–100 on a hardcoded target using raw TCP sockets.

**Concepts introduced:**
- `socket.AF_INET` — IPv4 addressing
- `socket.SOCK_STREAM` — TCP (connection-based) vs UDP
- `connect_ex()` — returns `0` if port is open, error code otherwise
- `settimeout()` — prevents the script from hanging on filtered ports

```python
import socket

target = input("Enter target IP: ")
print(f"\nScanning target: {target}\n")

for port in range(1, 101):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((target, port))
    if result == 0:
        print(f"[OPEN] Port {port}")
    sock.close()
```

**Limitation:** Target and port range are fixed — no flexibility from the command line.

---

## port-scanner2 — CLI Arguments (argparse)

Adds `argparse` so the target IP is passed as a command-line argument instead of typed interactively.

**Concepts introduced:**
- `argparse` — standard Python library for building CLI tools
- Positional arguments vs flags

```bash
python scanner.py 192.168.1.1
```

```python
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
```

**Limitation:** Port range is still hardcoded to 1–100.

---

## port-scanner3 — Custom Port Range + Scan Timer

Adds `--start` and `--end` flags so the user can define any port range. Also measures and displays total scan time.

**Concepts introduced:**
- Optional arguments with default values (`--start`, `--end`)
- `datetime` module for timing
- Graceful error handling (`KeyboardInterrupt`, `socket.gaierror`)

```bash
python scanner.py 192.168.1.1 --start 1 --end 1024
```

```python
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
```

---

## Test Results

All scanners were tested in a local virtual machine environment:

- **Attacker:** Kali Linux VM
- **Target 1:** Ubuntu Server VM (`192.168.18.32`)
- **Target 2:** Windows 11 host machine

### Ubuntu Server — scanner1
```
$ python3 scanner.py
Enter target IP: 192.168.18.32

Scanning target: 192.168.18.32
[OPEN] Port 22
```

### Ubuntu Server — scanner2
```
$ python3 scanner2.py 192.168.18.32

Scanning target: 192.168.18.32
[OPEN] Port 22
```

### Ubuntu Server — scanner3 (ports 1–1024)
```
$ python3 scanner3.py 192.168.18.32 --start 1 --end 1024

Scanning target: 192.168.18.32
Port range: 1 – 1024
Started at: 2026-05-21 07:55:06.574298
[OPEN] Port 22

Scan completed in: 0:00:00.570998
```

**Result:** Only port 22 (SSH) is open on the Ubuntu Server. Scan of 1024 ports completed in **0.57 seconds**.

---

## Key Finding — Why Ubuntu Was Fast and Windows Was Slow

Scanning the same port range against the Windows 11 host took approximately **2 minutes** compared to under 1 second for Ubuntu Server. This reveals a fundamental concept in network scanning:

| Port state | What the target sends back | Scanner response time |
|---|---|---|
| **Open** | `TCP SYN-ACK` | Immediate |
| **Closed** | `TCP RST` (reset) | Immediate |
| **Filtered** (firewall DROP) | Nothing | Waits for full timeout |

**Ubuntu Server** responds to closed ports with an immediate `TCP RST` — the scanner gets a response right away and moves on. With `settimeout(1)`, a 1024-port scan takes under a second.

**Windows 11 Firewall** silently drops packets on most ports instead of sending `RST`. The scanner gets no response and must wait the full 1-second timeout per port:

```
1024 ports × 1 second timeout = ~17 minutes worst case
```


**This is exactly why tools like Nmap use flags such as `-T4`, `-T5`, and `--min-rate`** — to aggressively reduce timeouts when scanning targets with firewalls, where waiting the full timeout on every filtered port would make scans impractically slow.

---

## What's Next

- [ ] **Threading** — scanning ports concurrently instead of one by one (massively faster)
- [ ] **Banner grabbing** — reading the service response to identify what's running on an open port
- [ ] **Output to file** — saving results to `.txt` or `.json`
- [ ] **UDP scanning** — understanding why UDP scanning is fundamentally different from TCP

---

## Disclaimer

This tool is for educational use only. Only scan systems you own or have explicit permission to test.