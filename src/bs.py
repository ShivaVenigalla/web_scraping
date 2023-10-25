import os
import sys
import requests
import pdfkit
import io
from bs4 import BeautifulSoup
from PIL import Image
from urllib.parse import urljoin
from common.utils import url_to_str
from common.utils import get_logger
from common.utils import string_to_hash

logger = get_logger(__name__)


def update_toVisit_n_touched_lists(to_visit, touched_urls, new_link):
    if new_link not in touched_urls:
        if new_link.startswith("https://docs.github.com/en") or new_link.startswith(
            "https://docs.github.com/assets"
        ):
            logger.info(f"Inserted Link : {new_link}")
            to_visit.append(new_link)
            touched_urls.add(new_link)


def correct_url_as_useful(url):
    if "#" in url:
        parts = url.split("#")
        logger.debug(f"original url:'{url}'\tmodified to:'{parts[0]}'")
        return parts[0]
    return url  # Return the original URL if no modification is needed


def persist_iterabale_at(iterable, file_name):
    if os.path.exists(file_name):
        os.remove(file_name)

    with open(file_name, "w") as file:
        file.write("\n".join(iterable))


def persist_element_at(element, file_name):
    with open(file_name, "a") as file:
        file.write(element + "\n")
        
def dump_url(url, output_dir):
        response = requests.get(url)

        if not dry_run:
            save_url_as_pdf(url, response, output_dir)


def save_url_as_pdf(visit_url, response, dir_name):
    if response.status_code == 200:
        endPointHash = string_to_hash(visit_url)
        pdf_name = os.path.join(dir_name, endPointHash + ".pdf")
        with open("url_to_pdf_map", "a") as file:
            file.write(f"{endPointHash}\t{visit_url}" + "\n")
        content_type = response.headers.get("content-type")
        if "text/html" in content_type or "text/csv" in content_type:
            pdfkit.from_url(visit_url, pdf_name)
        elif "image/png" in content_type:
            imageContent = Image.open(io.BytesIO(response.content))
            imagePdf = imageContent.convert("RGB")
            imagePdf.save(pdf_name)
        elif "application/pdf" in content_type:
            with open(pdf_name, "wb") as file:
                file.write(response.content)
    else:
        logger.WARN(f"Unsuccessful Response for {visit_url} is {response.status_code}")


def scrape_root_url(start_url, dir_name, recovery_mode=False, dry_run=False):
    to_visit = []
    failed_urls = []
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

    visited_url_count = 0
    while to_visit:
        visit_url = to_visit.pop(0)

        try:
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

            if visited_url_count % 1000 == 0:
                persist_iterabale_at(to_visit, f"to_visit_{visited_url_count}.txt")
                persist_iterabale_at(
                    touched_urls, f"touched_urls_{visited_url_count}.txt"
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
                        logger.info(f"{visit_url}\t{href}\t{modified_url}")
                        update_toVisit_n_touched_lists(
                            to_visit, touched_urls, modified_url
                        )
                    elif href[0] == "/":
                        new_link = urljoin(start_url, href)

                        modified_url = correct_url_as_useful(new_link)
                        logger.info(f"{visit_url}\t{href}\t{modified_url}")
                        update_toVisit_n_touched_lists(
                            to_visit, touched_urls, modified_url
                        )

            if not dry_run:
                save_url_as_pdf(visit_url, response, dir_name)
            visited_url_count += 1
        except Exception as e:
            # Catch the exception and print its message
            logger.error(f"An exception occurred: {str(e)}")
            logger.error(
                f"Skipping this url: {visit_url}\tvisited url: {visited_url_count}"
            )

            failed_urls.append(visit_url)
            persist_element_at(visit_url, f"failed_urls.txt")
            save_url_lists = True

    if save_url_lists:
        # Save visited & touched urls.
        persist_iterabale_at(to_visit, "to_visit.txt")
        persist_iterabale_at(touched_urls, "touched_urls.txt")

    if len(failed_urls):
        # Save failed urls.
        persist_iterabale_at(failed_urls, "failed_urls.txt")
