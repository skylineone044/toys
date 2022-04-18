import time
import requests
import sys
import json
from bs4 import BeautifulSoup
from settings import *


def get_individual_assignmet_page_links() -> [str]:
    print("getting list table page html...")
    soup = BeautifulSoup(requests.post(DL_PAGE_ADDR, cookies=COOKIES).text, features="lxml")
    return [a["href"] for a in soup.find_all("a", attrs={"class": "title"}, href=True)]


def get_dl_links(assignmet_page_links: [str]) -> [[str, str]]:
    print("extracting download links, from each sub page, this may take a while...")
    dl_links = []

    try:
        with open("link_cache.json", 'r') as file:
            jsonData = json.load(file)
            source_url = jsonData["source_url"]
            links = jsonData["dl_links"]
            if source_url == DL_PAGE_ADDR:
                dl_links = links
                print("using cached list!")
            else:
                raise FileNotFoundError
    except FileNotFoundError:
        for i, link in enumerate(assignmet_page_links):
            while True:
                try:
                    print(f"{i}/{len(assignmet_page_links) - 1}        ", end='\r')
                    page_soup = BeautifulSoup(requests.post(link, cookies=COOKIES, timeout=5).text, features="lxml")
                    file_list_ul = page_soup.find("div", attrs={"class": "attachments"}).find("ul", attrs={"class": "files"})
                    name = page_soup.find("div", attrs={"class": "fullname"}).find("a", href=True).text
                    dl_links.append([
                        name,
                        [link.find("a", href=True)["href"] for link in
                         file_list_ul.find_all("li", {"class": "application/zip"})][0]
                    ]
                    )
                    break
                except requests.exceptions.ConnectionError:
                    print("timeout, waiting 5s...")
                    time.sleep(5)
                    continue

        # print(f"{dl_links=}")
        with open("link_cache.json", 'w') as file:
            json.dump({"source_url": DL_PAGE_ADDR, "dl_links": dl_links}, file, indent=4)

    return dl_links


def bulk_download(links: [str], continue_from: int):
    print("downloading files...")
    for i, link_and_name in enumerate(links):
        print(f"{i + continue_from}/{len(links) - 1}        ", end='\r')
        # print(f"{link_and_name}")
        name, link = link_and_name
        path = f"{DL_DIR}/{i + continue_from:03}_{name}.{DEFAULT_FILE_EXT}"
        while True:
            try:
                r = requests.get(link, cookies=COOKIES, stream=True, timeout=5)
                if r.status_code == 200:
                    with open(path, 'wb') as f:
                        for chunk in r:
                            f.write(chunk)
                else:
                    print(f"Http error: {r.status_code}")
                break
            except requests.exceptions.ConnectionError:
                print("timed out, waiting 5s...")
                time.sleep(5)
                continue


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            continue_from = int(sys.argv[1])
        else:
            continue_from = 0
        links = get_individual_assignmet_page_links()
        # print(f"{links=}")

        dl_links = get_dl_links(links)
        bulk_download(dl_links[continue_from:], continue_from)
        print("done.")
    except KeyboardInterrupt:
        print("\nInterrupted by user")
