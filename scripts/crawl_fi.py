import json
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = (
    "https://www.j-platpat.inpit.go.jp/"
    "cache/classify/patent/PMGS_HTML/jpp/FI/ja/"
)

YEAR = "202604"

visited = set()
records = []

session = requests.Session()

session.headers.update({
    "User-Agent":
    "Mozilla/5.0"
})


def get(url):

    r = session.get(
        url,
        timeout=120
    )

    r.raise_for_status()

    return r.text


def extract_level(title):

    m = re.match(
        r"^(・+)",
        title
    )

    if not m:
        return 0

    return len(m.group(1))


def add_record(
    code,
    title,
    fterm="",
    hb=False,
    cc=False
):

    records.append({

        "code": code,

        "title": title.lstrip("・"),

        "level": extract_level(title),

        "fterm": fterm,

        "hb": hb,

        "cc": cc

    })


def crawl_filist(url):

    print("FILIST", url)

    html = get(url)

    soup = BeautifulSoup(
        html,
        "lxml"
    )

    rows = soup.find_all("tr")

    for row in rows:

        a = row.find("a")

        explain = row.find(
            class_="explanationArea"
        )

        if not a:
            continue

        if not explain:
            continue

        fi_code = a.get("name")

        if not fi_code:
            continue

        title = explain.get_text(
            " ",
            strip=True
        )

        hb = False
        cc = False
        fterm = ""

        for link in row.find_all("a"):

            txt = link.get_text(
                strip=True
            )

            if txt == "HB":
                hb = True

            elif txt == "CC":
                cc = True

            elif re.match(
                r"^\d[A-Z]\d+",
                txt
            ):
                fterm = txt

        add_record(
            fi_code,
            title,
            fterm,
            hb,
            cc
        )


def crawl(url):

    if url in visited:
        return

    visited.add(url)

    print("CRAWL", url)

    try:

        html = get(url)

    except Exception as e:

        print(e)

        return

    soup = BeautifulSoup(
        html,
        "lxml"
    )

    for a in soup.find_all("a"):

        href = a.get(
            "href",
            ""
        )

        if not href:
            continue

        if "javascript:" in href:
            continue

        full = urljoin(
            url,
            href
        )

        if "fiClass" in href:

            crawl(full)

        elif "fiSubClass" in href:

            crawl(full)

        elif "fiMainGroup" in href:

            crawl(full)

        elif "fiList" in href:

            crawl_filist(full)


SECTIONS = list(
    "ABCDEFGH"
)

for s in SECTIONS:

    start = (
        BASE
        + "fiClass/"
        + f"fiClass{s}.html"
        + "?select="
        + YEAR
    )

    crawl(start)


records.sort(
    key=lambda x: x["code"]
)

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

print(
    "Records:",
    len(records)
)
