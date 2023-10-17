import sys

from common.utils import url_to_str
from common.utils import create_directory
from bs import scrape_root_url


def main():
    # Access command-line arguments using sys.argv
    # sys.argv[0] is the script name, and subsequent elements are arguments
    if len(sys.argv) < 2:
        print("Usage: python script.py <base_url>")
        return

    start_url = sys.argv[1]

    print(f"Start url: {start_url}")

    dir_name = url_to_str(start_url)
    create_directory(dir_name)

    scrape_root_url(start_url, dir_name)


if __name__ == "__main__":
    main()
