# Port Scanner
This project was created for educational purposes to better understand how TCP port scanning works under the hood.
# Overall
In this project we will focus on creating a script to scan ports. Not to replace already made tools for scanning network like nmap, but to better understand how things work. 
I wanted to learn the mechanisms of network scanning and working with sockets.
And we can easily automatize this tasks.
# Egzample 2
[`port-scanner1/`](./port-scanner1.py)
In first project i bulid easy port scanner whose job is only to scan first 100 ports.
We imported socket library and created an object sock with parameters IPv4 and TCP. So we can use this object to scan our target `sock.connect_ex((target, port))` using our target ip and port range.
We also did a timeout so our scirpt won't stop for too much time.
# Example 2
[`port-scanner2/`](./port-scanner2.py)
In this second we added a arpparse for better development