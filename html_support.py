import utils
import preset
import database
import title_master
from urllib import parse
from urllib.parse import urlparse


def get_fld_fast(url_value):
    if url_value == 'PDF':
        return 'Archive (PDF)'
    elif url_value == 'FTP':
        return 'Archive (FTP)'
    elif url_value == 'JScript':
        return 'Archive (JavaScript)'
    elif url_value == 'ChromeSettings':
        return 'Chrome Settings'
    else:
        return title_master.get_title_master(f"http://{url_value}")


def get_stored_name(stored):
    item = database.get_item(stored)
    if item:
        return item['folder_info_name_proposal']
    new_item = title_master.get_title_master(stored)
    database.insert_item({'_id': stored, 'folder_info_name_proposal': new_item})
    return new_item


def get_stored_link(stored):
    item = database.get_name(stored)
    if item:
        return item['url_name']
    new_item = title_master.get_title_master(stored)
    database.insert_name({'_id': stored, 'url_name': new_item})
    return new_item


def parse_url(url_value):
    parsed_url = urlparse(url_value)
    dictionary = dict(parse.parse_qsl(parse.urlsplit(url_value).query))

    if url_value.lower().endswith('.pdf'):
        dictionary['url_data_fld'] = 'PDF'
        dictionary['folder_info_name_proposal'] = 'Archive (PDF)'
    elif url_value.lower().endswith('.mp4'):
        dictionary['url_data_fld'] = 'MP4'
        dictionary['folder_info_name_proposal'] = 'Archive (MP4)'
    elif url_value.lower().endswith('.png'):
        dictionary['url_data_fld'] = 'IMG'
        dictionary['folder_info_name_proposal'] = 'Archive (IMG)'
    elif url_value.lower().endswith('.jpg'):
        dictionary['url_data_fld'] = 'IMG'
        dictionary['folder_info_name_proposal'] = 'Archive (IMG)'
    elif url_value.lower().endswith('.jpeg'):
        dictionary['url_data_fld'] = 'IMG'
        dictionary['folder_info_name_proposal'] = 'Archive (IMG)'
    elif url_value.lower().endswith('.gif'):
        dictionary['url_data_fld'] = 'IMG'
        dictionary['folder_info_name_proposal'] = 'Archive (IMG)'
    elif url_value.lower().endswith('apk'):
        dictionary['url_data_fld'] = 'PRG'
        dictionary['folder_info_name_proposal'] = 'Archive (PRG)'
    elif url_value.lower().endswith('exe'):
        dictionary['url_data_fld'] = 'PRG'
        dictionary['folder_info_name_proposal'] = 'Archive (PRG)'
    elif url_value.lower().endswith('msi'):
        dictionary['url_data_fld'] = 'PRG'
        dictionary['folder_info_name_proposal'] = 'Archive (PRG)'
    elif url_value.lower().endswith('zip'):
        dictionary['url_data_fld'] = 'ZIP'
        dictionary['folder_info_name_proposal'] = 'Archive (ZIP)'
    elif url_value.lower().endswith('java'):
        dictionary['url_data_fld'] = 'SRC'
        dictionary['folder_info_name_proposal'] = 'Archive (SRC)'
    elif parsed_url.scheme.startswith('file'):
        dictionary['url_data_fld'] = 'FTP'
        dictionary['folder_info_name_proposal'] = 'Archive (FTP)'
    elif parsed_url.scheme.startswith('java'):
        dictionary['url_data_fld'] = 'JScript'
        dictionary['folder_info_name_proposal'] = 'Archive (JavaScript)'
    elif parsed_url.scheme.startswith('chrome'):
        dictionary['url_data_fld'] = 'ChromeSettings'
        dictionary['folder_info_name_proposal'] = 'Chrome Settings'
    else:
        dictionary['url_data_fld'] = title_master.parse_fld(parsed_url.netloc)
        dictionary['folder_info_name_proposal'] = get_stored_name(dictionary['url_data_fld'])

    dictionary['url_data_scheme'] = parsed_url.scheme
    dictionary['url_data_netloc'] = parsed_url.netloc
    dictionary['url_data_hostname'] = parsed_url.hostname
    dictionary['url_data_path'] = parsed_url.path
    dictionary['url_data_port'] = parsed_url.port
    dictionary['url_data_params'] = parsed_url.params
    dictionary['url_data_fragment'] = parsed_url.fragment
    dictionary['url_data_username'] = parsed_url.username
    dictionary['url_data_password'] = parsed_url.password

    return dictionary


def split_qsl(s):
    parts = []
    for pair in s.split('&'):
        key_value = pair.split('=', 1)
        parts.extend(key_value)
    return parts


def parse_qsl(query):
    tokens = {}
    if query.strip():
        items = query.split('&')
        for item in items:
            if '=' in item and not item.endswith('='):
                item_split = split_qsl(item)
                tokens[item_split[0]] = item_split[1]
            else:
                tokens[item] = ''
    return tokens


def urlunparse(values):
    question = '?' if values[3] or values[4] else ''
    sharp = '#' if values[5] else ''
    double_slash = '//'
    if values[0] == 'about':
        double_slash = ''
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
    if not url_value.startswith('java'):
        return_list = []
        dictionary = parse_qsl(parse.urlsplit(url_value).query)
        parsed_url = urlparse(url_value)
        for token in dictionary:
            url = parsed_url.hostname
            net_path = parsed_url.path

            if net_path == '/playlist' and 'list' in preset.dict_params['youtube.com']:
                preset.dict_params['youtube.com'].remove('list')
            elif 'list' not in preset.dict_params['youtube.com']:
                preset.dict_params['youtube.com'].append('list')

            key_res = utils.key_on_substring(preset.dict_params, url)
            if not utils.contains(token, preset.dict_params[key_res] + preset.dict_params['tracking_module'] if key_res else preset.dict_params['general'] + preset.dict_params['tracking_module']):
                equals = '=' if dictionary[token] else ''
                return_list.append(f'{token}{equals}{dictionary[token]}')

        qsl = '&'.join(return_list)
        net_lo = parsed_url.netloc.replace(preset.YOUTUBE_M, preset.YOUTUBE_WWW)
        frags = utils.check_fragment(parsed_url.fragment, net_lo)
        url_value = urlunparse((parsed_url.scheme,
                                net_lo,
                                parsed_url.path,
                                parsed_url.params,
                                qsl,
                                frags))
        url_return = str(url_value)
        """
        quick_split = qsl.split('&')
        qv = {}
        for qs in quick_split:
            qe = qs.split('=', 1)
            if len(qe) > 1:
                qv[qe[0]] = qe[1]
            elif qe[0]:
                qv[qe[0]] = ''

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
        return url_return
    return url_value


'''
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
            if not key.startswith(tuple(preset.dict_params['youtube.com'])) and not key.startswith(tuple(preset.dict_params['general'])):
                filtered_parameters.update([(key, value)])
        elif preset.FACEBOOK_COM in host_name:
            if not key.startswith(tuple(preset.dict_params['facebook.com'])) and not key.startswith(tuple(preset.dict_params['general'])):
                filtered_parameters.update([(key, value)])
        elif not key.startswith(tuple(preset.dict_params['general'])):
            filtered_parameters.update([(key, value)])

    return urlunparse([
        url_parsed.scheme,
        url_parsed.netloc,
        url_parsed.path,
        url_parsed.params,
        urlencode(filtered_parameters, doseq=True),
        url_parsed.fragment
    ])
'''
