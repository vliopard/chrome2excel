import tools
import preset

from socket import timeout
from html.parser import HTMLParser

from urllib import parse
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse, urlunparse, urlencode, parse_qsl


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


def parseURL(value):
    parsed = urlparse(value)
    dt = dict(parse.parse_qsl(parse.urlsplit(value).query))

    additional0 = (
                    tools.check_is_none(parsed.scheme),
                    tools.check_is_none(parsed.netloc),
                    tools.check_is_none(parsed.hostname),
                    tools.check_is_none(parsed.path),
                    tools.check_is_none(parsed.port),
                    tools.check_is_none(parsed.params),
                    tools.check_is_none(parsed.fragment),
                    tools.check_is_none(parsed.username),
                    tools.check_is_none(parsed.password)
                  )

    additional1 = ()
    for d in dt:
        additional1 = additional1 + (d+"<=>"+dt[d],)

    return additional0 + additional1


def clean_url(url):
    parsed = urlparse(url)
    qd = parse_qsl(parsed.query, keep_blank_values=True)
    filtered = {}
    if parsed.hostname:
        hname = parsed.hostname
    else:
        hname = parsed.netloc
    for k, v in qd:
        if "youtube.com" in hname or "youtu.be" in hname:
            if not k.startswith(preset.youtube) and not k.startswith(preset.words):
                filtered.update([(k, v)])
        elif "facebook.com" in hname:
            if not k.startswith(preset.facebook) and not k.startswith(preset.words):
                filtered.update([(k, v)])
        elif not k.startswith(preset.words):
            filtered.update([(k, v)])

    newurl = urlunparse([
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        urlencode(filtered, doseq=True),
        parsed.fragment
    ])
    return newurl


def gettitle(url):
    #######################################################################################
    # TODO: If not enabled, returns current name or url
    #######################################################################################
    try:
        #######################################################################################
        # TODO: Place timeout in a settings file
        #######################################################################################
        with urlopen(url, timeout=120) as stream:
            data = stream.read()
    except HTTPError as error:
        err = str(error)
        err = err.replace("<", "[").replace(">", "]")
        return -2, "HTTPError - " + err
    except URLError as error:
        err = str(error)
        err = err.replace("<", "[").replace(">", "]")
        return -2, "URLError - " + err
    except timeout as error:
        err = str(error)
        err = err.replace("<", "[").replace(">", "]")
        return -2, "Timeout - " + err
    except Exception as e:
        return -1, "Unknown Exception: " + str(e)

    try:
        parser = Parser()
        decoded = data.decode('utf-8', errors='ignore')
        parser.feed(decoded)
        value = parser.title.replace('\n', '[n').replace('\t', '[t').strip()
        if len(value) > 0:
            return 0, value
        else:
            return -2, "NONAME - " + value
    except NotImplementedError as e:
        return -2, str(e) + " - " + url
    except Exception as e:
        return -1, "Unknown Exception: " + str(e)


'''
import lxml.html

from http import HTTPStatus
from http.client import RemoteDisconnected
from urllib.request import urlopen, Request


def get_title(url):
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
            return t.find(".//title").text.replace('\n', '[n').replace('\t', '[t')
        except Exception as e:
            tools.display("Exception:", str(e))
            return -1
'''

'''
from mechanize import Browser

def _get_title(url):
    response = ""
    try:
        br = Browser()
        br.open(url)
        response = br.title()
    except Exception as e:
        response = "request disallowed by robots: " + str(e)
    return (response)
'''

'''
from bs4 import BeautifulSoup

def url_title(url):
    soup = BeautifulSoup(urlopen("https://www.google.com"))
    return soup.title.string
'''
