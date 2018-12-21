import requests
import urllib
from bs4 import BeautifulSoup
from settings import TOKEN


def fetch_fb(link):
    path = "https://graph.facebook.com/v2.8/?id={0}&access_token={1}"
    url = urllib.parse.quote(link)
    graph = path.format(url, TOKEN)
    return requests.get(graph).json()


def fetch_desc(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, features="lxml")
    description = soup.find("meta", attrs={'name': "description"})
    og_description = soup.find("meta", property="og:description")
    desc_content = description.get('content', '') if description else ''
    og_desc_content = og_description.get('content', '') if og_description else ''
    desc_text = " ".join(desc_content.split())
    og_desc_text = " ".join(og_desc_content.split())
    if og_desc_text:
        return og_desc_text
    elif desc_text:
        return desc_text
    else:
        return ''
