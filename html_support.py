import utils
import preset
import database
import title_master
from urllib import parse
from urllib.parse import urlparse


def get_fld_fast(url_value):
    if url_value == preset.PDF:
        return preset.ARCHIVE_PDF
    elif url_value == preset.FTP_U:
        return preset.ARCHIVE_FTP
    elif url_value == preset.JSCRIPT:
        return preset.ARCHIVE_JAVASCRIPT
    elif url_value == preset.CHROMESETTINGS:
        return preset.CHROME_SETTINGS
    else:
        return title_master.get_title_master(f'{preset.PROTOCOL}{url_value}')


def get_stored_name(stored):
    item = database.get_item(stored)
    if item:
        return item[preset.FOLDER_INFO_NAME_PROPOSAL]
    new_item = title_master.get_title_master(stored)
    database.insert_item({preset.DATABASE_ID: stored, preset.FOLDER_INFO_NAME_PROPOSAL: new_item})
    return new_item


def get_stored_link(stored):
    item = database.get_name(stored)
    if item:
        return item[preset.URL_NAME]
    new_item = title_master.get_title_master(stored)
    database.insert_name({preset.DATABASE_ID: stored, preset.URL_NAME: new_item})
    return new_item


def parse_url(url_value):
    parsed_url = urlparse(url_value)
    dictionary = dict(parse.parse_qsl(parse.urlsplit(url_value).query))

    if preset.DIRECTORY_SUGGESTION:
        if url_value.lower().endswith(preset.EXT_PDF):
            dictionary[preset.URL_DATA_FLD] = preset.PDF
            dictionary[preset.FOLDER_INFO_NAME_PROPOSAL] = preset.ARCHIVE_PDF
        elif url_value.lower().endswith(preset.EXT_MP4):
            dictionary[preset.URL_DATA_FLD] = preset.MP4
            dictionary[preset.FOLDER_INFO_NAME_PROPOSAL] = preset.ARCHIVE_MP4
        elif url_value.lower().endswith(preset.EXT_PNG):
            dictionary[preset.URL_DATA_FLD] = preset.IMG
            dictionary[preset.FOLDER_INFO_NAME_PROPOSAL] = preset.ARCHIVE_IMG
        elif url_value.lower().endswith(preset.EXT_JPG):
            dictionary[preset.URL_DATA_FLD] = preset.IMG
            dictionary[preset.FOLDER_INFO_NAME_PROPOSAL] = preset.ARCHIVE_IMG
        elif url_value.lower().endswith(preset.EXT_JPEG):
            dictionary[preset.URL_DATA_FLD] = preset.IMG
            dictionary[preset.FOLDER_INFO_NAME_PROPOSAL] = preset.ARCHIVE_IMG
        elif url_value.lower().endswith(preset.EXT_GIF):
            dictionary[preset.URL_DATA_FLD] = preset.IMG
            dictionary[preset.FOLDER_INFO_NAME_PROPOSAL] = preset.ARCHIVE_IMG
        elif url_value.lower().endswith(preset.EXT_APK):
            dictionary[preset.URL_DATA_FLD] = preset.PRG
            dictionary[preset.FOLDER_INFO_NAME_PROPOSAL] = preset.ARCHIVE_PRG
        elif url_value.lower().endswith(preset.EXT_EXE):
            dictionary[preset.URL_DATA_FLD] = preset.PRG
            dictionary[preset.FOLDER_INFO_NAME_PROPOSAL] = preset.ARCHIVE_PRG
        elif url_value.lower().endswith(preset.EXT_MSI):
            dictionary[preset.URL_DATA_FLD] = preset.PRG
            dictionary[preset.FOLDER_INFO_NAME_PROPOSAL] = preset.ARCHIVE_PRG
        elif url_value.lower().endswith(preset.EXT_ZIP):
            dictionary[preset.URL_DATA_FLD] = preset.ZIP
            dictionary[preset.FOLDER_INFO_NAME_PROPOSAL] = preset.ARCHIVE_ZIP
        elif url_value.lower().endswith(preset.EXT_JAVA):
            dictionary[preset.URL_DATA_FLD] = preset.SRC
            dictionary[preset.FOLDER_INFO_NAME_PROPOSAL] = preset.ARCHIVE_SRC
        elif parsed_url.scheme.startswith(preset.FILE):
            dictionary[preset.URL_DATA_FLD] = preset.FTP_U
            dictionary[preset.FOLDER_INFO_NAME_PROPOSAL] = preset.ARCHIVE_FTP
        elif parsed_url.scheme.startswith(preset.JAVA):
            dictionary[preset.URL_DATA_FLD] = preset.JSCRIPT
            dictionary[preset.FOLDER_INFO_NAME_PROPOSAL] = preset.ARCHIVE_JAVASCRIPT
        elif parsed_url.scheme.startswith(preset.CHROME):
            dictionary[preset.URL_DATA_FLD] = preset.CHROMESETTINGS
            dictionary[preset.FOLDER_INFO_NAME_PROPOSAL] = preset.CHROME_SETTINGS
        else:
            dictionary[preset.URL_DATA_FLD] = title_master.parse_fld(parsed_url.netloc)
            dictionary[preset.FOLDER_INFO_NAME_PROPOSAL] = get_stored_name(dictionary[preset.URL_DATA_FLD])

    dictionary[preset.URL_DATA_SCHEME] = parsed_url.scheme
    dictionary[preset.URL_DATA_NETLOC] = parsed_url.netloc
    dictionary[preset.URL_DATA_HOSTNAME] = parsed_url.hostname
    dictionary[preset.URL_DATA_PATH] = parsed_url.path
    dictionary[preset.URL_DATA_PORT] = parsed_url.port
    dictionary[preset.URL_DATA_PARAMS] = parsed_url.params
    dictionary[preset.URL_DATA_FRAGMENT] = parsed_url.fragment
    dictionary[preset.URL_DATA_USERNAME] = parsed_url.username
    dictionary[preset.URL_DATA_PASSWORD] = parsed_url.password

    return dictionary


