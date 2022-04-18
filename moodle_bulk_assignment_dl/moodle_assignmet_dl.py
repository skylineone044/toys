import requests
import sys
import json
from bs4 import BeautifulSoup
from settings import *

def get_individual_assignmet_page_links() -> [str]:
    print("getting list table page html...")
    soup = BeautifulSoup(requests.post(DL_PAGE_ADDR, cookies=COOKIES).text, features="lxml")
    return [a["href"] for a in soup.find_all("a", attrs={"class": "title"}, href=True)]


def dl_attachments(assignmet_page_links: [str], continue_from: int) -> [[str, str]]:
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
            if i >= continue_from:
                print(f"{i}/{len(assignmet_page_links)}        ", end='\r')
                page_soup = BeautifulSoup(requests.post(link, cookies=COOKIES).text, features="lxml")
                file_list_ul = page_soup.find("div", attrs={"class": "attachments"}).find("ul",
                                                                                          attrs={"class": "files"})
                name = page_soup.find("div", attrs={"class": "fullname"}).find("a", href=True).text
                dl_links.append([
                    name,
                    [link.find("a", href=True)["href"] for link in
                     file_list_ul.find_all("li", {"class": "application/zip"})][0]
                    ]
                )

        # print(f"{dl_links=}")
        with open("link_cache.json", 'w') as file:
            json.dump({"source_url": DL_PAGE_ADDR, "dl_links": dl_links}, file, indent=4)

    return dl_links


def bulk_download(dl_links: [str], continue_from: int):
    print("downloading files...")
    for i, link_and_name in enumerate(dl_links):
        print(f"{i+continue_from-1}/{len(links)}        ", end='\r')
        # print(f"{link_and_name}")
        name, link = link_and_name
        path = f"{DL_DIR}/{i+continue_from:03}_{name}.{DEFAULT_FILE_EXT}"
        r = requests.get(link, cookies=COOKIES, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        else:
            print("baj")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        continue_from = int(sys.argv[1])
    else:
         continue_from = 0
    links = get_individual_assignmet_page_links()
    # print(f"{links=}")

    dl_links = dl_attachments(links, continue_from)
    bulk_download(dl_links, continue_from)
