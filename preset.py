import os
from tools import add


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
    def __init__(self, dataHeader):
        pos = [-1]

        self._Folder_GUID = dataHeader[add(pos)]  # 00
        self._Folder_ID = dataHeader[add(pos)]  # 01
        self._Folder_Sync = dataHeader[add(pos)]  # 02
        self._Type = dataHeader[add(pos)]  # 03

        self._Folder_Added = dataHeader[add(pos)]  # 04
        self._Folder_Modified = dataHeader[add(pos)]  # 05
        self._Folder_visited = dataHeader[add(pos)]  # 06

        self._Folder_Name = dataHeader[add(pos)]  # 07
        self._Folder_URL = dataHeader[add(pos)]  # 08

        self._URL_GUID = dataHeader[add(pos)]  # 09
        self._URL_ID = dataHeader[add(pos)]  # 10
        self._URL_Sync = dataHeader[add(pos)]  # 11
        self._Type = dataHeader[add(pos)]  # 12

        self._URL_Added = dataHeader[add(pos)]  # 13
        self._URL_Modified = dataHeader[add(pos)]  # 14
        self._URL_Visited = dataHeader[add(pos)]  # 15

        self._URL_Name = dataHeader[add(pos)]  # 16
        self._URL_Clean = dataHeader[add(pos)]  # 17
        self._URL = dataHeader[add(pos)]  # 18
        self._Scheme = dataHeader[add(pos)]  # 19
        self._Netloc = dataHeader[add(pos)]  # 20
        self._Hostname = dataHeader[add(pos)]  # 21
        self._Path = dataHeader[add(pos)]  # 22
        self._Port = dataHeader[add(pos)]  # 23
        self._Param = dataHeader[add(pos)]  # 24
        self._Fragment = dataHeader[add(pos)]  # 25
        self._Username = dataHeader[add(pos)]  # 26
        self._Password = dataHeader[add(pos)]  # 27

        self._ParamA = dataHeader[add(pos)]  # 28
        self._ParamB = dataHeader[add(pos)]  # 29
        self._ParamC = dataHeader[add(pos)]  # 30
        self._ParamD = dataHeader[add(pos)]  # 31
        self._ParamE = dataHeader[add(pos)]  # 32
        self._ParamF = dataHeader[add(pos)]  # 33
        self._ParamG = dataHeader[add(pos)]  # 34
        self._ParamH = dataHeader[add(pos)]  # 35
        self._ParamI = dataHeader[add(pos)]  # 36
        self._ParamJ = dataHeader[add(pos)]  # 37
        self._ParamK = dataHeader[add(pos)]  # 38
        self._ParamL = dataHeader[add(pos)]  # 39
        self._ParamM = dataHeader[add(pos)]  # 40
        self._ParamN = dataHeader[add(pos)]  # 41
        self._ParamO = dataHeader[add(pos)]  # 42
        self._ParamP = dataHeader[add(pos)]  # 43


