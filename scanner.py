import json
import logging
import re
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

        banner = banner_socket.recv(1024).decode(
            errors="ignore"
        ).strip()

        banner_socket.close()

        if banner:
            return banner

    except Exception:
        return None
    
def parse_banner(banner):
    if not banner:
        return {
            "product": None,
            "version": None
        }

    patterns = [
        (r"OpenSSH[_/](\S+)", "OpenSSH"),
        (r"Apache/(\S+)", "Apache"),
        (r"nginx/(\S+)", "nginx"),
        (r"Microsoft-IIS/(\S+)", "Microsoft IIS"),
        (r"SimpleHTTP/(\S+)", "SimpleHTTP"),
        (r"MySQL\s+(\S+)", "MySQL"),
        (r"vsftpd\s+(\S+)", "vsftpd"),
        (r"ProFTPD\s+(\S+)", "ProFTPD")
    ]

    for pattern, product in patterns:
        match = re.search(
            pattern,
            banner,
            re.IGNORECASE
        )

        if match:
            return {
                "product": product,
                "version": match.group(1)
            }

    return {
        "product": None,
        "version": None
    }

def port_scan():
    results = []
    scan_time = datetime.now()

    target = input(
        "Enter target IP or hostname: "
    )

    try:
        socket.gethostbyname(target)
    except socket.gaierror:
        print("Invalid hostname or IP address.")
        return

    try:
        start_port = int(
            input("Enter start port: ")
        )

        end_port = int(
            input("Enter end port: ")
        )

    except ValueError:
        print("Ports must be numbers.")
        return

    if start_port < 1 or end_port > 65535:
        print(
            "Ports must be between 1 and 65535."
        )
        return

    if start_port > end_port:
        print(
            "Start port must be less than "
            "or equal to end port."
        )
        return

    logging.info(
        f"Port scan started - target: {target}, "
        f"port range: {start_port}-{end_port}"
    )

    print(f"\nScanning target: {target}")
    print(
        f"Port range: {start_port}-{end_port}\n"
    )

    def scan_port(port):
        scanner = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        scanner.settimeout(1)

        result = scanner.connect_ex(
            (target, port)
        )

        if result == 0:
            service = COMMON_SERVICES.get(
                port,
                "Unknown Service"
            )

            banner = grab_banner(
                target,
                port
            )

            parsed_banner = parse_banner(banner)

            results.append({
                "port": port,
                "service": service,
                "product": parsed_banner["product"],
                "version": parsed_banner["version"],
                "banner": banner
                })

            logging.info(
                f"Open port found - "
                f"{target}:{port} "
                f"({service})"
            )

        scanner.close()

    with ThreadPoolExecutor(
        max_workers=100
    ) as executor:

        executor.map(
            scan_port,
            range(
                start_port,
                end_port + 1
            )
        )

    print("\nScan Results:\n")

    for result in sorted(
        results,
        key=lambda x: x["port"]
    ):

        print(
            f"Port {result['port']} "
            f"is open "
            f"({result['service']})"
        )

        if result["banner"]:
            print(
                f"  Banner: "
                f"{result['banner']}"
            )

    with open(
        "scan_results.txt",
        "w"
    ) as report:

        report.write(
            "=====================================\n"
        )

        report.write(
            "NETWORK RECONNAISSANCE REPORT\n"
        )

        report.write(
            "=====================================\n\n"
        )

        report.write(
            f"Target: {target}\n"
        )

        report.write(
            f"Scan Time: "
            f"{scan_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )

        report.write(
            f"Port Range: "
            f"{start_port}-{end_port}\n\n"
        )

        for result in sorted(
            results,
            key=lambda x: x["port"]
        ):

            report.write(
                f"Port {result['port']} "
                f"Open "
                f"({result['service']})\n"
            )

            if result["banner"]:
                report.write(
                    f"Banner: "
                    f"{result['banner']}\n"
                )

            report.write("\n")

    json_report = {
        "target": target,
        "scan_time": scan_time.strftime("%Y-%m-%d %H:%M:%S"),
        "port_range": {
            "start": start_port,
            "end": end_port
        },
        "open_ports_found": len(results),
        "results": sorted(results, key=lambda x: x["port"])
    }

    with open("scan_results.json", "w") as json_file:
        json.dump(
            json_report,
            json_file,
            indent=4
        )
    
    logging.info(
        "Report saved to scan_results.txt"
    )

    logging.info(
        "JSON report saved to scan_results.json"
    )

    logging.info(
        f"Port scan completed - "
        f"target: {target}, "
        f"{len(results)} open ports found"
    )

    print(
        "\nReport saved to scan_results.txt"
    )

    print(
        "JSON report saved to scan_results.json"
    )

    print("\nScan complete.")


if __name__ == "__main__":
    port_scan()