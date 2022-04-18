import requests
import sys
from bs4 import BeautifulSoup
from settings import *

def get_individual_assignmet_page_links() -> [str]:
    print("getting list table page html...")
    soup = BeautifulSoup(requests.post(DL_PAGE_ADDR, cookies=COOKIES).text, features="lxml")
    return [a["href"] for a in soup.find_all("a", attrs={"class": "title"}, href=True)]


def dl_attachments(assignmet_page_links: [str]) -> [[str, str]]:
    print("extracting download links, from each sub page, this may take a while...")
    dl_links = []

    for i, link in enumerate(links):
        print(f"{i}/{len(links)}", end='\r')
        page_soup = BeautifulSoup(requests.post(link, cookies=COOKIES).text, features="lxml")
        file_list_ul = page_soup.find("div", attrs={"class": "attachments"}).find("ul", attrs={"class": "files"})
        name = page_soup.find("div", attrs={"class": "fullname"}).find("a", href=True).text
        dl_links.append([
            name,
            [link.find("a", href=True)["href"] for link in file_list_ul.find_all("li", {"class": "application/zip"})][0]
        ]
        )

    # print(f"{dl_links=}")
    return dl_links


def bulk_download(dl_links: [str], continue_from: int):
    print("downloading files...")
    for i, link_and_name in enumerate(dl_links):
        if i >= continue_from:
            print(f"{i}/{len(links)}", end='\r')
            # print(f"{link_and_name}")
            name, link = link_and_name
            path = f"{DL_DIR}/{i:03}_{name}.{DEFAULT_FILE_EXT}"
            r = requests.get(link, cookies=COOKIES, stream=True)
            if r.status_code == 200:
                with open(path, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        continue_from = sys.argv[1]
    else:
         continue_from = 0
    links = get_individual_assignmet_page_links()
    # print(f"{links=}")

    dl_links = dl_attachments(links)
    bulk_download(dl_links, continue_from)
