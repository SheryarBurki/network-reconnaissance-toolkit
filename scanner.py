import socket

target = input("Enter target IP or hostname: ")

start_port = int(input("Enter start port: "))
end_port = int(input("Enter end port: "))

print(f"\nScanning target: {target}")
print(f"Port range: {start_port}-{end_port}\n")

for port in range(start_port, end_port + 1):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(1)

    result = scanner.connect_ex((target, port))

    if result == 0:
        print(f"Port {port} is open")

    scanner.close()

print("\nScan complete.")