def split_qsl(s):
    parts = []
    for pair in s.split(preset.SYMBOL_AMP):
        key_value = pair.split(preset.SYMBOL_EQ, 1)
        parts.extend(key_value)
    return parts


def parse_qsl(query):
    tokens = {}
    if query.strip():
        items = query.split(preset.SYMBOL_AMP)
        for item in items:
            if preset.SYMBOL_EQ in item and not item.endswith(preset.SYMBOL_EQ):
                item_split = split_qsl(item)
                tokens[item_split[0]] = item_split[1]
            else:
                tokens[item] = preset.SYMBOL_EMPTY
    return tokens


def urlunparse(values):
    question = preset.SYMBOL_QM if values[3] or values[4] else preset.SYMBOL_EMPTY
    sharp = preset.SYMBOL_SHARP if values[5] else preset.SYMBOL_EMPTY
    double_slash = preset.SYMBOL_FORWARD_SLASHES
    if values[0] == preset.ABOUT:
        double_slash = preset.SYMBOL_EMPTY
    if values[3] and values[4]:
        retval = f'{values[0]}:{double_slash}{values[1]}{values[2]};{values[3]}?{values[4]}{sharp}{values[5]}'
    else:
        retval = f'{values[0]}:{double_slash}{values[1]}{values[2]}{question}{values[3]}{values[4]}{sharp}{values[5]}'
    return retval


def in_list(elem, elem_list):
    for item in elem_list:
        if item in elem:
            return True
    return False


