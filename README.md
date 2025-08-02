# SQL Injection Detection Tool

This project is a SQL Injection Detection Tool implemented in Python. It scans a given URL for potential SQL injection vulnerabilities by injecting common SQL payloads into query parameters and analyzing the responses for SQL error patterns.

## Project Structure

```
SQLInjectionScanner
├── scanner.py          # Main logic for the SQL Injection Detection Tool
├── requirements.txt    # Dependencies required for the project
└── README.md           # Documentation for the project
```

## Installation

To get started, clone the repository and navigate into the project directory:

```bash
git clone <repository-url>
cd SQLInjectionScanner
```

Next, install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

To run the SQL Injection Scanner, execute the following command:

```bash
python scanner.py
```

You will be prompted to enter the target URL with GET parameters (e.g., `http://testphp.vulnweb.com/page.php?id=1`).

## Example

1. Start the scanner:
   ```bash
   python scanner.py
   ```

2. Input a URL when prompted:
   ```
   Enter the target URL: http://testphp.vulnweb.com/page.php?id=1
   ```

3. The scanner will test various SQL payloads and report any potential vulnerabilities based on the responses received.

## Dependencies

This project requires the following Python packages:

- `requests`: For making HTTP requests.
- `colorama`: For colored terminal output (optional).

You can install these dependencies using the `requirements.txt` file provided.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.