from validators import url as is_valid_url
from urllib.parse import urlparse
import requests
from datetime import datetime
from bs4 import BeautifulSoup


def validate_url(url):
    MAXLENGTH_URL = 255
    return is_valid_url(url) and len(url) <= MAXLENGTH_URL


def get_parsed_url(url):
    parsed_url = urlparse(url)
    format_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    return format_url


def make_urlcheck(url_id, url_name):
    url_request = requests.get(url_name)
    if url_request.status_code == requests.codes.ok:
        soup = BeautifulSoup(url_request.text, 'html.parser')
        desc = soup.find('meta', attrs={'name': 'description'})

        check = {'url_id': url_id,
                 'status_code': url_request.status_code,
                 'h1': soup.h1.string,
                 'title': soup.head.title.string,
                 'description': (desc['content'] if desc else None),
                 'created_at': datetime.now()
                 }
        return check
    return