#######################################################################################
# TODO: MUST SET DATES AS DATES (INVOKE CONVERTER)
#######################################################################################
# TODO: MUST RETURN ATTRIBUTE FROM INDEX NUMBER
#######################################################################################

    @property
    def Folder_GUID(self):
        return self._Folder_GUID

    @Folder_GUID.setter
    def Folder_GUID(self, Folder_GUID):
        self._Folder_GUID = Folder_GUID

    @property
    def Folder_ID(self):
        return self._Folder_ID

    @Folder_ID.setter
    def Folder_ID(self, Folder_ID):
        self._Folder_ID = Folder_ID

    @property
    def Folder_Sync(self):
        return self._Folder_Sync

    @Folder_Sync.setter
    def Folder_Sync(self, Folder_Sync):
        self._Folder_Sync = Folder_Sync

    @property
    def Type(self):
        return self._Type

    @Type.setter
    def Type(self, Type):
        self._Type = Type

    @property
    def Folder_Added(self):
        return self._Folder_Added

    @Folder_Added.setter
    def Folder_Added(self, Folder_Added):
        self._Folder_Added = Folder_Added

    @property
    def Folder_Modified(self):
        return self._Folder_Modified

    @Folder_Modified.setter
    def Folder_Modified(self, Folder_Modified):
        self._Folder_Modified = Folder_Modified

    @property
    def Folder_visited(self):
        return self._Folder_visited

    @Folder_visited.setter
    def Folder_visited(self, Folder_visited):
        self._Folder_visited = Folder_visited

    @property
    def Folder_Name(self):
        return self._Folder_Name

    @Folder_Name.setter
    def Folder_Name(self, Folder_Name):
        self._Folder_Name = Folder_Name

    @property
    def Folder_URL(self):
        return self._Folder_URL

    @Folder_URL.setter
    def Folder_URL(self, Folder_URL):
        self._Folder_URL = Folder_URL

    @property
    def URL_GUID(self):
        return self._URL_GUID

    @URL_GUID.setter
    def URL_GUID(self, URL_GUID):
        self._URL_GUID = URL_GUID

    @property
    def URL_ID(self):
        return self._URL_ID

    @URL_ID.setter
    def URL_ID(self, URL_ID):
        self._URL_ID = URL_ID

    @property
    def URL_Sync(self):
        return self._URL_Sync

    @URL_Sync.setter
    def URL_Sync(self, URL_Sync):
        self._URL_Sync = URL_Sync

    @property
    def Type(self):
        return self._Type

    @Type.setter
    def Type(self, Type):
        self._Type = Type

    @property
    def URL_Added(self):
        return self._URL_Added

    @URL_Added.setter
    def URL_Added(self, URL_Added):
        self._URL_Added = URL_Added

    @property
    def URL_Modified(self):
        return self._URL_Modified

    @URL_Modified.setter
    def URL_Modified(self, URL_Modified):
        self._URL_Modified = URL_Modified

    @property
    def URL_Visited(self):
        return self._URL_Visited

    @URL_Visited.setter
    def URL_Visited(self, URL_Visited):
        self._URL_Visited = URL_Visited

    @property
    def URL_Name(self):
        return self._URL_Name

    @URL_Name.setter
    def URL_Name(self, URL_Name):
        self._URL_Name = URL_Name

    @property
    def URL_Clean(self):
        return self._URL_Clean

    @URL_Clean.setter
    def URL_Clean(self, URL_Clean):
        self._URL_Clean = URL_Clean

    @property
    def URL(self):
        return self._URL

    @URL.setter
    def URL(self, URL):
        self._URL = URL

    @property
    def Scheme(self):
        return self._Scheme

    @Scheme.setter
    def Scheme(self, Scheme):
        self._Scheme = Scheme

    @property
    def Netloc(self):
        return self._Netloc

    @Netloc.setter
    def Netloc(self, Netloc):
        self._Netloc = Netloc

    @property
    def Hostname(self):
        return self._Hostname

    @Hostname.setter
    def Hostname(self, Hostname):
        self._Hostname = Hostname

    @property
    def Path(self):
        return self._Path

    @Path.setter
    def Path(self, Path):
        self._Path = Path

    @property
    def Port(self):
        return self._Port

    @Port.setter
    def Port(self, Port):
        self._Port = Port

    @property
    def Param(self):
        return self._Param

    @Param.setter
    def Param(self, Param):
        self._Param = Param

    @property
    def Fragment(self):
        return self._Fragment

    @Fragment.setter
    def Fragment(self, Fragment):
        self._Fragment = Fragment

    @property
    def Username(self):
        return self._Username

    @Username.setter
    def Username(self, Username):
        self._Username = Username

    @property
    def Password(self):
        return self._Password

    @Password.setter
    def Password(self, Password):
        self._Password = Password

    @property
    def ParamA(self):
        return self._ParamA

    @ParamA.setter
    def ParamA(self, ParamA):
        self._ParamA = ParamA

    @property
    def ParamB(self):
        return self._ParamB

    @ParamB.setter
    def ParamB(self, ParamB):
        self._ParamB = ParamB

    @property
    def ParamC(self):
        return self._ParamC

    @ParamC.setter
    def ParamC(self, ParamC):
        self._ParamC = ParamC

    @property
    def ParamD(self):
        return self._ParamD

    @ParamD.setter
    def ParamD(self, ParamD):
        self._ParamD = ParamD

    @property
    def ParamE(self):
        return self._ParamE

    @ParamE.setter
    def ParamE(self, ParamE):
        self._ParamE = ParamE

    @property
    def ParamF(self):
        return self._ParamF

    @ParamF.setter
    def ParamF(self, ParamF):
        self._ParamF = ParamF

    @property
    def ParamG(self):
        return self._ParamG

    @ParamG.setter
    def ParamG(self, ParamG):
        self._ParamG = ParamG

    @property
    def ParamH(self):
        return self._ParamH

    @ParamH.setter
    def ParamH(self, ParamH):
        self._ParamH = ParamH

    @property
    def ParamI(self):
        return self._ParamI

    @ParamI.setter
    def ParamI(self, ParamI):
        self._ParamI = ParamI

    @property
    def ParamJ(self):
        return self._ParamJ

    @ParamJ.setter
    def ParamJ(self, ParamJ):
        self._ParamJ = ParamJ

    @property
    def ParamK(self):
        return self._ParamK

    @ParamK.setter
    def ParamK(self, ParamK):
        self._ParamK = ParamK

    @property
    def ParamL(self):
        return self._ParamL

    @ParamL.setter
    def ParamL(self, ParamL):
        self._ParamL = ParamL

    @property
    def ParamM(self):
        return self._ParamM

    @ParamM.setter
    def ParamM(self, ParamM):
        self._ParamM = ParamM

    @property
    def ParamN(self):
        return self._ParamN

    @ParamN.setter
    def ParamN(self, ParamN):
        self._ParamN = ParamN

    @property
    def ParamO(self):
        return self._ParamO

    @ParamO.setter
    def ParamO(self, ParamO):
        self._ParamO = ParamO

    @property
    def ParamP(self):
        return self._ParamP

    @ParamP.setter
    def ParamP(self, ParamP):
        self._ParamP = ParamP

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


