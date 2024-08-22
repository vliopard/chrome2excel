import preset
import chardet
import title_master
import urllib.request
from bs4 import UnicodeDammit

encodings = [
    preset.CHARSET_ASCII,
    preset.CHARSET_ISO88591,
    preset.CHARSET_JOHAB,
    preset.CHARSET_LATIN1,
    preset.CHARSET_MACROMAN,
    preset.CHARSET_UTF8,
    preset.CHARSET_WINDOWS1251,
    preset.CHARSET_WINDOWS1254,
    preset.CHARSET_WINDOWS1256,
]


def get_url_encoding(url_address):
    try:
        response = title_master.request_wrapper(url_address, header=preset.HEADERS)
        return chardet.detect(response.content)[preset.ENCODING]
    except Exception:
        return None


def get_charset_hard(url_address, response_type=True):
    try:
        response = title_master.request_wrapper(url_address, header=preset.HEADERS)
        if response_type:
            res_type = response.content
        else:
            res_type = response.text
        soup = title_master.soup_wrapper(res_type, preset.HTML_PARSER)
        meta_tag = soup.find(preset.META, attrs={preset.HTTP_EQUIV: preset.CONTENT_TYPE})
        charset = None
        if meta_tag and preset.CONTENT in meta_tag.attrs:
            content_value = meta_tag[preset.CONTENT]
            charset = content_value.split(preset.CHARSET_EQ)[-1] if preset.CHARSET_EQ in content_value else None
        return charset
    except Exception:
        return None


def get_html_codepage(url_address):
    try:
        response = title_master.request_wrapper(url_address, rfs=True, header=preset.HEADERS)
        inferred_codepage = response.encoding
        soup = title_master.soup_wrapper(response.content, preset.HTML_PARSER)
        meta_charset = soup.find(preset.META, attrs={preset.CHARSET: True})
        if meta_charset:
            inferred_codepage = meta_charset[preset.CHARSET]
        return inferred_codepage
    except Exception:
        return None


def get_url_encoding_dammit(url_address):
    try:
        response = title_master.request_wrapper(url_address, header=preset.HEADERS)
        content = UnicodeDammit(response.content)
        return content.original_encoding
    except Exception:
        return None


def get_url_unicode_dammit(url_address):
    try:
        response = title_master.request_wrapper(url_address, header=preset.HEADERS)
        dammit = title_master.soup_wrapper(UnicodeDammit(response.content, encodings).unicode_markup, preset.HTML_PARSER)
        return dammit.original_encoding
    except Exception:
        return None


def get_charset_complex(url_address):
    try:
        response = title_master.request_wrapper(url_address, rfs=True, header=preset.HEADERS)
        content_type = response.headers.get(preset.CONTENT_TYPE)
        if content_type:
            charset = content_type.split(preset.CHARSET_EQ)[-1]
            if charset:
                return charset
        soup = title_master.soup_wrapper(response.content, preset.HTML_PARSER)
        meta_charset = soup.find(preset.META, attrs={preset.CHARSET: True})
        if meta_charset:
            return meta_charset[preset.CHARSET]
        charset = chardet.detect(response.content)[preset.ENCODING]
        return charset
    except Exception:
        return None


def get_charset_complex_hardcode(url_address):
    try:
        response = title_master.request_wrapper(url_address, rfs=True, header=preset.HEADERS)
        content_type = response.headers.get(preset.CONTENT_TYPE)
        if content_type:
            charset = content_type.split(preset.CHARSET_EQ)[-1]
            if charset:
                return charset
        content = response.content
        start_index = content.find(b'<meta charset=')
        if start_index != -1:
            end_index = content.find(b'"', start_index + 14)
            if end_index != -1:
                charset = content[start_index + 14:end_index].decode(preset.CHARSET_ASCII)
                return charset
        charset = chardet.detect(content)[preset.ENCODING]
        return charset
    except Exception:
        return None


def get_url_encoding_meta(url_address):
    try:
        response = title_master.request_wrapper(url_address, header=preset.HEADERS)
        soup = title_master.soup_wrapper(response.content, preset.HTML_PARSER)
        charset = soup.meta.get(preset.CHARSET)
        if not charset:
            content_type = soup.meta.get(preset.CONTENT_TYPE)
            if content_type and preset.CHARSET in content_type:
                charset = content_type.split(preset.CHARSET_EQ)[-1]
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
        response = title_master.request_wrapper(url_address, header=preset.HEADERS)
        soup = title_master.soup_wrapper(response.content, preset.HTML_PARSER)
        meta = soup.find_all(preset.META, {preset.HTTP_EQUIV: lambda v: v and v.lower() == preset.CONTENT_TYPE})
        charset = meta[0].get(preset.CHARSET) if meta else None
        return charset
    except Exception:
        return None


def get_encoding_master(url_address):
    debug = False
    print(f'get_encoding_master[{url_address}]') if debug else None
    answer = get_charset_hard(url_address)
    if answer:
        print(f'get_charset_hard[{answer}]') if debug else None
        return answer
    answer = get_charset_hard(url_address, False)
    if answer:
        print(f'get_charset_hard[{answer}]') if debug else None
        return answer
    answer = get_html_codepage(url_address)
    if answer:
        print(f'get_html_codepage[{answer}]') if debug else None
        return answer
    answer = get_url_encoding_meta(url_address)
    if answer:
        print(f'get_url_encoding_meta[{answer}]') if debug else None
        return answer
    answer = get_url_encoding(url_address)
    if answer:
        print(f'get_url_encoding[{answer}]') if debug else None
        return answer
    answer = get_url_encoding_dammit(url_address)
    if answer:
        print(f'get_url_encoding_dammit[{answer}]') if debug else None
        return answer
    answer = get_url_unicode_dammit(url_address)
    if answer:
        print(f'get_url_unicode_dammit[{answer}]') if debug else None
        return answer
    answer = get_charset_urllib_basic(url_address)
    if answer:
        print(f'get_charset_urllib_basic[{answer}]') if debug else None
        return answer
    answer = get_charset_lambda(url_address)
    if answer:
        print(f'get_charset_lambda[{answer}]') if debug else None
        return answer
    answer = get_charset_complex_hardcode(url_address)
    if answer:
        print(f'get_charset_complex_hardcode[{answer}]') if debug else None
        return answer
    answer = get_charset_complex(url_address)
    if answer:
        print(f'get_charset_complex[{answer}]') if debug else None
        return answer
    print(f'get_encoding_master[{preset.NO_TITLE}]') if debug else None
    return preset.NO_TITLE
