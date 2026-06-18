import logging
from host_discovery import host_discovery
from scanner import port_scan

logging.basicConfig(
    filename="toolkit.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def show_menu():
    print("\nNetwork Reconnaissance Toolkit")
    print("1. Host Discovery")
    print("2. Port Scan")
    print("3. Exit")


def main():
    logging.info("Toolkit started")

    while True:
        show_menu()
        choice = input("\nSelect an option: ")

        if choice == "1":
            logging.info("Host Discovery selected")
            host_discovery()

        elif choice == "2":
            logging.info("Port Scan selected")
            port_scan()

        elif choice == "3":
            print("\nExiting toolkit.")
            logging.info("Toolkit exited")
            break

        else:
            print("\nInvalid option. Please choose 1, 2, or 3.")
            logging.warning("Invalid menu option entered")


if __name__ == "__main__":
    main()