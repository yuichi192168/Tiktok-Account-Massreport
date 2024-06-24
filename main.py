import ctypes, json, os, time, random, threading, re, sys
import httpx
import datetime
from pystyle import Write, System, Colorate, Colors
from colorama import Fore, Style, init
from tls_client import Session  # Adjusted import to use directly from tls_client

# Ensure correct colors for Termux (may need adjustments)
Fore.RED = '\033[91m'
Fore.YELLOW = '\033[93m'
Fore.GREEN = '\033[92m'
Fore.BLUE = '\033[94m'
Fore.LIGHTMAGENTA_EX = '\033[95m'
Fore.MAGENTA = '\033[95m'
Fore.LIGHTBLUE_EX = '\033[94m'
Fore.CYAN = '\033[96m'
Fore.LIGHTBLACK_EX = '\033[90m'
Fore.WHITE = '\033[97m'
Fore.RESET = '\033[0m'
Fore.LIGHTGREEN_EX = '\033[92m'

# Global variables
success = 0
failed = 0
total = 1

# Function to save proxies to file
def save_proxies(proxies):
    with open("proxies.txt", "w") as file:
        file.write("\n".join(proxies))

# Function to fetch proxies from API
def get_proxies():
    try:
        url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all"
        response = httpx.get(url, timeout=60)

        if response.status_code == 200:
            proxies = response.text.splitlines()
            save_proxies(proxies)
        else:
            time.sleep(1)
            get_proxies()
    except (httpx.RequestError, httpx.TimeoutException) as e:
        time.sleep(1)
        get_proxies()

# Function to check and fetch proxies if necessary
def check_proxies_file():
    file_path = "proxies.txt"
    if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
        get_proxies()

# Function to update console title with progress
def update_console_title():
    global success, failed, total
    success_rate = round(success / total * 100, 2)
    print(f'[ Tiktok MassReport ] Reports Sent: {success} ~ Failed: {failed} ~ Success Rate: {success_rate}%')

# Function to fetch current time
def get_time_rn():
    now = datetime.datetime.now()
    return now.strftime("%H:%M:%S")

# Function to perform mass reporting
def mass_report():
    global success, total, failed

    # Sample session initialization, adjust as per tls_client documentation
    session = Session(
        client_identifier="chrome_113",
        random_tls_extension_order=True
    )

    # Placeholder for proxy handling logic (to be adjusted)
    proxy_string = "http://your_proxy_here"

    session.proxies = {
        "http": proxy_string,
        "https": proxy_string
    }

    # Sample reporting logic, adjust as per your actual needs
    try:
        url = "https://api.example.com/report"
        response = session.get(url)

        if response.status_code == 200:
            success += 1
        else:
            failed += 1

    except Exception as e:
        failed += 1

    total += 1
    update_console_title()
    mass_report()

# Main execution
if __name__ == "__main__":
    try:
        with open("config.json") as f:
            data = json.load(f)
            if data.get("proxy_scraper", "").lower() in {"y", "yes"}:
                check_proxies_file()

        num_threads = data.get("threads", 1)

        # Launch threads for mass reporting
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=mass_report)
            thread.start()
            threads.append(thread)

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
