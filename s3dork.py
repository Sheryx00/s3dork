import os
import time
import argparse
import requests
from googlesearch import search

def google_dork_search(company):
    dork = (
        f'site:.s3.amazonaws.com OR site:.blob.core.windows.net OR '
        f'site:.storage.googleapis.com OR site:.r2.cloudflarestorage.com OR '
        f'site:.r2.dev "{company}"'
    )
    print(f"Searching for: {dork}")
    return search(dork)

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
        print(f"Failed to download {url}: {e}")

def log_urls(urls, output_folder):
    log_file = os.path.join(output_folder, "s3dork.log")
    with open(log_file, "w") as f:
        f.writelines(url + "\n" for url in urls)
    print(f"Logged URLs to: {log_file}")

def main():
    parser = argparse.ArgumentParser(description="Google Dork Search and File Downloader")
    parser.add_argument("-t", "--target", type=str, required=True, help="Target company name to search for")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output folder to save files or logs")
    parser.add_argument("-d", "--delay", type=float, default=2.0, help="Delay (in seconds) between processing each result")
    parser.add_argument("-q", "--no-quiet", action="store_true", help="Download files instead of listing URLs")
    args = parser.parse_args()

    # Perform the Google Dork search
    urls = google_dork_search(args.target)

    # Log all URLs to a file
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    log_urls(urls, args.output)

    # If --no-quiet is not set, just list the URLs
    if not args.no_quiet:
        print("\nQuiet mode enabled by default. Links found:")
        for url in urls:
            print(url)
        print("\nNo files were downloaded.")
        return

    # If --no-quiet is set, download files
    for url in urls:
        print(f"Processing: {url}")
        download_file(url, args.output)
        print(f"Sleeping for {args.delay} seconds...")
        time.sleep(args.delay)

if __name__ == "__main__":
    main()