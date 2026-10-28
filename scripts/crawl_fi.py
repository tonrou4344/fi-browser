import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://www.j-platpat.inpit.go.jp/cache/classify/patent/PMGS_HTML/jpp/FI/ja/"
YEAR = "202604"

visited = set()

records = []

def get(url):

    print(url)

    r = requests.get(url, timeout=120)

    r.raise_for_status()

    return r.text

def crawl_filist(url):

    html = get(url)

    soup = BeautifulSoup(html, "lxml")

    rows = soup.find_all("tr")

    for r in rows:

        a = r.find("a")

        e = r.find(class_="explanationArea")

        if e is None:
            continue

        if a and a.get("name"):

            code = a["name"]

            title = e.get_text(" ", strip=True)

            hb = False
            cc = False
            fterm = ""

            for x in r.find_all("a"):

                txt = x.get_text(strip=True)

                if txt == "HB":
                    hb = True

                elif txt == "CC":
                    cc = True

                elif txt.startswith("4"):
                    fterm = txt

            records.append({
                "code": code,
                "title": title,
                "hb": hb,
                "cc": cc,
                "fterm": fterm
            })

def crawl(url):

    if url in visited:
        return

    visited.add(url)

    html = get(url)

    soup = BeautifulSoup(html, "lxml")

    for a in soup.find_all("a"):

        href = a.get("href", "")

        if "fiClass" in href:
            crawl(urljoin(url, href))

        elif "fiSubClass" in href:
            crawl(urljoin(url, href))

        elif "fiMainGroup" in href:
            crawl(urljoin(url, href))

        elif "fiList" in href:

            full = urljoin(url, href)

            crawl_filist(full)

root = (
 BASE
 +
 "fiSection/fiSection.html?select="
 +
 YEAR
)

crawl(root)

with open(
 "data/fi_latest.json",
 "w",
 encoding="utf-8"
) as f:

    json.dump(
      records,
      f,
      ensure_ascii=False,
      indent=2
    )
