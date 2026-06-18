import logging
import subprocess
from concurrent.futures import ThreadPoolExecutor


def host_discovery():
    live_hosts = []

    network_prefix = input(
        "Enter network prefix (e.g. 192.168.0): "
    )

    logging.info(f"Host discovery started for {network_prefix}.0/24")

    print(
        f"\nDiscovering live hosts on "
        f"{network_prefix}.0/24...\n"
    )

    def ping_host(host_number):
        ip_address = f"{network_prefix}.{host_number}"

        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", ip_address],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if result.returncode == 0:
            live_hosts.append(ip_address)

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(ping_host, range(1, 255))

    print("Live Hosts Found:\n")

    for host in sorted(live_hosts):
        print(host)

    logging.info(
        f"Host discovery completed for {network_prefix}.0/24 - "
        f"{len(live_hosts)} live hosts found"
    )

    print("\nHost discovery complete.")