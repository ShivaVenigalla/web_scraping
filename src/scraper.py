import argparse

from common.utils import get_logger
from common.utils import url_to_str
from common.utils import create_directory
from bs import scrape_root_url

logger = get_logger(__name__)


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Application to scrape the given URL")

    # Define the mandatory URL argument
    parser.add_argument("url", type=str, help="A URL string")

    # Define the optional boolean argument to start the app from reading urls from files
    parser.add_argument(
        "--recovery-mode",
        action="store_true",
        help="Restart the app using the urls dumped in the previous run",
    )

    # Define the optional boolean argument to run the app without dumping urls as pdfs.
    # This will help us to prepare the list of all the urls needs to be dumped.
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Rrun the app without dumping urls as pdfs",
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the URL and boolean values
    start_url = args.url
    recovery_mode = args.recovery_mode
    dry_run = args.dry_run

    # Use the input arguments in your script
    print(f"URL: {start_url}")
    if recovery_mode:
        logger.info(
            f"Restarting the app by using the urls saved in "
            f"'tovisit.txt' & 'touched_urls.txt' as input"
        )

    logger.info(f"Start url: {start_url}")

    dir_name = url_to_str(start_url)
    create_directory(dir_name)

    scrape_root_url(start_url, dir_name, recovery_mode=recovery_mode, dry_run=dry_run)


if __name__ == "__main__":
    main()
