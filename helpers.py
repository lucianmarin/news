import requests
import urllib
from bs4 import BeautifulSoup
from settings import HEADERS, TOKEN


def get_paragraphs(soup):
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
            if child.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                text = child.text.strip()
                if text:
                    paragraphs.append(text)
    return paragraphs


def get_description(soup):
    desc = soup.find('meta', attrs={'name': "description"})
    t_desc = soup.find('meta', attrs={'name': "twitter:description"})
    og_desc = soup.find('meta', attrs={'property': "og:description"})
    desc_content = desc.get('content', '') if desc else ''
    t_desc_content = t_desc.get('content', '') if t_desc else ''
    og_desc_content = og_desc.get('content', '') if og_desc else ''
    desc_text = " ".join(desc_content.split())
    t_desc_text = " ".join(t_desc_content.split())
    og_desc_text = " ".join(og_desc_content.split())
    if og_desc_text:
        return og_desc_text
    elif t_desc_text:
        return t_desc_text
    elif desc_text:
        return desc_text
    else:
        return ''


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
    if description:
        return description
    elif paragraphs:
        return paragraphs[0]
    else:
        return ''


def fetch_paragraphs(link):
    r = requests.get(link, headers=HEADERS)
    soup = BeautifulSoup(r.text, features="lxml")
    return get_paragraphs(soup)


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
