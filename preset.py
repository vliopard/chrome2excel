from json import load
from pathlib import Path

from utils import add, to_date


def load_translation_file():
    return load(Path("translation.json").open(encoding="utf-8"))


configuration_filename = "config.ini"
main_section = 'main'

debug_mode = False
text_filename = "chrome.txt"
html_filename = "chrome.html"
xlsx_filename = "chrome.xlsx"

english = 'en-us'
message = load_translation_file()[english]

on = 'on'
off = 'off'
empty = ""
blank = " "
all_profiles = "all"

protocol = "http://"

preferences = "Preferences"
bookmarks = "Bookmarks"

tab = "\t"
new_line = "\n"

underline = "_"
overline = "\u203e"

no_host_name = "[no hostname]"
no_site_name = "[no site name]"
no_clean_url = "[no clean URL]"
no_url_address = "[no URL address]"

label_date_added = "Date Added"
label_date_modified = "Date Modified"
label_date_visited = "Date Visited"
label_url_name = "URL Name"
label_url_clean = "URL Clean"
label_original_url = "URL Address"
label_url_hostname = "Hostname"
label_folder_name = "Folder"

children = 'children'
meta_info = 'meta_info'
last_visited = 'last_visited'
date_added = 'date_added'
date_modified = 'date_modified'
guid = 'guid'
icon = 'icon'
item_id = 'id'
item_name = 'name'
sync_transaction_version = 'sync_transaction_version'
item_type = 'type'
url = 'url'

no_date = "No Date"
empty_string = '[Empty]'
date_format = "%Y/%m/%d %H:%M:%S"
number_format = "YYYY/MM/DD hh:mm:ss"

system_language = "system_language"
export_file_type = "export_file_type"
refresh_url_title = "refresh_url_title"
remove_duplicated_urls = "remove_duplicated_urls"
remove_tracking_tokens_from_url = "remove_tracking_tokens_from_url"
import_urls_from_text_file = "import_urls_from_text_file"
refresh_folder_name_with_hostname_title = "refresh_folder_name_with_hostname_title"

general_tracking_tokens = (
        "__twitter_impression",
        "bffb",
        "client_id",
        "cmpid",
        "comment_id",
        "fb_action_ids",
        "fb_action_types",
        "fb_comment_id",
        "fbclid",
        "fbid",
        "notif_id",
        "notif_t",
        "reply_comment_id",
        "story_fbid",
        "total_comments",
        "campaign",
        "campanha",
        "gws_rd",
        "mkt_tok",
        "offset",
        "sc_campaign",
        "sc_category",
        "sc_channel",
        "sc_content",
        "sc_country",
        "sc_funnel",
        "sc_medium",
        "sc_publisher",
        "sc_segment",
        "utm_",
        "utm_campaign",
        "utm_content",
        "utm_medium",
        "utm_source",
        "utm_term"
)

youtube_parameters = (
        "sm",
        "time_continue",
        "feature",
        "app",
        "bpctr",
        "1c"
)

facebook_tracking_tokens = (
        "_rdc",
        "_rdr",
        "rc",
        "comment_tracking",
        "__tn__",
        "__xts__[0]",
        "__xts__",
        "sns",
        "hc_location",
        "pnref",
        "entry_point",
        "tab",
        "source_ref",
        "hc_ref",
        "__mref",
        "ref",
        "eid",
        "fref",
        "lst",
        "__nodl",
        "permPage",
        "notif_id"
)




def set_language(selected_language):
    global message
    message = load_translation_file()[selected_language]


def get_languages():
    language_list = []
    for language_item in load_translation_file():
        language_list.append(language_item)
    return language_list


