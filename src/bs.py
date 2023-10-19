import os
import sys
import requests
import pdfkit
from bs4 import BeautifulSoup
from common.utils import url_to_str


def scrape_root_url(start_url, dir_name):
    to_visit = []
    touched_urls = set()
    if os.path.exists('touched_urls.txt') and os.path.exists('to_visit.txt'):
        # Read touched_urls
        with open('touched_urls.txt', 'r') as f:
            lines = []
            for line in f:
                touched_urls.add(line.strip())
        # Read tovisit links
        with open('to_visit.txt', 'r') as f:
            lines = []
            for line in f:
                to_visit.append(line.strip())
    else:
        to_visit.append(start_url)
        touched_urls.add(start_url)

    try:
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
                    if href[0] == "#" and len(href) > 1 and '#' not in linkToVisit:
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
            with open('touched_urls.txt', 'a') as the_file:
                the_file.write(linkToVisit + '\n')

            pdf_name = os.path.join(dir_name, url_to_str(end_point) + ".pdf")
            pdfkit.from_url(linkToVisit, pdf_name)
    except Exception:
        print('Exception Occured')
    finally:
        # Touched urls are already saved.
        # Now try to save to_visit urls.
        with open('to_visit.txt','w') as file:
	        file.write('\n'.join(to_visit))
