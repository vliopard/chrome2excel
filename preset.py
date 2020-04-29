import os
from platform import system
from tools import add, to_date


words = (
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

youtube = (
    "sm",
    "time_continue",
    "feature",
    "app",
    "bpctr",
    "1c"
)

facebook = (
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

#######################################################################################
# TODO: CHANGE TO OBJECT AND RETURN A DICT
#######################################################################################


class Header:
    def __init__(self):
        pos = [-1]
        stub_date = to_date(13231709218000000)
        self._Folder_GUID = (None, add(pos))
        self._Folder_ID = (None, add(pos))
        self._Folder_Sync = (None, add(pos))
        self._Folder_Type = (None, add(pos))

        self._Folder_Added = (stub_date, add(pos))
        self._Folder_Modified = (stub_date, add(pos))
        self._Folder_visited = (stub_date, add(pos))

        self._Folder_Name = ("", add(pos))
        self._Folder_URL = ("", add(pos))

        self._URL_GUID = (None, add(pos))
        self._URL_ID = (None, add(pos))
        self._URL_Sync = (None, add(pos))
        self._URL_Type = (None, add(pos))

        self._URL_Added = (stub_date, add(pos))
        self._URL_Modified = (stub_date, add(pos))
        self._URL_Visited = (stub_date, add(pos))

        self._URL_Name = ("[no site name]", add(pos))
        self._URL_Clean = ("[no clean URL]", add(pos))
        self._URL = ("[no URL address]", add(pos))
        self._Scheme = (None, add(pos))
        self._Netloc = (None, add(pos))
        self._Hostname = ("[no hostname]", add(pos))
        self._Path = (None, add(pos))
        self._Port = (None, add(pos))
        self._Param = (None, add(pos))
        self._Fragment = (None, add(pos))
        self._Username = ("", add(pos))
        self._Password = ("", add(pos))

        self._ParamA = (None, add(pos))
        self._ParamB = (None, add(pos))
        self._ParamC = (None, add(pos))
        self._ParamD = (None, add(pos))
        self._ParamE = (None, add(pos))
        self._ParamF = (None, add(pos))
        self._ParamG = (None, add(pos))
        self._ParamH = (None, add(pos))
        self._ParamI = (None, add(pos))
        self._ParamJ = (None, add(pos))
        self._ParamK = (None, add(pos))
        self._ParamL = (None, add(pos))
        self._ParamM = (None, add(pos))
        self._ParamN = (None, add(pos))
        self._ParamO = (None, add(pos))
        self._ParamP = (None, add(pos))

    def setData(self, dataHeader):
        pos = [-1]

        self._Folder_GUID = (dataHeader[add(pos)], pos[0])  # 00
        self._Folder_ID = (dataHeader[add(pos)], pos[0])  # 01
        self._Folder_Sync = (dataHeader[add(pos)], pos[0])  # 02
        self._Folder_Type = (dataHeader[add(pos)], pos[0])  # 03

        self._Folder_Added = (dataHeader[add(pos)], pos[0])  # 04
        self._Folder_Modified = (dataHeader[add(pos)], pos[0])  # 05
        self._Folder_visited = (dataHeader[add(pos)], pos[0])  # 06

        self._Folder_Name = (dataHeader[add(pos)], pos[0])  # 07
        self._Folder_URL = (dataHeader[add(pos)], pos[0])  # 08

        self._URL_GUID = (dataHeader[add(pos)], pos[0])  # 09
        self._URL_ID = (dataHeader[add(pos)], pos[0])  # 10
        self._URL_Sync = (dataHeader[add(pos)], pos[0])  # 11
        self._URL_Type = (dataHeader[add(pos)], pos[0])  # 12

        self._URL_Added = (dataHeader[add(pos)], pos[0])  # 13
        self._URL_Modified = (dataHeader[add(pos)], pos[0])  # 14
        self._URL_Visited = (dataHeader[add(pos)], pos[0])  # 15

        self._URL_Name = (dataHeader[add(pos)], pos[0])  # 16
        self._URL_Clean = (dataHeader[add(pos)], pos[0])  # 17
        self._URL = (dataHeader[add(pos)], pos[0])  # 18
        self._Scheme = (dataHeader[add(pos)], pos[0])  # 19
        self._Netloc = (dataHeader[add(pos)], pos[0])  # 20
        self._Hostname = (dataHeader[add(pos)], pos[0])  # 21
        self._Path = (dataHeader[add(pos)], pos[0])  # 22
        self._Port = (dataHeader[add(pos)], pos[0])  # 23
        self._Param = (dataHeader[add(pos)], pos[0])  # 24
        self._Fragment = (dataHeader[add(pos)], pos[0])  # 25
        self._Username = (dataHeader[add(pos)], pos[0])  # 26
        self._Password = (dataHeader[add(pos)], pos[0])  # 27

        self._ParamA = (dataHeader[add(pos)], pos[0])  # 28
        self._ParamB = (dataHeader[add(pos)], pos[0])  # 29
        self._ParamC = (dataHeader[add(pos)], pos[0])  # 30
        self._ParamD = (dataHeader[add(pos)], pos[0])  # 31
        self._ParamE = (dataHeader[add(pos)], pos[0])  # 32
        self._ParamF = (dataHeader[add(pos)], pos[0])  # 33
        self._ParamG = (dataHeader[add(pos)], pos[0])  # 34
        self._ParamH = (dataHeader[add(pos)], pos[0])  # 35
        self._ParamI = (dataHeader[add(pos)], pos[0])  # 36
        self._ParamJ = (dataHeader[add(pos)], pos[0])  # 37
        self._ParamK = (dataHeader[add(pos)], pos[0])  # 38
        self._ParamL = (dataHeader[add(pos)], pos[0])  # 39
        self._ParamM = (dataHeader[add(pos)], pos[0])  # 40
        self._ParamN = (dataHeader[add(pos)], pos[0])  # 41
        self._ParamO = (dataHeader[add(pos)], pos[0])  # 42
        self._ParamP = (dataHeader[add(pos)], pos[0])  # 43


#######################################################################################
# TODO: MUST SET DATES AS DATES (INVOKE CONVERTER)
#######################################################################################

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

    def getPos(self, position):
        item = self.toTuple()
        return item[position][0]

    def getName(self, name):
        item = self.toDict()
        return item['_'+name][0]

    def toDict(self):
        dc = self.__dict__
        dic = {}
        for x in dc:
            dic.update({x: dc[x][0]})
        return dic

    def toTuple(self):
        dc = self.__dict__
        tp = []
        for x in dc:
            tp.append(dc[x])
        tp.sort(key=lambda k: k[1])
        tpl = []
        for x in tp:
            tpl.append(x[0])
        return tuple(tpl)

    def toDictIdx(self):
        return self.__dict__

    def __repr__(self):
        return str(self.__dict__)


data_header = [
    (
        'Folder GUID',      # 00
        'Folder ID',        # 01
        'Folder Sync',      # 02
        'Type',             # 03

        'Folder Added',     # 04
        'Folder Modified',  # 05
        'Folder visited',   # 06

        'Folder Name',      # 07
        'Folder URL',       # 08

        'URL GUID',         # 09
        'URL ID',           # 10
        'URL Sync',         # 11
        'Type',             # 12

        'URL Added',        # 13
        'URL Modified',     # 14
        'URL Visited',      # 15

        'URL Name',         # 16
        'URL Clean',        # 17
        'URL',              # 18
        'Scheme',           # 19
        'Netloc',           # 20
        'Hostname',         # 21
        'Path',             # 22
        'Port',             # 23
        'Param',            # 24
        'Fragment',         # 25
        'Username',         # 26
        'Password',         # 27

        'ParamA',           # 28
        'ParamB',           # 29
        'ParamC',           # 30
        'ParamD',           # 31
        'ParamE',           # 32
        'ParamF',           # 33
        'ParamG',           # 34
        'ParamH',           # 35
        'ParamI',           # 36
        'ParamJ',           # 37
        'ParamK',           # 38
        'ParamL',           # 39
        'ParamM',           # 40
        'ParamN',           # 41
        'ParamO',           # 42
        'ParamP'            # 43
    )
]


def select_profile(profile_):
    profile_ = str(profile_)
    if profile_ == "0":
        profile_ = "Default"
    else:
        profile_ = "Profile "+profile_
    return profile_


def get_chrome_element(profile_, item):
    # item Preferences / Bookmarks
    computer = system()
    profile_ = select_profile(profile_)
    chrome_file = ""
    if computer == "Windows":
        chrome_file = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\" + profile_ + "\\" + item)
    if computer == "Linux":
        chrome_file = os.path.expanduser("~/.config/google-chrome/" + profile_ + "/" + item)
    if computer == "Darwin":
        chrome_file = os.path.expanduser("~/Library/Application Support/Google/Chrome/" + profile_ + "/" + item)
    if os.path.exists(chrome_file):
        return chrome_file
    return None
