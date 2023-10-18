import os
import sys
import requests
import pdfkit
from bs4 import BeautifulSoup
from common.utils import url_to_str


def scrape_root_url(start_url, dir_name):
    to_visit = []
    touched_urls = set()
    to_visit.append(start_url)
    touched_urls.add(start_url)
    print(to_visit)

    while to_visit:
        linkToVisit = to_visit.pop(0)
        print(linkToVisit, '==== More to go : ' + str(len(to_visit)))
        response = requests.get(linkToVisit)
        source = BeautifulSoup(response.text, "html.parser")
        divsFound = source.find_all("div", {"class": "d-lg-flex"})
        if len(divsFound) < 2:
            continue
        div = divsFound[1]
        linksFound = div.find_all('a')
        for link in linksFound:
            if link.has_attr("href"):
                href = link["href"]
                if href[0] == "#" and len(href) > 1:
                    new_link = linkToVisit + href
                    if new_link not in touched_urls:
                        to_visit.append(new_link)
                        touched_urls.add(new_link)
                if href[0] == "?" and len(href) > 1:
                    new_link = linkToVisit + href
                    if new_link not in touched_urls:
                        to_visit.append(new_link)
                        touched_urls.add(new_link)
                elif href[0] == "/":
                    new_link = start_url + href
                    if new_link not in touched_urls:
                        to_visit.append(new_link)
                        touched_urls.add(new_link)

        end_point = linkToVisit.removeprefix(start_url)

        pdf_name = os.path.join(dir_name, url_to_str(end_point) + ".pdf")
        pdfkit.from_url(linkToVisit, pdf_name)
