import lxml.html

from html.parser import HTMLParser
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from mechanize import Browser
from http import HTTPStatus
from http.client import RemoteDisconnected


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ''
        self._in_title_tag = False

    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self._in_title_tag = True

    def handle_data(self, data):
        if self._in_title_tag:
            self.title += data

    def handle_endtag(self, tag):
        if tag == 'title':
            self._in_title_tag = False


def get_title(url):
    try:
        with urlopen(url) as stream:
            data = stream.read()
    except:
        return url

    parser = Parser()
    parser.feed(data.decode('utf-8', errors='ignore'))
    return parser.title


def gettitle(url):
    ret = None
    try:
        req = Request(url)
        urlopen(req)
    except ValueError as e:
        ret = str(e)
    except HTTPError as e:
        ret = "[" + str(e.code) + " - " + HTTPStatus(e.code).phrase + "]"
    except URLError as e:        
        ret = str(e.reason)
    except RemoteDisconnected as e:
        ret = str(e)
    except ConnectionResetError as e:
        ret = str(e)
    if ret:
        return ret
    else:
        try:
            t = lxml.html.parse(url)
            return t.find(".//title").text
        except:
            return -1


def _get_title(url):
    response = ""
    try:
        br = Browser()
        br.open(url)
        response = br.title()
    except:
        response = "request disallowed by robots"
    return (response)
