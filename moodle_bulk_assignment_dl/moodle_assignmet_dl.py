import requests
from bs4 import BeautifulSoup

COOKIES = {"MoodleSession": "INSERT YOUR MOODLE COOKIE HERE"}
DL_PAGE_ADDR = "INSERT YOUR MOODLE HUB TABLE PAGE ADDRESS HERE"  # for example: "https://moodle2.inf.u-szeged.hu/moodle38/mod/workshop/view.php?id=81" it works best if you set to see all entries in the moodle web interface, so the sript actually sees all the links, as it will not step through the pages for you
DL_DIR = "/home/skyline/Downloads/bulk_moodle/cmd"  # set the directory for the results to be saved to
DEFAULT_FILE_EXT = "zip"  # resutl file extenison


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

    print(f"{dl_links=}")
    return dl_links


def bulk_download(dl_links: [str]):
    print("downloading files...")
    for i, link_and_name in enumerate(dl_links):
        print(f"{i}/{len(links)}", end='\r')
        # print(f"{link_and_name}")
        name, link = link_and_name
        path = f"{DL_DIR}/{i:03}_{name}.{DEFAULT_FILE_EXT}"
        r = requests.get(link, cookies=COOKIES, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)


links = get_individual_assignmet_page_links()
print(f"{links=}")

dl_links = dl_attachments(links)
bulk_download(dl_links)
