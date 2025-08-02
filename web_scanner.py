from flask import Flask, render_template_string, request, send_from_directory
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

app = Flask(__name__)

@app.route('/image.png')
def logo():
    return send_from_directory('.', 'image.png')


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

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SQL Injection Scanner by A2V Digital</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            background-color: black;
            color: green;
        }

        .navbar {
            background-color: #226c8c;
            color: white;
            padding: 10px 20px;
            display: flex;
            align-items: center;
        }

        .navbar img {
            height: 40px;
            margin-right: 15px;
        }

        .navbar h1 {
            margin: 0;
            font-size: 20px;
        }

        .container {
            padding: 40px;
        }

        textarea {
            width: 100%;
            height: 300px;
            background-color: #111;
            color: green;
            border: 1px solid #444;
        }

        input, button {
            padding: 8px;
            font-size: 14px;
            color: green;
            margin-top: 10px;
            margin-bottom: 20px;
            background-color: #222;
            border: 1px solid #444;
        }

        .vuln { color: red; }
        .safe { color: green; }
        .warn { color: orange; }
    </style>
</head>
<body>

    <div class="navbar">
        <!-- Replace the src with your A2V Digital logo URL -->
        <img src="image.png" alt="A2V Digital Logo">
        <h1>A2V Digital</h1>
    </div>

    <div class="container">
        <h2>SQL Injection Scanner by A2V Digital</h2>
        <form method="post">
            Target URL: <input name="url" size="60" required>
            <br>
            <button type="submit">Scan</button>
        </form>

        {% if results %}
        <h3>Results:</h3>
        <textarea readonly>{% for line in results %}{{line}}
{% endfor %}</textarea>
        {% endif %}
    </div>

</body>
</html>

"""

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

def scan_url(url):
    results = []
    params = get_params(url)
    if not params:
        results.append("[!] No query parameters found in the URL.")
        return results

    for param in params:
        for payload in payloads:
            test_url = inject_payload(url, param, payload)
            results.append(f"Testing {param} with payload {repr(payload)}... ")
            try:
                resp = requests.get(test_url, timeout=7)
                error = check_sql_error(resp.text)
                if error:
                    results.append(f"VULNERABLE! ({error})")
                else:
                    results.append("No error detected.")
            except requests.RequestException as e:
                results.append(f"Request failed: {e}")
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method == 'POST':
        url = request.form['url'].strip()
        if not url.startswith("http"):
            results = ["[!] Please enter a valid http/https URL."]
        else:
            results = scan_url(url)
    return render_template_string(HTML, results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)