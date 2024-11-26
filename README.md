**s3dork** is a simple Python tool to search and download publicly accessible files using Google Dorks. It supports customizable delays, logging, and an option to list URLs without downloading.

## Features

* Perform Google Dork searches for cloud storage services (e.g., AWS S3, Azure Blob).
Download files found during the search.
* Log all discovered URLs to a urls.log file.
* Quiet mode to list URLs without downloading.

## Installation

Clone this repository.

```bash
git clone https://github.com/sheryx00/s3dork.git
```

## Usage

Search Download

```bash
python3 s3dork.py -t "example_company" -o ./downloads --d 3
```

Quiet Mode (List URLs Only)

```bash
python3 s3dork.py -t "target_company" -o /path/to/output/folder --quiet
```

## Help

```bash
-t, --target: Target company name (required).
-o, --output: Folder to save downloaded files (required).
-d, --delay: Delay between processing results (default: 2 seconds).
-q, --quiet: List URLs only, skip downloading.
```

## Support

Support the creator to keep sharing new tools:

<a href="https://www.buymeacoffee.com/Sheryx00" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
