import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
GENERATOR = ROOT / "generator"
TEMPLATE_FILE = GENERATOR / "template.html"
OUTPUT = ROOT / "index.html"
BASE_URL = "https://docs.aws.amazon.com/whitepapers/latest/aws-overview"
START_URL = f"{BASE_URL}/amazon-web-services-cloud-platform.html"


@dataclass
class Card:
    title: str
    text: str
    url: str
    index: int = 0

    def clean(self):
        self.title = self.title.strip()
        self.text = self.text.strip()


def fetch(url):
    resp = requests.get(url)
    resp.encoding = resp.apparent_encoding
    if resp.status_code != 200:
        return None
    return resp.text


def get_doc_pages(data):
    soup = BeautifulSoup(data, "html.parser")
    table = soup.find("div", {"class": "table-container"})
    links = table.find_all("a")
    urls = []
    for link in links:
        url = link.attrs.get("href")
        if url:
            urls.append(f"{BASE_URL}{url[1:]}")
    return urls


def get_card_from_doc_page(url):
    data = fetch(url)
    if not data:
        raise FileNotFoundError
    soup = BeautifulSoup(data, "html.parser")
    cards = []
    main_content = soup.find("div", attrs={"id": "main-col-body"}).children
    found_start = False
    title = None
    text = []
    for child in main_content:
        if found_start == False and child.name != "h2":
            continue
        else:
            found_start = True
        if child.name == "h2" or child.name == "h3":
            if len(text) > 0:
                card = Card(str(title), "\n".join([str(i) for i in text]), url)
                cards.append(card)
                title = None
            title = child
            text = []
        if title and child.name == "p":
            html_text = child.text
            if "Return to AWS services." in html_text:
                continue
            text.append(child)
    card = Card(str(title), "\n".join([str(i) for i in text]), url)
    if title:
        cards.append(card)
    return cards


def get_html(cards):
    template = TEMPLATE_FILE.read_text()
    content = "<div class=content>"
    for card in cards:
        content += card_html(card)
    content += "</div>"
    return template.replace("{{ content }}", content)


def card_html(card):
    return f"""
            <div id="card-{card.index}" class="card">
                <div class="top">{card.title}</div>
                <div class="bottom">{card.text}</div>
            </div>
            """


if __name__ == "__main__":
    data = fetch(START_URL)
    doc_urls = get_doc_pages(data)
    cards = []
    for url in doc_urls:
        cards += get_card_from_doc_page(url)
    for i, card in enumerate(cards):
        card.index = i
        card.clean()
    html = get_html(cards)
    soup = BeautifulSoup(html, "html.parser")
    OUTPUT.write_text(soup.prettify())
