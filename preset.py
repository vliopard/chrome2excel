import os


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

data_header = [
    ('Folder GUID',     #00
     'Folder ID',       #01
     'Folder Sync',     #02
     'Type',            #03

     'Folder Added',    #04
     'Folder Modified', #05
     'Folder visited',  #06

     'Folder Name',     #07
     'Folder URL',      #08

     'URL GUID',        #09
     'URL ID',          #10
     'URL Sync',        #11
     'Type',            #12

     'URL Added',       #13
     'URL Modified',    #14
     'URL Visited',     #15

     'URL Name',        #16
     'URL Clean',       #17
     'URL',             #18
     'Scheme',          #19
     'Netloc',          #20
     'Hostname',        #21
     'Path',            #22
     'Port',            #23
     'Param',           #24
     'Fragment',        #25
     'Username',        #26
     'Password',        #27

     'ParamA',          #28
     'ParamB',          #29
     'ParamC',          #30
     'ParamD',          #31
     'ParamE',          #32
     'ParamF',          #33
     'ParamG',          #34
     'ParamH',          #35
     'ParamI',          #36
     'ParamJ',          #37
     'ParamK',          #38
     'ParamL',          #39
     'ParamM',          #40
     'ParamN',          #41
     'ParamO',          #42
     'ParamP'           #43
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
