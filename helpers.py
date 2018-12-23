import requests
import urllib
from bs4 import BeautifulSoup
from settings import HEADERS, TOKEN


def get_url(link):
    url = urllib.parse.urlparse(link)
    url_list = list(url)
    url_list[4] = ''
    return urllib.parse.urlunparse(url_list)


def get_paragraphs(soup):
    allowed = ["p", "h1", "h2", "h3", "h4", "h5", "h6", "pre"]
    block = ["script", "ins"]
    candidate = None
    counter = 0
    for tag in soup.findAll():
        length = len(tag.findAll('p', recursive=False))
        if length > counter:
            candidate = tag
            counter = length
    paragraphs = []
    if candidate:
        for child in candidate.children:
            if child.name in allowed:
                for subchild in child.findAll():
                    if subchild.name in block:
                        subchild.decompose()
                text = child.text.strip()
                if text:
                    if child.name in ["p", "pre"]:
                        paragraphs.append((text, False))
                    else:
                        paragraphs.append((text, True))
    return paragraphs


def get_description(soup):
    attrs = (
        {'name': "description"},
        {'name': "twitter:description"},
        {'name': "og:description"},
        {'property': "og:description"}
    )
    description = ""
    for attr in attrs:
        meta = soup.find('meta', attrs=attr)
        meta_content = meta.get('content', '') if meta else ''
        meta_pretty = " ".join(meta_content.split())
        description = meta_pretty if meta_pretty else description
    return description


def fetch_fb(link):
    path = "https://graph.facebook.com/v2.8/?id={0}&access_token={1}"
    url = urllib.parse.quote(link)
    graph = path.format(url, TOKEN)
    return requests.get(graph).json()


def fetch_desc(link):
    r = requests.get(link, headers=HEADERS)
    soup = BeautifulSoup(r.text, features="lxml")
    description = get_description(soup)
    paragraphs = get_paragraphs(soup)
    description = '' if description.endswith(('…', '...')) else description
    if not description and paragraphs:
        return paragraphs[0][0]
    return description


def fetch_paragraphs(link):
    r = requests.get(link, headers=HEADERS)
    soup = BeautifulSoup(r.text, features="lxml")
    return get_paragraphs(soup)


def fetch_external(link):
    def netloc(value):
        url = urllib.parse.urlsplit(value)
        return url.netloc.replace('www.', '')
    hn = netloc(link)
    r = requests.get(link, headers=HEADERS)
    soup = BeautifulSoup(r.text, features="lxml")
    links = set()
    for a in soup.findAll('a', href=True):
        href = a['href']
        if href.startswith(('https://', 'http://')) and netloc(href) != hn:
            links.add(href)
    print(links)
    print(len(links))
    return list(links)


def fetch_words(link):
    r = requests.get(link, headers=HEADERS)
    soup = BeautifulSoup(r.text, features="lxml")
    words = set()
    textual_tags = ['td', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    for tag in soup.findAll(textual_tags):
        for word in tag.text.split():
            words.add(word.lower())
    print(words)
    print(len(words))
    return list(words)
