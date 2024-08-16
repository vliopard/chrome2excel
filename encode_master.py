import preset
import chardet
import title_master
import urllib.request
from bs4 import UnicodeDammit

encodings = [
    'ASCII',
    'ISO-8859-1',
    'Johab'
    'Latin-1',
    'MacRoman',
    'UTF-8',
    'Windows-1251',
    'windows-1254',
    'windows-1256',
             ]


def get_url_encoding(url_address):
    try:
        response = title_master.request_wrapper(url_address, header=title_master.headers)
        return chardet.detect(response.content)['encoding']
    except Exception:
        return None


def get_charset_hard(url_address, response_type=True):
    try:
        response = title_master.request_wrapper(url_address, header=title_master.headers)
        if response_type:
            res_type = response.content
        else:
            res_type = response.text
        soup = title_master.soup_wrapper(res_type, 'html.parser')
        meta_tag = soup.find('meta', attrs={'http-equiv': 'Content-Type'})
        charset = None
        if meta_tag and 'content' in meta_tag.attrs:
            content_value = meta_tag['content']
            charset = content_value.split('charset=')[-1] if 'charset=' in content_value else None
        return charset
    except Exception:
        return None


def get_html_codepage(url_address):
    try:
        response = title_master.request_wrapper(url_address, rfs=True, header=title_master.headers)
        inferred_codepage = response.encoding
        soup = title_master.soup_wrapper(response.content, 'html.parser')
        meta_charset = soup.find('meta', attrs={'charset': True})
        if meta_charset:
            inferred_codepage = meta_charset['charset']
        return inferred_codepage
    except Exception:
        return None


def get_url_encoding_dammit(url_address):
    try:
        response = title_master.request_wrapper(url_address, header=title_master.headers)
        content = UnicodeDammit(response.content)
        return content.original_encoding
    except Exception:
        return None


def get_url_unicode_dammit(url_address):
    try:
        response = title_master.request_wrapper(url_address, header=title_master.headers)
        dammit = title_master.soup_wrapper(UnicodeDammit(response.content, encodings).unicode_markup, "html.parser")
        return dammit.original_encoding
    except Exception:
        return None


def get_charset_complex(url_address):
    try:
        response = title_master.request_wrapper(url_address, rfs=True, header=title_master.headers)
        content_type = response.headers.get('Content-Type')
        if content_type:
            charset = content_type.split('charset=')[-1]
            if charset:
                return charset
        soup = title_master.soup_wrapper(response.content, 'html.parser')
        meta_charset = soup.find('meta', attrs={'charset': True})
        if meta_charset:
            return meta_charset['charset']
        charset = chardet.detect(response.content)['encoding']
        return charset
    except Exception:
        return None


def get_charset_complex_hardcode(url_address):
    try:
        response = title_master.request_wrapper(url_address, rfs=True, header=title_master.headers)
        content_type = response.headers.get('Content-Type')
        if content_type:
            charset = content_type.split('charset=')[-1]
            if charset:
                return charset
        content = response.content
        start_index = content.find(b'<meta charset=')
        if start_index != -1:
            end_index = content.find(b'"', start_index + 14)
            if end_index != -1:
                charset = content[start_index + 14:end_index].decode('ascii')
                return charset
        charset = chardet.detect(content)['encoding']
        return charset
    except Exception:
        return None


def get_url_encoding_meta(url_address):
    try:
        response = title_master.request_wrapper(url_address, header=title_master.headers)
        soup = title_master.soup_wrapper(response.content, 'html.parser')
        charset = soup.meta.get('charset')
        if not charset:
            content_type = soup.meta.get('content-type')
            if content_type and 'charset' in content_type:
                charset = content_type.split('charset=')[-1]
        return charset
    except Exception:
        return None


def get_charset_urllib_basic(url_address):
    try:
        response = urllib.request.urlopen(url_address, timeout=preset.TIMEOUT)
        return response.headers.get_content_charset()
    except Exception:
        return None


def get_charset_lambda(url_address):
    try:
        response = title_master.request_wrapper(url_address, header=title_master.headers)
        soup = title_master.soup_wrapper(response.content, 'html.parser')
        meta = soup.find_all('meta', {'http-equiv': lambda v: v and v.lower() == 'content-type'})
        charset = meta[0].get('charset') if meta else None
        return charset
    except Exception:
        return None


def get_encoding_master(url_address):
    answer = get_charset_hard(url_address)
    if answer:
        return answer
    answer = get_charset_hard(url_address, False)
    if answer:
        return answer
    answer = get_html_codepage(url_address)
    if answer:
        return answer
    answer = get_url_encoding_meta(url_address)
    if answer:
        return answer
    answer = get_url_encoding(url_address)
    if answer:
        return answer
    answer = get_url_encoding_dammit(url_address)
    if answer:
        return answer
    answer = get_url_unicode_dammit(url_address)
    if answer:
        return answer
    answer = get_charset_urllib_basic(url_address)
    if answer:
        return answer
    answer = get_charset_lambda(url_address)
    if answer:
        return answer
    answer = get_charset_complex_hardcode(url_address)
    if answer:
        return answer
    answer = get_charset_complex(url_address)
    if answer:
        return answer
    return preset.NO_TITLE
