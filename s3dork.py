import os
import time
import argparse
import requests
import random
import re

# Colors
BLUE = "\33[94m"
RED = "\33[91m"
END = "\033[0m"

# List of some common User-Agent strings to randomize
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:25.0) Gecko/20100101 Firefox/25.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 Edge/14.14393',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
]

def banner():
    banner = f"""
    {BLUE}
     _____     _            _    
 ___|___ /  __| | ___   ___| | __
/ __| |_ \ / _` |/ _ \ / __| |/ /
\__ \___) | (_| | (_) | (__|   < 
|___/____/ \__,_|\___/ \___|_|\_\
                                 

    {BLUE}Created by{END}: @Sheryx00
    {BLUE}Github{END}: https://github.com/Sheryx00/s3dock\n\n"""
    return banner

def google_dork_search(company):
    dork = (
        f'site:.s3.amazonaws.com OR site:.blob.core.windows.net OR '
        f'site:.storage.googleapis.com OR site:.r2.cloudflarestorage.com OR '
        f'site:.r2.dev "{company}"'
    )
    
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.google.com/',
    }

    # Send GET request to Google with headers
    search_url = f"https://www.google.com/search?q={dork}"
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()  # Will raise an HTTPError if the status code is 4xx or 5xx
    
    # Extract URLs from the response text using regular expressions
    urls = re.findall(r'href="(http[^"]+)"', response.text)
    
    # Filter out irrelevant links (we can refine this if needed)
    valid_urls = [url for url in urls if url.startswith('http')]
    
    return valid_urls

def download_file(url, output_folder):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Extract the filename from the URL
        filename = url.split("/")[-1] or "file_from_url"
        filepath = os.path.join(output_folder, filename)
        
        with open(filepath, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {filepath}")
    except requests.RequestException as e:
        print(f"{RED}Failed to download {url}: {e}{END}")

def log_urls(urls, output_folder):
    log_file = os.path.join(output_folder, "s3dork.log")
    with open(log_file, "w") as f:
        f.writelines(url + "\n" for url in urls)
    print(f"{BLUE}Logged URLs to: {log_file}{END}")

def main():
    parser = argparse.ArgumentParser(description="Google Dork Search and File Downloader")
    parser.add_argument("-t", "--target", type=str, required=True, help="Target company name to search for")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output folder to save files or logs")
    parser.add_argument("-d", "--delay", type=float, default=2.0, help="Delay (in seconds) between processing each result")
    parser.add_argument("-q", "--quiet", action="store_true", default=False, help="Do not download files, just list URLs")
    args = parser.parse_args()

    # Display banner
    print(banner())

    # Perform the Google Dork search and get the URLs as a list
    urls = google_dork_search(args.target)

    # Log all URLs to a file
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    log_urls(urls, args.output)

    # If --quiet is set, just list the URLs, otherwise download the files
    if args.quiet:
        print(f"{BLUE}\nQuiet mode enabled. Links found:{END}")
        for url in urls:
            print(url)
        print(f"{BLUE}\nNo files were downloaded.{END}")
    else:
        for url in urls:
            print(f"{BLUE}Processing: {url}{END}")  # Updated to blue
            download_file(url, args.output)
            time.sleep(args.delay)

if __name__ == "__main__":
    main()
