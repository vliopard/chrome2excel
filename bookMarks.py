import os
import json
import tools
import public
import preset
import htmlSupport


@public.add
class nobj:
    def __init__(self, element):
        self.date_added = element[0]
        self.date_modified = element[1]
        self.date_visited = element[2]
        self.url_name = element[3]
        self.url_clean = element[4]
        self.original_url = element[5]
        self.url_hostname = element[6]

    def save():
        pass


@public.add
class Item(dict):

    @property
    def id(self):
        return self["id"]

    @property
    def name(self):
        return self["name"]

    @property
    def type(self):
        return self["type"]

    @property
    def url(self):
        if "url" in self:
            return self["url"]
        return ""

    @property
    def icon(self):
        if "icon" in self:
            return self["icon"]
        return ""

    @property
    def added(self):
        return tools.dateFromWebkit(self["date_added"])

    @property
    def modified(self):
        if "date_modified" in self:
            return tools.dateFromWebkit(self["date_modified"])

    @property
    def folders(self):
        items = []
        for children in self["children"]:
            if children["type"] == "folder":
                items.append(Item(children))
        return items

    @property
    def urls(self):
        items = []
        for children in self["children"]:
            if children["type"] == "url":
                items.append(Item(children))
        return items


@public.add
class Bookmarks:
    path = None

    def __init__(self, path):
        self.path = path
        self.data = json.loads(open(path, encoding='utf-8').read())
        self.attrList = self.processRoots()
        self.urls = self.attrList["urls"]
        self.folders = self.attrList["folders"]

    def processRoots(self):
        attrList = {"urls": [], "folders": []}
        for key, value in json.loads(open(self.path, encoding='utf-8').read())["roots"].items():
            if "children" in value:
                self.processTree(attrList, value["children"])
        return attrList

    def processTree(self, attrList, childrenList):
        for item in childrenList:
            self.processUrls(item, attrList, childrenList)
            self.processFolders(item, attrList, childrenList)

    def processUrls(self, item, attrList, childrenList):
        if "type" in item and item["type"] == "url":
            attrList["urls"].append(Item(item))

    def processFolders(self, item, attrList, childrenList):
        if "type" in item and item["type"] == "folder":
            attrList["folders"].append(Item(item))
            if "children" in item:
                self.processTree(attrList, item["children"])


def read_content(content):
    data = []
    for chrome_url in content:
        date_added = '[Empty]'
        date_modified = '[Empty]'
        guid = '[Empty]'
        item_id = '[Empty]'
        last_visited = '[Empty]'
        name = '[Empty]'
        sync_transaction_version = '[Empty]'
        item_type = '[Empty]'
        url = '[Empty]'
        icon = '[Empty]'
        for x in chrome_url:
            if x == 'children':
                read_content(chrome_url[x])
            elif x == 'meta_info':
                for y in chrome_url[x]:
                    if y == 'last_visited':
                        last_visited = chrome_url[x][y]
            elif x == 'date_added':
                date_added = chrome_url[x]
            elif x == 'date_modified':
                date_modified = chrome_url[x]
            elif x == 'guid':
                guid = chrome_url[x]
            elif x == 'icon':
                # TODO: Add icon to the spreadsheet
                icon = chrome_url[x]
            elif x == 'id':
                item_id = chrome_url[x]
            elif x == 'name':
                name = chrome_url[x]
            elif x == 'sync_transaction_version':
                sync_transaction_version = chrome_url[x]
            elif x == 'type':
                item_type = chrome_url[x]
            elif x == 'url':
                url = chrome_url[x]
            else:
                tools.debug('WARNING: '+str(x))
        part1 = (
                 guid,
                 tools.toNumber(item_id),
                 tools.toNumber(sync_transaction_version),
                 item_type,

                 tools.toDate(date_added),
                 tools.toDate(date_modified),
                 tools.toDate(last_visited),

                 name,
                 htmlSupport.clean_url(url),
                 url
                )
        part2 = htmlSupport.parseURL(url)
        part3 = part1 + part2
        data.append(part3)
    return data


def generate_bookmarks(profile_):
    print("Generating bookmarks...")
    for f in preset.retPath(profile_):
        if os.path.exists(f):
            return Bookmarks(f)


def generate_data(instance):
    for folder in instance.folders:
        data = None
        f_date_added = '[Empty]'
        f_date_modified = '[Empty]'
        f_guid = '[Empty]'
        f_id = '[Empty]'
        f_last_visited = '[Empty]'
        f_name = '[Empty]'
        f_sync_transaction_version = '[Empty]'
        f_type = '[Empty]'
        f_url = '[Empty]'
        for x in folder:
            if x == 'children':
                data = read_content(folder[x])
            elif x == 'meta_info':
                for y in folder[x]:
                    if y == 'last_visited':
                        f_last_visited = folder[x][y]
            elif x == 'date_added':
                f_date_added = folder[x]
            elif x == 'date_modified':
                f_date_modified = folder[x]
            elif x == 'guid':
                f_guid = folder[x]
            elif x == 'id':
                f_id = folder[x]
            elif x == 'name':
                f_name = folder[x]
            elif x == 'sync_transaction_version':
                f_sync_transaction_version = folder[x]
            elif x == 'type':
                f_type = folder[x]
            elif x == 'url':
                f_url = folder[x]
            else:
                tools.debug('WARNING: '+str(x))
        f_data = (
                    f_guid,
                    tools.toNumber(f_id),
                    tools.toNumber(f_sync_transaction_version),
                    f_type,

                    tools.toDate(f_date_added),
                    tools.toDate(f_date_modified),
                    tools.toDate(f_last_visited),

                    f_name,
                    f_url
                 )

        for d in data:
            new_data = f_data + d
            preset.data_header.append(new_data)
    return preset.data_header
