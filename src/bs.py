import os
import sys
import requests
import pdfkit
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from common.utils import url_to_str
from common.utils import get_logger

logger = get_logger(__name__)


def update_toVisit_n_touched_lists(to_visit, touched_urls, new_link):
    if new_link not in touched_urls:
        to_visit.append(new_link)
        touched_urls.add(new_link)


def correct_url_as_useful(url):
    if "#" in url:
        parts = url.split("#")
        if "?" not in parts[1]:
            # If there's no '?' after '#', truncate the URL before '#'
            logger.debug(f"original url:'{url}'\tmodified to:'{parts[0]}'")
            return parts[0]
    return url  # Return the original URL if no modification is needed


def persist_iterabale_at(iterable, file_name):
    if os.path.exists(file_name):
        os.remove(file_name)

    with open(file_name, "w") as file:
        file.write("\n".join(iterable))


def scrape_root_url(start_url, dir_name, recovery_mode=False, dry_run=False):
    to_visit = []
    touched_urls = set()
    save_url_lists = dry_run

    if recovery_mode:
        if os.path.exists("touched_urls.txt") and os.path.exists("to_visit.txt"):
            # Read touched_urls
            with open("touched_urls.txt", "r") as f:
                lines = []
                for line in f:
                    touched_urls.add(line.strip())
            # Read to-visit links
            with open("to_visit.txt", "r") as f:
                lines = []
                for line in f:
                    to_visit.append(line.strip())
        else:
            to_visit.append(start_url)
            touched_urls.add(start_url)
    else:
        to_visit.append(start_url)
        touched_urls.add(start_url)

    visit_url = None
    try:
        visited_url_count = 0
        while to_visit:
            visit_url = to_visit.pop(0)

            if visit_url == None:
                logger.warning(
                    f"A 'None' element has been added to the list of URLs."
                    f" It should not happen"
                )
                continue

            logger.debug(
                f"Visiting url:{visit_url},\tTotal urls visited:{visited_url_count}"
                f"\tTouched urls:{len(touched_urls)}"
                f"\tLinks to visit: {len(to_visit)}"
            )

            if visited_url_count % 100 == 0:
                logger.info(
                    f"url:{visit_url},\tTotal urls visited:{visited_url_count}"
                    f"\tTouched urls:{len(touched_urls)}"
                    f"\tLinks to visit: {len(to_visit)}"
                )

            response = requests.get(visit_url)
            source = BeautifulSoup(response.text, "html.parser")
            divsFound = source.find_all("div", {"class": "d-lg-flex"})

            if len(divsFound) < 2:
                continue

            div = divsFound[1]
            linksFound = div.find_all("a")

            for link in linksFound:
                if link.has_attr("href"):
                    href = link["href"]

                    if href[0] == "?" and len(href) > 1:
                        new_link = urljoin(visit_url, href)

                        modified_url = correct_url_as_useful(new_link)
                        update_toVisit_n_touched_lists(
                            to_visit, touched_urls, modified_url
                        )
                    elif href[0] == "/":
                        new_link = urljoin(start_url, href)

                        modified_url = correct_url_as_useful(new_link)
                        update_toVisit_n_touched_lists(
                            to_visit, touched_urls, modified_url
                        )

            if not dry_run:
                end_point = visit_url.removeprefix(start_url)
                pdf_name = os.path.join(dir_name, url_to_str(end_point) + ".pdf")
                pdfkit.from_url(visit_url, pdf_name)
            visited_url_count += 1
    except Exception as e:
        # Catch the exception and print its message
        logger.error(f"An exception occurred: {str(e)}")

        to_visit.append(visit_url)
        save_url_lists = True
    finally:
        if save_url_lists:
            # Save visited & touched urls.
            persist_iterabale_at(to_visit, "to_visit.txt")
            persist_iterabale_at(touched_urls, "touched_urls.txt")
