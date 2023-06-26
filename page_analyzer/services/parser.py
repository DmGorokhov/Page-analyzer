import requests
from datetime import datetime
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict

MAXLENGTH_URL = 255


@dataclass(slots=True, frozen=True)
class UrlCheck:
    url_id: int
    status_code: int
    h1: str | None
    title: str | None
    description: str | None
    created_at: datetime


def make_url_request(url_name: str):
    try:
        response = requests.get(url_name)
        response.raise_for_status()
        return response
    except requests.HTTPError:
        return 'error'


def make_urlcheck(url_id: int, url_name: str) -> dict[str, any] | None:
    "Returns check parameters if request was successfull"
    url_response = make_url_request(url_name)
    if url_response != 'error':
        soup = BeautifulSoup(url_response.text, 'html.parser')
        desc = soup.find('meta', attrs={'name': 'description'})

        check = UrlCheck(
            url_id=url_id,
            status_code=url_response.status_code,
            h1=(soup.h1.string if soup.h1 else None),
            title=(soup.head.title.string if soup.head else None),
            description=(desc['content'] if desc else None),
            created_at=(datetime.now())
        )
        return asdict(check)
    return
