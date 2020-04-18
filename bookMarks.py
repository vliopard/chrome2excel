import json
import tools
import public

@public.add
class nobj:
    def __init__(self, date_visited, date_added, date_modified):
        self.date_visited = date_visited
        self.date_added = date_added
        self.date_modified = date_modified

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
        self.data = json.loads(open(path,encoding='utf-8').read())
        self.attrList = self.processRoots()
        self.urls = self.attrList["urls"]
        self.folders = self.attrList["folders"]

    def processRoots(self):
        attrList = {"urls" : [], "folders" : []}
        for key, value in json.loads(open(self.path,encoding='utf-8').read())["roots"].items():
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