class Header:
    def __init__(self):
        index = [-1]
        stub_date = to_date(13231709218000000)
        self._Folder_GUID = (empty, add(index))
        self._Folder_ID = (empty, add(index))
        self._Folder_Sync = (empty, add(index))
        self._Folder_Type = (empty, add(index))

        self._Folder_Added = (stub_date, add(index))
        self._Folder_Modified = (stub_date, add(index))
        self._Folder_visited = (stub_date, add(index))

        self._Folder_Name = (empty, add(index))
        self._Folder_URL = (empty, add(index))

        self._URL_GUID = (empty, add(index))
        self._URL_ID = (empty, add(index))
        self._URL_Sync = (empty, add(index))
        self._URL_Type = (empty, add(index))

        self._URL_Added = (stub_date, add(index))
        self._URL_Modified = (stub_date, add(index))
        self._URL_Visited = (stub_date, add(index))

        self._URL_Name = (no_site_name, add(index))
        self._URL_Clean = (no_clean_url, add(index))
        self._URL = (no_url_address, add(index))
        self._Scheme = (empty, add(index))
        self._Netloc = (empty, add(index))
        self._Hostname = (no_host_name, add(index))
        self._Path = (empty, add(index))
        self._Port = (empty, add(index))
        self._Param = (empty, add(index))
        self._Fragment = (empty, add(index))
        self._Username = (empty, add(index))
        self._Password = (empty, add(index))

        self._ParamA = (empty, add(index))
        self._ParamB = (empty, add(index))
        self._ParamC = (empty, add(index))
        self._ParamD = (empty, add(index))
        self._ParamE = (empty, add(index))
        self._ParamF = (empty, add(index))
        self._ParamG = (empty, add(index))
        self._ParamH = (empty, add(index))
        self._ParamI = (empty, add(index))
        self._ParamJ = (empty, add(index))
        self._ParamK = (empty, add(index))
        self._ParamL = (empty, add(index))
        self._ParamM = (empty, add(index))
        self._ParamN = (empty, add(index))
        self._ParamO = (empty, add(index))
        self._ParamP = (empty, add(index))

    def set_data(self, url_element):
        index = [-1]

        self._Folder_GUID = (url_element[add(index)], index[0])
        self._Folder_ID = (url_element[add(index)], index[0])
        self._Folder_Sync = (url_element[add(index)], index[0])
        self._Folder_Type = (url_element[add(index)], index[0])

        self._Folder_Added = (url_element[add(index)], index[0])
        self._Folder_Modified = (url_element[add(index)], index[0])
        self._Folder_visited = (url_element[add(index)], index[0])

        self._Folder_Name = (url_element[add(index)], index[0])
        self._Folder_URL = (url_element[add(index)], index[0])

        self._URL_GUID = (url_element[add(index)], index[0])
        self._URL_ID = (url_element[add(index)], index[0])
        self._URL_Sync = (url_element[add(index)], index[0])
        self._URL_Type = (url_element[add(index)], index[0])

        self._URL_Added = (url_element[add(index)], index[0])
        self._URL_Modified = (url_element[add(index)], index[0])
        self._URL_Visited = (url_element[add(index)], index[0])

        self._URL_Name = (url_element[add(index)], index[0])
        self._URL_Clean = (url_element[add(index)], index[0])
        self._URL = (url_element[add(index)], index[0])
        self._Scheme = (url_element[add(index)], index[0])
        self._Netloc = (url_element[add(index)], index[0])
        self._Hostname = (url_element[add(index)], index[0])
        self._Path = (url_element[add(index)], index[0])
        self._Port = (url_element[add(index)], index[0])
        self._Param = (url_element[add(index)], index[0])
        self._Fragment = (url_element[add(index)], index[0])
        self._Username = (url_element[add(index)], index[0])
        self._Password = (url_element[add(index)], index[0])

        self._ParamA = (url_element[add(index)], index[0])
        self._ParamB = (url_element[add(index)], index[0])
        self._ParamC = (url_element[add(index)], index[0])
        self._ParamD = (url_element[add(index)], index[0])
        self._ParamE = (url_element[add(index)], index[0])
        self._ParamF = (url_element[add(index)], index[0])
        self._ParamG = (url_element[add(index)], index[0])
        self._ParamH = (url_element[add(index)], index[0])
        self._ParamI = (url_element[add(index)], index[0])
        self._ParamJ = (url_element[add(index)], index[0])
        self._ParamK = (url_element[add(index)], index[0])
        self._ParamL = (url_element[add(index)], index[0])
        self._ParamM = (url_element[add(index)], index[0])
        self._ParamN = (url_element[add(index)], index[0])
        self._ParamO = (url_element[add(index)], index[0])
        self._ParamP = (url_element[add(index)], index[0])

    def get_position(self, position):
        item = self.to_tuple()
        return item[position]

    def get_name(self, name):
        item = self.to_dict()
        return item[underline + name][0]

    def to_list(self):
        dictionary = self.__dict__
        item_list = []
        for item in dictionary:
            item_list.append(dictionary[item])
        item_list.sort(key=lambda element: element[1])
        element_list = []
        for item in item_list:
            element_list.append(item[0])
        return element_list

    def to_dict(self):
        indexed_dictionary = self.__dict__
        dictionary = {}
        for element in indexed_dictionary:
            dictionary.update({element: indexed_dictionary[element][0]})
        return dictionary

    def to_tuple(self):
        dictionary = self.__dict__
        item_list = []
        for item in dictionary:
            item_list.append(dictionary[item])
        item_list.sort(key=lambda element: element[1])
        tuple_list = []
        for item in item_list:
            tuple_list.append(item[0])
        return tuple(tuple_list)

    def get_label(self, index):
        return label_dictionary[index]

    def to_dict_index(self):
        return self.__dict__

    def __repr__(self):
        return str(self.__dict__)

    @property
    def Folder_GUID(self):
        return self._Folder_GUID

    @Folder_GUID.setter
    def Folder_GUID(self, Folder_GUID):
        self._Folder_GUID = (Folder_GUID, self._Folder_GUID[1])

    @Folder_GUID.getter
    def Folder_GUID(self):
        return self._Folder_GUID[0]

    @property
    def Folder_ID(self):
        return self._Folder_ID

    @Folder_ID.setter
    def Folder_ID(self, Folder_ID):
        self._Folder_ID = (Folder_ID, self._Folder_ID[1])

    @Folder_ID.getter
    def Folder_ID(self):
        return self._Folder_ID[0]

    @property
    def Folder_Sync(self):
        return self._Folder_Sync

    @Folder_Sync.setter
    def Folder_Sync(self, Folder_Sync):
        self._Folder_Sync = (Folder_Sync, self._Folder_Sync[1])

    @Folder_Sync.getter
    def Folder_Sync(self):
        return self._Folder_Sync[0]

    @property
    def Folder_Type(self):
        return self._Folder_Type

    @Folder_Type.setter
    def Folder_Type(self, Folder_Type):
        self._Folder_Type = (Folder_Type, self._Folder_Type[1])

    @Folder_Type.getter
    def Folder_Type(self):
        return self._Folder_Type[0]

    @property
    def Folder_Added(self):
        return self._Folder_Added

    @Folder_Added.setter
    def Folder_Added(self, Folder_Added):
        self._Folder_Added = (Folder_Added, self._Folder_Added[1])

    @Folder_Added.getter
    def Folder_Added(self):
        return self._Folder_Added[0]

    @property
    def Folder_Modified(self):
        return self._Folder_Modified

    @Folder_Modified.setter
    def Folder_Modified(self, Folder_Modified):
        self._Folder_Modified = (Folder_Modified, self._Folder_Modified[1])

    @Folder_Modified.getter
    def Folder_Modified(self):
        return self._Folder_Modified[0]

    @property
    def Folder_visited(self):
        return self._Folder_visited

    @Folder_visited.setter
    def Folder_visited(self, Folder_visited):
        self._Folder_visited = (Folder_visited, self._Folder_visited[1])

    @Folder_visited.getter
    def Folder_visited(self):
        return self._Folder_visited[0]

    @property
    def Folder_Name(self):
        return self._Folder_Name

    @Folder_Name.setter
    def Folder_Name(self, Folder_Name):
        self._Folder_Name = (Folder_Name, self._Folder_Name[1])

    @Folder_Name.getter
    def Folder_Name(self):
        return self._Folder_Name[0]

    @property
    def Folder_URL(self):
        return self._Folder_URL

    @Folder_URL.setter
    def Folder_URL(self, Folder_URL):
        self._Folder_URL = (Folder_URL, self._Folder_URL[1])

    @Folder_URL.getter
    def Folder_URL(self):
        return self._Folder_URL[0]

    @property
    def URL_GUID(self):
        return self._URL_GUID

    @URL_GUID.setter
    def URL_GUID(self, URL_GUID):
        self._URL_GUID = (URL_GUID, self._URL_GUID[1])

    @URL_GUID.getter
    def URL_GUID(self):
        return self._URL_GUID[0]

    @property
    def URL_ID(self):
        return self._URL_ID

    @URL_ID.setter
    def URL_ID(self, URL_ID):
        self._URL_ID = (URL_ID, self._URL_ID[1])

    @URL_ID.getter
    def URL_ID(self):
        return self._URL_ID[0]

    @property
    def URL_Sync(self):
        return self._URL_Sync

    @URL_Sync.setter
    def URL_Sync(self, URL_Sync):
        self._URL_Sync = (URL_Sync, self._URL_Sync[1])

    @URL_Sync.getter
    def URL_Sync(self):
        return self._URL_Sync[0]

    @property
    def URL_Type(self):
        return self._URL_Type

    @URL_Type.setter
    def URL_Type(self, URL_Type):
        self._URL_Type = (URL_Type, self._URL_Type[1])

    @URL_Type.getter
    def URL_Type(self):
        return self._URL_Type[0]

    @property
    def URL_Added(self):
        return self._URL_Added

    @URL_Added.setter
    def URL_Added(self, URL_Added):
        self._URL_Added = (URL_Added, self._URL_Added[1])

    @URL_Added.getter
    def URL_Added(self):
        return self._URL_Added[0]

    @property
    def URL_Modified(self):
        return self._URL_Modified

    @URL_Modified.setter
    def URL_Modified(self, URL_Modified):
        self._URL_Modified = (URL_Modified, self._URL_Modified[1])

    @URL_Modified.getter
    def URL_Modified(self):
        return self._URL_Modified[0]

    @property
    def URL_Visited(self):
        return self._URL_Visited

    @URL_Visited.setter
    def URL_Visited(self, URL_Visited):
        self._URL_Visited = (URL_Visited, self._URL_Visited[1])

    @URL_Visited.getter
    def URL_Visited(self):
        return self._URL_Visited[0]

    @property
    def URL_Name(self):
        return self._URL_Name

    @URL_Name.setter
    def URL_Name(self, URL_Name):
        self._URL_Name = (URL_Name, self._URL_Name[1])

    @URL_Name.getter
    def URL_Name(self):
        return self._URL_Name[0]

    @property
    def URL_Clean(self):
        return self._URL_Clean

    @URL_Clean.setter
    def URL_Clean(self, URL_Clean):
        self._URL_Clean = (URL_Clean, self._URL_Clean[1])

    @URL_Clean.getter
    def URL_Clean(self):
        return self._URL_Clean[0]

    @property
    def URL(self):
        return self._URL

    @URL.setter
    def URL(self, URL):
        self._URL = (URL, self._URL[1])

    @URL.getter
    def URL(self):
        return self._URL[0]

    @property
    def Scheme(self):
        return self._Scheme

    @Scheme.setter
    def Scheme(self, Scheme):
        self._Scheme = (Scheme, self._Scheme[1])

    @Scheme.getter
    def Scheme(self):
        return self._Scheme[0]

    @property
    def Netloc(self):
        return self._Netloc

    @Netloc.setter
    def Netloc(self, Netloc):
        self._Netloc = (Netloc, self._Netloc[1])

    @Netloc.getter
    def Netloc(self):
        return self._Netloc[0]

    @property
    def Hostname(self):
        return self._Hostname

    @Hostname.setter
    def Hostname(self, Hostname):
        self._Hostname = (Hostname, self._Hostname[1])

    @Hostname.getter
    def Hostname(self):
        return self._Hostname[0]

    @property
    def Path(self):
        return self._Path

    @Path.setter
    def Path(self, Path):
        self._Path = (Path, self._Path[1])

    @Path.getter
    def Path(self):
        return self._Path[0]

    @property
    def Port(self):
        return self._Port

    @Port.setter
    def Port(self, Port):
        self._Port = (Port, self._Port[1])

    @Port.getter
    def Port(self):
        return self._Port[0]

    @property
    def Param(self):
        return self._Param

    @Param.setter
    def Param(self, Param):
        self._Param = (Param, self._Param[1])

    @Param.getter
    def Param(self):
        return self._Param[0]

    @property
    def Fragment(self):
        return self._Fragment

    @Fragment.setter
    def Fragment(self, Fragment):
        self._Fragment = (Fragment, self._Fragment[1])

    @Fragment.getter
    def Fragment(self):
        return self._Fragment[0]

    @property
    def Username(self):
        return self._Username

    @Username.setter
    def Username(self, Username):
        self._Username = (Username, self._Username[1])

    @Username.getter
    def Username(self):
        return self._Username[0]

    @property
    def Password(self):
        return self._Password

    @Password.setter
    def Password(self, Password):
        self._Password = (Password, self._Password[1])

    @Password.getter
    def Password(self):
        return self._Password[0]

    @property
    def ParamA(self):
        return self._ParamA

    @ParamA.setter
    def ParamA(self, ParamA):
        self._ParamA = (ParamA, self._ParamA[1])

    @ParamA.getter
    def ParamA(self):
        return self._ParamA[0]

    @property
    def ParamB(self):
        return self._ParamB

    @ParamB.setter
    def ParamB(self, ParamB):
        self._ParamB = (ParamB, self._ParamB[1])

    @ParamB.getter
    def ParamB(self):
        return self._ParamB[0]

    @property
    def ParamC(self):
        return self._ParamC

    @ParamC.setter
    def ParamC(self, ParamC):
        self._ParamC = (ParamC, self._ParamC[1])

    @ParamC.getter
    def ParamC(self):
        return self._ParamC[0]

    @property
    def ParamD(self):
        return self._ParamD

    @ParamD.setter
    def ParamD(self, ParamD):
        self._ParamD = (ParamD, self._ParamD[1])

    @ParamD.getter
    def ParamD(self):
        return self._ParamD[0]

    @property
    def ParamE(self):
        return self._ParamE

    @ParamE.setter
    def ParamE(self, ParamE):
        self._ParamE = (ParamE, self._ParamE[1])

    @ParamE.getter
    def ParamE(self):
        return self._ParamE[0]

    @property
    def ParamF(self):
        return self._ParamF

    @ParamF.setter
    def ParamF(self, ParamF):
        self._ParamF = (ParamF, self._ParamF[1])

    @ParamF.getter
    def ParamF(self):
        return self._ParamF[0]

    @property
    def ParamG(self):
        return self._ParamG

    @ParamG.setter
    def ParamG(self, ParamG):
        self._ParamG = (ParamG, self._ParamG[1])

    @ParamG.getter
    def ParamG(self):
        return self._ParamG[0]

    @property
    def ParamH(self):
        return self._ParamH

    @ParamH.setter
    def ParamH(self, ParamH):
        self._ParamH = (ParamH, self._ParamH[1])

    @ParamH.getter
    def ParamH(self):
        return self._ParamH[0]

    @property
    def ParamI(self):
        return self._ParamI

    @ParamI.setter
    def ParamI(self, ParamI):
        self._ParamI = (ParamI, self._ParamI[1])

    @ParamI.getter
    def ParamI(self):
        return self._ParamI[0]

    @property
    def ParamJ(self):
        return self._ParamJ

    @ParamJ.setter
    def ParamJ(self, ParamJ):
        self._ParamJ = (ParamJ, self._ParamJ[1])

    @ParamJ.getter
    def ParamJ(self):
        return self._ParamJ[0]

    @property
    def ParamK(self):
        return self._ParamK

    @ParamK.setter
    def ParamK(self, ParamK):
        self._ParamK = (ParamK, self._ParamK[1])

    @ParamK.getter
    def ParamK(self):
        return self._ParamK[0]

    @property
    def ParamL(self):
        return self._ParamL

    @ParamL.setter
    def ParamL(self, ParamL):
        self._ParamL = (ParamL, self._ParamL[1])

    @ParamL.getter
    def ParamL(self):
        return self._ParamL[0]

    @property
    def ParamM(self):
        return self._ParamM

    @ParamM.setter
    def ParamM(self, ParamM):
        self._ParamM = (ParamM, self._ParamM[1])

    @ParamM.getter
    def ParamM(self):
        return self._ParamM[0]

    @property
    def ParamN(self):
        return self._ParamN

    @ParamN.setter
    def ParamN(self, ParamN):
        self._ParamN = (ParamN, self._ParamN[1])

    @ParamN.getter
    def ParamN(self):
        return self._ParamN[0]

    @property
    def ParamO(self):
        return self._ParamO

    @ParamO.setter
    def ParamO(self, ParamO):
        self._ParamO = (ParamO, self._ParamO[1])

    @ParamO.getter
    def ParamO(self):
        return self._ParamO[0]

    @property
    def ParamP(self):
        return self._ParamP

    @ParamP.setter
    def ParamP(self, ParamP):
        self._ParamP = (ParamP, self._ParamP[1])

    @ParamP.getter
    def ParamP(self):
        return self._ParamP[0]


