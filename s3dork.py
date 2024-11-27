import os
import time
import argparse
import requests
import re
import random
import mimetypes

# Storage sites list (no `site:` prefix for flexibility)
STORAGE_SITES = [
    "s3.amazonaws.com",
    "blob.core.windows.net",
    "storage.googleapis.com",
    "r2.cloudflarestorage.com",
    "r2.dev",
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    # Add more user agents if needed
]

BLUE = "\33[94m"
RED = "\33[91m"
END = "\033[0m"

def build_dork_query(company):
    """Constructs a Google dork search query using the storage sites."""
    sites_query = " OR ".join([f"site:{site}" for site in STORAGE_SITES])
    return f'{sites_query} "{company}"'

def is_valid_file_url(url):
    """
    Validates whether a URL points to a file hosted on one of the specified storage sites.
    """
    for site in STORAGE_SITES:
        if site in url:
            return True
    return False

def google_dork_search(company, max_pages=10):
    """
    Performs a Google dork search for the given company across all specified storage sites.
    """
    dork = build_dork_query(company)
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.google.com/",
    }

    print(f"{BLUE}Searching for: {dork}{END}")
    all_urls = []

    for page in range(max_pages):
        start = page * 10
        search_url = f"https://www.google.com/search?q={dork}&start={start}"

        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()

            # Extract URLs using regex
            urls = re.findall(r'href="(http[^"]+)"', response.text)
            valid_urls = [url for url in urls if url.startswith("http")]

            if not valid_urls:
                print(f"{BLUE}No more results found after {page + 1} pages.{END}")
                break

            all_urls.extend(valid_urls)
            print(f"{BLUE}Page {page + 1}: {len(valid_urls)} results found.{END}")
            time.sleep(random.uniform(2.0, 4.0))  # Random delay to avoid being blocked

        except requests.RequestException as e:
            print(f"{RED}Failed to fetch page {page + 1}:{END}\n{e}")
            break

    return list(set(all_urls))  # Deduplicate URLs

def download_file(url, output_folder, extensions):
    """
    Downloads a file from the given URL and saves it in the specified output folder
    if it matches the desired extensions (or downloads all if extensions are None).
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Check the MIME type directly from the response headers
        mime_type = response.headers.get('Content-Type', '').split(';')[0]
        if not mime_type:
            print(f"{RED}Could not determine MIME type from headers:{END} {url}")
            return

        # Check if the MIME type matches allowed extensions
        if extensions:
            ext = mime_type.split("/")[-1]  # Extract extension from MIME type
            if ext not in extensions:
                print(f"{RED}Skipped (extension is not in whitelist) [{ext}]:{END} {url}")
                return

        # Temporary file download
        filename = url.split("/")[-1] or f"file.{mime_type.split('/')[-1] if mime_type else 'unknown'}"
        filepath = os.path.join(output_folder, filename)

        with open(filepath, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"{BLUE}Downloaded:{END} {filepath}")

    except requests.RequestException as e:
        print(f"{RED}Failed to download:{END} {url}\n{e}")
    except OSError as e:
        print(f"{RED}Error handling file:{END} {e}")

def log_urls(urls, output_folder):
    """
    Logs all found URLs to a file named `s3dork.log` in the specified output folder.
    """
    log_file = os.path.join(output_folder, "s3dork.log")
    with open(log_file, "w") as f:
        f.writelines(url + "\n" for url in urls)
    print(f"{BLUE}Logged URLs to:{END} {log_file}")

def banner():
    """
    Displays the script banner.
    """
    banner = f"""
     {BLUE}
     _____     _            _    
  ___|___ /  __| | ___   ___| | __
 / __| |_ \ / _` |/ _ \ / __| |/ /
 \__ \___) | (_| | (_) | (__|   < 
 |___/____/ \__,_|\___/ \___|_|\_\\
                                  
     {BLUE}Created by{END}: @Sheryx00
     {BLUE}Github{END}: https://github.com/Sheryx00/s3dork
    """
    print(banner)

def main():
    banner()

    parser = argparse.ArgumentParser(description="Google Dork Search and File Downloader")
    parser.add_argument("-t", "--target", type=str, required=True, help="Target company name to search for")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output folder to save files or logs")
    parser.add_argument("-d", "--delay", type=float, default=2.0, help="Delay (in seconds) between processing each result")
    parser.add_argument("-e", "--ext", type=str, help="Comma-separated list of allowed file extensions (e.g., pdf,jpg,txt)")
    parser.add_argument("-q", "--quiet", action="store_true", help="Only log URLs without downloading files")
    parser.add_argument("-x", "--extended", action="store_true", help="Include extended set of extensions (default 20 common extensions)")

    args = parser.parse_args()

    # Define the base extensions
    base_extensions = [
        "txt", "csv", "json", "xml", "xls", "xlsx", "pdf", "doc", "docx", "db",
        "env", "bak", "log", "sql", "key", "pem", "tar", "tar.gz", "zip", "backup",
    ]
    
    # If --extended flag is set, add the extended set of 20 file extensions
    if args.extended:
        extensions = base_extensions
    else:
        extensions = args.ext.split(",") if args.ext else None

    # Perform the Google Dork search
    urls = google_dork_search(args.target)

    # Log all URLs to a file
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    log_urls(urls, args.output)

    if args.quiet:
        print(f"{BLUE}Quiet mode enabled. URLs are logged but not downloaded.{END}")
        return

    # Process each URL
    for url in urls:
        if is_valid_file_url(url):
            print(f"{BLUE}Processing:{END} {url}")
            download_file(url, args.output, extensions)

if __name__ == "__main__":
    main()
