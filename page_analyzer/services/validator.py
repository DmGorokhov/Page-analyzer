from validators import url as is_valid_url
from urllib.parse import urlparse

MAXLENGTH_URL = 255


def validate_url(url: str) -> bool:
    return is_valid_url(url) and len(url) <= MAXLENGTH_URL


def get_parsed_url(url: str) -> str:
    parsed_url = urlparse(url)
    format_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    return format_url
