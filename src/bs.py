import os
import sys
import requests
import pdfkit
from bs4 import BeautifulSoup
from  urllib.parse import urljoin
from common.utils import url_to_str


def update_toVisit_n_touched_lists(to_visit, touched_urls, new_link):
    to_visit.append(new_link)
    touched_urls.add(new_link)


def scrape_root_url(start_url, dir_name, recovery_mode=False, dry_run=False):
    to_visit = []
    touched_urls = set()

    if recovery_mode:
        if os.path.exists("touched_urls.txt") and os.path.exists("to_visit.txt"):
            # Read touched_urls
            with open("touched_urls.txt", "r") as f:
                lines = []
                for line in f:
                    touched_urls.add(line.strip())
            # Read tovisit links
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

    try:
        visited_url_count = 0
        while to_visit:
            linkToVisit = to_visit.pop(0)
            print(
                f"url:{linkToVisit},\tTotal urls visited:{visited_url_count}"
                f"\tTouched urls:{len(touched_urls)}"
                f"\tLinks to visit: {len(to_visit)}"
            )
            response = requests.get(linkToVisit)
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
                        new_link = urljoin(linkToVisit, href)
                        if new_link not in touched_urls:
                            update_toVisit_n_touched_lists(
                                to_visit, touched_urls, new_link
                            )
                    elif href[0] == "/":
                        new_link = urljoin(start_url, href)
                        if new_link not in touched_urls:
                            update_toVisit_n_touched_lists(
                                to_visit, touched_urls, new_link
                            )

            if not dry_run:
                end_point = linkToVisit.removeprefix(start_url)
                pdf_name = os.path.join(dir_name, url_to_str(end_point) + ".pdf")
                pdfkit.from_url(linkToVisit, pdf_name)
            visited_url_count += 1
    except Exception:
        print("Exception Occured")
    finally:
        if dry_run:
            # Save visited & touched urls.
            with open("to_visit.txt", "w") as file:
                file.write("\n".join(to_visit))
            with open("touched_urls.txt", "a") as the_file:
                the_file.write("\n".join(touched_urls))