def parse_url_clean(url_value):
    if not url_value.startswith(preset.JAVA):
        return_list = []
        dictionary = parse_qsl(parse.urlsplit(url_value).query)
        parsed_url = urlparse(url_value)
        for token in dictionary:
            url = parsed_url.hostname
            net_path = parsed_url.path

            if net_path == preset.PLAYLIST and preset.LIST in preset.dict_params[preset.WEBSITE_YOUTUBE_COM]:
                preset.dict_params[preset.WEBSITE_YOUTUBE_COM].remove(preset.LIST)
            elif preset.LIST not in preset.dict_params[preset.WEBSITE_YOUTUBE_COM]:
                preset.dict_params[preset.WEBSITE_YOUTUBE_COM].append(preset.LIST)

            key_res = utils.key_on_substring(preset.dict_params, url)
            if not utils.contains(token, preset.dict_params[key_res] + preset.dict_params[preset.TRACKING_MODULE] if key_res else preset.dict_params[preset.GENERAL] + preset.dict_params[preset.TRACKING_MODULE]):
                equals = preset.SYMBOL_EQ if dictionary[token] else preset.SYMBOL_EMPTY
                return_list.append(f'{token}{equals}{dictionary[token]}')

        qsl = preset.SYMBOL_AMP.join(return_list)
        net_lo = parsed_url.netloc.replace(preset.WEBSITE_YOUTUBE_M, preset.WEBSITE_YOUTUBE_WWW)
        frags = utils.check_fragment(parsed_url.fragment, net_lo)
        url_value = urlunparse((parsed_url.scheme, net_lo, parsed_url.path, parsed_url.params, qsl, frags))
        url_return = str(url_value)
        """
        quick_split = qsl.split(preset.AMP)
        qv = {}
        for qs in quick_split:
            qe = qs.split(preset.EQ, 1)
            if len(qe) > 1:
                qv[qe[0]] = qe[1]
            elif qe[0]:
                qv[qe[0]] = preset.EMPTY

        not_starts = not url_backup.startswith(url_return)
        not_equal = url_backup != url_return
        mlist = [
            'mercadolivre',
            'youtube',
            'twitter',
            'instagram',
            'facebook',
            'uol',
            'estadao',
            'folha',
            'globo',
        ]
        sites_in = in_list(host_netloc, mlist)

        if url_backup and not_equal and not sites_in and not qv:
            print(f'url_backup[{url_backup}]')
            print(f'url_return[{url_return}]')
            # print(f'url_split [{url_split}]')
            print(f'url_query [{url_query}]')
            # print(f'url_qsl   [{url_qsl}]')
            print(f'dictionary[{dictionary}]')
            print(f'qsl       [{qv}]')
            print(f'frags     [{parsed_url.fragment}]')
            print(f'frags     [{frags}]')
        """
        return url_return.strip()
    return url_value.strip()


"""
def clean_url(url_address):
    url_parsed = urlparse(url_address)
    qsl_parsed = parse.parse_qsl(url_parsed.query, keep_blank_values=True)
    filtered_parameters = {}
    if url_parsed.hostname:
        host_name = url_parsed.hostname
    else:
        host_name = url_parsed.netloc
    for key, value in qsl_parsed:
        if preset.YOUTUBE_COM in host_name or preset.YOUTUBE in host_name:
            if not key.startswith(tuple(preset.dict_params[preset.YOUTUBE_COM])) and not key.startswith(tuple(preset.dict_params[preset.GENERAL])):
                filtered_parameters.update([(key, value)])
        elif preset.FACEBOOK_COM in host_name:
            if not key.startswith(tuple(preset.dict_params['facebook.com'])) and not key.startswith(tuple(preset.dict_params[preset.GENERAL])):
                filtered_parameters.update([(key, value)])
        elif not key.startswith(tuple(preset.dict_params[preset.GENERAL])):
            filtered_parameters.update([(key, value)])

    return urlunparse([
        url_parsed.scheme,
        url_parsed.netloc,
        url_parsed.path,
        url_parsed.params,
        urlencode(filtered_parameters, doseq=True),
        url_parsed.fragment
    ])
"""
