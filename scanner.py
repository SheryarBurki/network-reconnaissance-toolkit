import socket
from concurrent.futures import ThreadPoolExecutor

target = input("Enter target IP or hostname: ")

start_port = int(input("Enter start port: "))
end_port = int(input("Enter end port: "))

print(f"\nScanning target: {target}")
print(f"Port range: {start_port}-{end_port}\n")


def scan_port(port):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(1)

    result = scanner.connect_ex((target, port))

    if result == 0:
        print(f"Port {port} is open")

    scanner.close()


with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scan_port, range(start_port, end_port + 1))

print("\nScan complete.")