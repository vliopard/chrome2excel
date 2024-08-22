import preset
import requests
import mechanize
import lxml.html
import tldextract
import chrome_pages
import encode_master
from tld import get_fld
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from urllib.request import urlopen, Request


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = preset.SYMBOL_EMPTY
        self._in_title_tag = False

    def handle_starttag(self, tag, attrs):
        if tag == preset.TITLE:
            self._in_title_tag = True

    def handle_data(self, data):
        if self._in_title_tag:
            self.title += data

    def handle_endtag(self, tag):
        if tag == preset.TITLE:
            self._in_title_tag = False


def urlopen_wrapper(url_address, encode=False, time_out=preset.TIMEOUT):
    response = urlopen(url_address, timeout=time_out)
    if encode:
        response.encoding = encode_master.get_encoding_master(url_address)
    return response


def request_wrapper(url_address, header=None, encode=None, rfs=False, time_out=preset.TIMEOUT):
    if header:
        response = requests.get(url_check(url_address), headers=header, timeout=time_out)
    else:
        response = requests.get(url_check(url_address), timeout=time_out)

    if encode:
        response.encoding = encode_master.get_encoding_master(url_address)

    if rfs:
        response.raise_for_status()

    return response


def soup_wrapper(response, method, encode=None):
    if encode:
        return BeautifulSoup(response, method, from_encoding=encode)
    return BeautifulSoup(response, method)


def clean_title(title):
    if title:
        if title == preset.YOUTUBE_T:
            return None
        new_title = preset.SYMBOL_SPACE.join(title.replace(preset.NEW_LINE, preset.SYMBOL_SPACE).replace(preset.TAB, preset.SYMBOL_SPACE).replace(preset.RECURSE, preset.SYMBOL_SPACE).strip().split())
        if new_title.endswith('.'):
            new_title = new_title[:-1]
        return new_title
    return preset.NO_TITLE


def url_check(url_address):
    if url_address.startswith(preset.HTTP) or url_address.startswith(preset.FTP_L) or url_address.startswith(preset.ABOUT) or url_address.startswith(preset.CHROME) or url_address.startswith(preset.FILE) or url_address.startswith(preset.VIEW_SOURCE) or url_address.startswith(preset.JAVASCRIPT):
        return url_address
    return f'{preset.PROTOCOL}{url_address}'


def get_short_addr(url_address):
    return get_fld(url_check(url_address))


def get_short_address(url_address):
    response = tldextract.extract(url_check(url_address))
    if response.domain and response.suffix:
        return f'{preset.PROTOCOL}{response.domain}.{response.suffix}'
    return preset.NO_DOMAIN


def parse_fld(url_val):
    try:
        return get_short_addr(url_val)
    except Exception:
        return get_short_address(url_val)


def open_with_urlopen(url_address, encode=False):
    try:
        return urlopen_wrapper(url_check(url_address), encode)
    except Exception:
        return urlopen_request(url_address, encode)


def urlopen_request(url_address, encode):
    try:
        return urlopen_wrapper(Request(url_check(url_address)), encode)
    except Exception:
        return None


def get_title_from_chrome_pages(this_url):
    if this_url in chrome_pages.chrome_pages:
        return clean_title(chrome_pages.chrome_pages[this_url])


def open_with_urlopen_stream(url_address):
    try:
        with open_with_urlopen(url_address) as stream:
            return stream.read()
    except Exception:
        return None


def get_title_urlopen_stream(url_address):
    url_data = open_with_urlopen_stream(url_address)
    try:
        url_parser = Parser()
        url_parser.feed(url_data.decode(encode_master.get_encoding_master(url_address), errors=preset.IGNORE))
        return clean_title(url_parser.title)
    except Exception:
        return None


def get_title_bs4_requests_encode(url_address):
    try:
        response = request_wrapper(url_address, encode=True)
        soup = soup_wrapper(response.text, preset.HTML_PARSER)
        value = clean_title(soup.title.string)
        if value == preset.ERROR:
            return None
        return value
    except Exception:
        return None


def get_title_lxml(url_address):
    try:
        title = lxml.html.parse(url_check(url_address))
        return clean_title(title.find(preset.TITLE_SCAPE).text)
    except Exception:
        return None