def getProfile(profile_):
    profile_ = str(profile_)
    if profile_ == "0":
        profile_ = "Default"
    else:
        profile_ = "Profile "+profile_
    return profile_


def retUser(profile_):
    profile_ = getProfile(profile_)
    return [
            os.path.expanduser("~/.config/google-chrome/"+profile_+"/Preferences"),
            os.path.expanduser("~/Library/Application Support/Google/Chrome/"+profile_+"/Preferences"),
            os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\"+profile_+"\\Preferences")
           ]


def retPath(profile_):
    profile_ = getProfile(profile_)
    return [
            os.path.expanduser("~/.config/google-chrome/"+profile_+"/Bookmarks"),
            os.path.expanduser("~/Library/Application Support/Google/Chrome/"+profile_+"/Bookmarks"),
            os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\"+profile_+"\\Bookmarks")
           ]

#######################################################################################
# TODO: Evaluate to change from tuple to Pandas DataFrame
#######################################################################################


'''

import pandas as pd

# df = pd.DataFrame([[1, 2, 3]], columns=["A", "B", "C"])

data = pd.read_pickle('data.pickle')

df = pd.DataFrame(data)

df1 = pd.DataFrame([[4, 5, 6],[7, 8, 9]], columns=["A", "B", "C"])

df = pd.concat([df, df1], ignore_index=True)

df2 = pd.DataFrame([['a', 'b', 'c'], ['d', 'e', 'f']], columns=["A", "B", "C"])

df = pd.concat([df, df2], ignore_index=True)

df.to_pickle('data.pickle')

'''
