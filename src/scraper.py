import os
import argparse

from common.utils import get_logger
from common.utils import url_to_str
from common.utils import create_directory
from bs import scrape_root_url, dump_urls

logger = get_logger(__name__)


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Application to scrape the given URL")

    # Define the mutually exclusive group for the URL and urls-to-dump arguments
    group = parser.add_mutually_exclusive_group(required=True)

    # Define the mandatory URL argument
    group.add_argument("url", type=str, nargs="?", help="A URL string")

    # Define the new string argument for the urls-to-dump argument
    group.add_argument(
        "--urls-to-dump",
        type=str,
        help="A file name having all the url links needs to be saved as pdf",
    )

    # Define the optional boolean argument to start the app from reading URLs from files
    parser.add_argument(
        "--recovery-mode",
        action="store_true",
        help="Restart the app using the URLs dumped in the previous run",
    )

    # Define the optional boolean argument to run the app without dumping URLs as PDFs.
    # This will help us to prepare the list of all the URLs that need to be dumped.
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the app without dumping URLs as PDFs",
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    if args.urls_to_dump:
        # If the urls-to-dump argument is used, process it and skip the URL and other options
        urls_to_dump = args.urls_to_dump

        start_url = "https://docs.github.com"
        dir_name = url_to_str(start_url)  # Change this to the desired output directory
        create_directory(dir_name)

        logger.info(f"Starting downloading urls from '{urls_to_dump}' as pdfs")
        dump_urls(urls_to_dump, dir_name)
        logger.info(f"Finished downloading urls from '{urls_to_dump}' as pdfs")
    else:
        # Access the URL and boolean values
        start_url = args.url
        recovery_mode = args.recovery_mode
        dry_run = args.dry_run

        # Use the input arguments in your script
        print(f"URL: {start_url}")
        if recovery_mode:
            logger.info(
                f"Restarting the app by using the URLs saved in "
                f"'tovisit.txt' & 'touched_urls.txt' as input"
            )

        logger.info(f"Start URL: {start_url}")

        dir_name = url_to_str(start_url)
        create_directory(dir_name)

        logger.info(f"Starting scraping urls from '{start_url}'")
        scrape_root_url(
            start_url,
            dir_name,
            recovery_mode=recovery_mode,
            dry_run=dry_run,
        )
        logger.info(f"Finished scraping urls starting at '{start_url}'")


if __name__ == "__main__":
    main()