def get_title_bs4_requests_encoded_status(url_address):
    try:
        response = request_wrapper(url_address, encode=True, rfs=True)
        soup = soup_wrapper(response.text, preset.HTML_PARSER)
        return clean_title(soup.title.text)
    except Exception:
        return None


def get_title_bs4_urlopen_encoded(url_address):
    try:
        soup = soup_wrapper(open_with_urlopen(url_address, encode=True), preset.HTML_PARSER)
        return clean_title(soup.title.string)
    except Exception:
        return None


def get_title_bs4_urlopen_get_encode(url_address):
    try:
        soup = soup_wrapper(open_with_urlopen(url_address), preset.HTML_PARSER, encode_master.get_encoding_master(url_address))
        return clean_title(soup.title.string)
    except Exception:
        return None


def get_title_bs4_urlopen_read_encoded(url_address):
    try:
        response = open_with_urlopen(url_address, encode=True)
        soup = soup_wrapper(response.read(), preset.HTML_PARSER, encode_master.get_encoding_master(url_address))
        return clean_title(soup.title.text)
    except Exception:
        return None


def get_title_mechanized(url_address):
    try:
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.set_handle_refresh(False)
        br.open(url_check(url_address), timeout=preset.TIMEOUT)
        return clean_title(br.title())
    except Exception:
        return None


def get_title_bs4_lxml(url_address):
    try:
        soup = soup_wrapper(open_with_urlopen(url_address, encode=True), preset.LXML, encode_master.get_encoding_master(url_address))
        return clean_title(soup.title.string)
    except Exception:
        return None


def get_title_bs4_apparent(url_address):
    try:
        response = request_wrapper(url_address, header=preset.HEADERS, rfs=True)
        response.encoding = response.apparent_encoding
        soup = soup_wrapper(response.content.decode(encode_master.get_encoding_master(url_address), preset.REPLACE), preset.HTML_PARSER)
        return clean_title(soup.title.text)
    except Exception:
        return None


def get_title_bs4_requests_headers_encode_status(url_address):
    try:
        response = request_wrapper(url_address, header=preset.HEADERS, rfs=True, encode=True)
        soup = soup_wrapper(response.text, preset.HTML_PARSER)
        return clean_title(soup.title.text)
    except Exception:
        return None


def get_title_master(url_address):
    debug = False
    print(f'get_title_master[{url_address}]') if debug else None

    answer = get_title_from_chrome_pages(url_address)
    if answer:
        print(f'get_title_from_chrome_pages[{answer}]') if debug else None
        return answer

    answer = get_title_bs4_apparent(url_address)
    if answer:
        print(f'get_title_bs4_apparent[{answer}]') if debug else None
        return answer

    answer = get_title_bs4_requests_encoded_status(url_address)
    if answer:
        print(f'get_title_bs4_requests_encoded_status[{answer}]') if debug else None
        return answer

    answer = get_title_bs4_lxml(url_address)
    if answer:
        print(f'get_title_bs4_lxml[{answer}]') if debug else None
        return answer

    answer = get_title_bs4_requests_headers_encode_status(url_address)
    if answer:
        print(f'get_title_bs4_requests_headers_encode_status[{answer}]') if debug else None
        return answer

    answer = get_title_mechanized(url_address)
    if answer:
        print(f'get_title_mechanized[{answer}]') if debug else None
        return answer

    answer = get_title_bs4_urlopen_read_encoded(url_address)
    if answer:
        print(f'get_title_bs4_urlopen_read_encoded[{answer}]') if debug else None
        return answer

    answer = get_title_bs4_urlopen_get_encode(url_address)
    if answer:
        print(f'get_title_bs4_urlopen_get_encode[{answer}]') if debug else None
        return answer

    answer = get_title_urlopen_stream(url_address)
    if answer:
        print(f'get_title_urlopen_stream[{answer}]') if debug else None
        return answer

    answer = get_title_bs4_urlopen_encoded(url_address)
    if answer:
        print(f'get_title_bs4_urlopen_encoded[{answer}]') if debug else None
        return answer

    answer = get_title_bs4_requests_encode(url_address)
    if answer:
        print(f'get_title_bs4_requests_encode[{answer}]') if debug else None
        return answer

    answer = get_title_lxml(url_address)
    if answer:
        print(f'get_title_lxml[{answer}]') if debug else None
        return answer

    print(f'get_title_master[{preset.NO_TITLE}]') if debug else None
    return preset.NO_TITLE
