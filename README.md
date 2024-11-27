# **s3dork**

**s3dork** is a simple Python tool to search and download publicly accessible files using Google Dorks. It supports customizable delays, logging, quiet mode, and an extended list of file extensions for filtering results.

## Features

- Perform Google Dork searches for cloud storage services (e.g., AWS S3, Azure Blob, Google Cloud Storage).
- Download files found during the search, with optional filtering by file extension.
- Log all discovered URLs to a `urls.log` file.
- Quiet mode to list URLs without downloading.
- **Extended file extension support** with the `-x` flag to automatically include a list of common extensions (e.g., `.txt`, `.pdf`, `.csv`, `.sql`, etc.).

## Installation

Clone this repository.

```bash
git clone https://github.com/sheryx00/s3dork.git
```

## Usage

### Search Download

```bash
python3 s3dork.py -t "example_company" -o ./downloads --d 3
```

### Quiet Mode (List URLs Only)

```bash
python3 s3dork.py -t "target_company" -o /path/to/output/folder -q
```

### Extended File Extensions (Use default 20 extensions)

```bash
python3 s3dork.py -t "target_company" -o /path/to/output/folder --extended
```

## Help

```bash
-t, --target: Target company name (required).
-o, --output: Folder to save downloaded files or logs (required).
-d, --delay: Delay (in seconds) between processing each result (default: 2 seconds).
-q, --quiet: List URLs only, skip downloading.
-e, --ext: Comma-separated list of allowed file extensions (e.g., pdf,jpg,txt).
-x, --extended: Include the extended set of 20 common file extensions (e.g., pdf, csv, sql, txt, docx, etc.).
```

## Support

Support the creator to keep sharing new tools: <a href="https://www.buymeacoffee.com/Sheryx00" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
