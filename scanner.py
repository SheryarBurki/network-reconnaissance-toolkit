import socket
from concurrent.futures import ThreadPoolExecutor

COMMON_SERVICES = {
    21: "FTP",
    22: "SSH",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Alt"
}

target = input("Enter target IP or hostname: ")

try:
    socket.gethostbyname(target)
except socket.gaierror:
    print("Invalid hostname or IP address.")
    exit()

try:
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))
except ValueError:
    print("Ports must be numbers.")
    exit()

if start_port < 1 or end_port > 65535:
    print("Ports must be between 1 and 65535.")
    exit()

if start_port > end_port:
    print("Start port must be less than or equal to end port.")
    exit()

print(f"\nScanning target: {target}")
print(f"Port range: {start_port}-{end_port}\n")

def grab_banner(target, port):
    try:
        banner_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        banner_socket.settimeout(2)
        banner_socket.connect((target, port))

        if port in [80, 8080]:
            banner_socket.send(
                b"HEAD / HTTP/1.1\r\nHost: "
                + target.encode()
                + b"\r\n\r\n"
            )

        banner = banner_socket.recv(1024).decode(errors="ignore").strip()

        banner_socket.close()

        if banner:
            return banner

    except:
        return None

def scan_port(port):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(1)

    result = scanner.connect_ex((target, port))

    if result == 0:
        service = COMMON_SERVICES.get(port, "Unknown Service")
        print(f"Port {port} is open ({service})")

        banner = grab_banner(target, port)

        if banner:
            print(f"  Banner: {banner}")

    scanner.close()

with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scan_port, range(start_port, end_port + 1))

print("\nScan complete.")