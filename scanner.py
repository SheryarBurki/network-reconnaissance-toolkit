import socket

target = input("Enter target IP: ")
ports = [22, 80, 443, 3306, 8080]

print(f"Scanning target: {target}")

for port in ports:
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(1)

    result = scanner.connect_ex((target, port))

    if result == 0:
        print(f"Port {port} is open")
    else:
        print(f"Port {port} is closed or filtered")

    scanner.close()