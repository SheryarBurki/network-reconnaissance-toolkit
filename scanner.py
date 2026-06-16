import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

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

results = []

scan_time = datetime.now()

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

        banner = grab_banner(target, port)

        results.append({
            "port": port,
            "service": service,
            "banner": banner
        })

    scanner.close()

with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scan_port, range(start_port, end_port + 1))

print("\nScan Results:\n")

for result in sorted(results, key=lambda x: x["port"]):
    print(f"Port {result['port']} is open ({result['service']})")

    if result["banner"]:
        print(f"  Banner: {result['banner']}")

with open("scan_results.txt", "w") as report:

    report.write("=====================================\n")
    report.write("NETWORK RECONNAISSANCE REPORT\n")
    report.write("=====================================\n\n")

    report.write(f"Target: {target}\n")
    report.write(f"Scan Time: {scan_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.write(f"Port Range: {start_port}-{end_port}\n\n")

    for result in sorted(results, key=lambda x: x["port"]):

        report.write(
            f"Port {result['port']} Open ({result['service']})\n"
        )

        if result["banner"]:
            report.write(
                f"Banner: {result['banner']}\n"
            )

        report.write("\n")

print("\nReport saved to scan_results.txt")

print("\nScan complete.")