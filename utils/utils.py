from urllib.parse import urlparse, urljoin
from flask import request

def url_has_allowed_host_and_scheme(target, host_url):
    ref_url = urlparse(host_url)
    test_url = urlparse(urljoin(host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