label_dictionary = {
                    "0": "Folder GUID",
                    "1": "Folder ID",
                    "2": "Folder Sync",
                    "3": "Type",

                    "4": "Folder Added",
                    "5": "Folder Modified",
                    "6": "Folder visited",

                    "7": "Folder Name",
                    "8": "Folder URL",

                    "9": "URL GUID",
                    "10": "URL ID",
                    "11": "URL Sync",
                    "12": "Type",

                    "13": "URL Added",
                    "14": "URL Modified",
                    "15": "URL Visited",

                    "16": "URL Name",
                    "17": "URL Clean",
                    "18": "URL",
                    "19": "Scheme",
                    "20": "Netloc",
                    "21": "Hostname",
                    "22": "Path",
                    "23": "Port",
                    "24": "Param",
                    "25": "Fragment",
                    "26": "Username",
                    "27": "Password",

                    "28": "ParamA",
                    "29": "ParamB",
                    "30": "ParamC",
                    "31": "ParamD",
                    "32": "ParamE",
                    "33": "ParamF",
                    "34": "ParamG",
                    "35": "ParamH",
                    "36": "ParamI",
                    "37": "ParamJ",
                    "38": "ParamK",
                    "39": "ParamL",
                    "40": "ParamM",
                    "41": "ParamN",
                    "42": "ParamO",
                    "43": "ParamP"

    }

data_header = []

trail = (
            blank,
            blank,
            blank,
            blank,
            blank,
            blank,
            blank,
            blank,
            blank,
            blank,
            blank,
            blank,
            blank,
            blank,
            blank,
            blank
        )
