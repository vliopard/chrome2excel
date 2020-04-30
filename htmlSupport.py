import tools
import utils
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


def parse_url(url_value):
    parsed_url = urlparse(url_value)
    dictionary = dict(parse.parse_qsl(parse.urlsplit(url_value).query))

    url_parameters = (
                    utils.check_is_none(parsed_url.scheme),
                    utils.check_is_none(parsed_url.netloc),
                    utils.check_is_none(parsed_url.hostname),
                    utils.check_is_none(parsed_url.path),
                    utils.check_is_none(parsed_url.port),
                    utils.check_is_none(parsed_url.params),
                    utils.check_is_none(parsed_url.fragment),
                    utils.check_is_none(parsed_url.username),
                    utils.check_is_none(parsed_url.password)
                  )

    qsl_parameters = ()
    for element in dictionary:
        qsl_parameters = qsl_parameters + (element + "<=>" + dictionary[element], )

    return url_parameters + qsl_parameters


def clean_url(url_address):
    url_parsed = urlparse(url_address)
    qsl_parsed = parse_qsl(url_parsed.query, keep_blank_values=True)
    filtered_parameters = {}
    if url_parsed.hostname:
        host_name = url_parsed.hostname
    else:
        host_name = url_parsed.netloc
    for key, value in qsl_parsed:
        if "youtube.com" in host_name or "youtu.be" in host_name:
            if not key.startswith(preset.youtube_parameters) and not key.startswith(preset.general_tracking_tokens):
                filtered_parameters.update([(key, value)])
        elif "facebook.com" in host_name:
            if not key.startswith(preset.facebook_tracking_tokens) and not key.startswith(preset.general_tracking_tokens):
                filtered_parameters.update([(key, value)])
        elif not key.startswith(preset.general_tracking_tokens):
            filtered_parameters.update([(key, value)])

    return urlunparse([
        url_parsed.scheme,
        url_parsed.netloc,
        url_parsed.path,
        url_parsed.params,
        urlencode(filtered_parameters, doseq=True),
        url_parsed.fragment
    ])


def get_title(url_address):
    #######################################################################################
    # TODO: If not enabled, returns current name or url
    #######################################################################################
    try:
        #######################################################################################
        # TODO: Place timeout in a settings file
        #######################################################################################
        with urlopen(url_address, timeout=120) as stream:
            url_data = stream.read()
    except HTTPError as error:
        error_message = str(error)
        error_message = error_message.replace("<", "[").replace(">", "]")
        return -2, "HTTPError - " + error_message
    except URLError as error:
        error_message = str(error)
        error_message = error_message.replace("<", "[").replace(">", "]")
        return -2, "URLError - " + error_message
    except timeout as error:
        error_message = str(error)
        error_message = error_message.replace("<", "[").replace(">", "]")
        return -2, "Timeout - " + error_message
    except Exception as error:
        return -1, preset.message["unknown_exception"] + str(error)

    try:
        url_parser = Parser()
        url_decoded = url_data.decode('utf-8', errors='ignore')
        url_parser.feed(url_decoded)
        url_value = url_parser.title.replace('\n', '¬').replace('\t', '§').strip()
        if len(url_value) > 0:
            return 0, url_value
        else:
            return -2, "NONAME - " + url_value
    except NotImplementedError as error:
        return -2, str(error) + " - " + url_address
    except Exception as error:
        return -1, preset.message["unknown_exception"] + str(error)


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
from bs4 import BeautifulSoup
def url_title(url):
    soup = BeautifulSoup(urlopen("https://www.google.com"))
    return soup.title.string
'''
