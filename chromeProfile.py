import os
import json

from argparse import ArgumentParser


def getUser(userpath):
    username = json.loads(open(userpath,encoding='utf-8').read())["account_info"][0]
    return username['email'], username['full_name'], username['given_name']


def retrieve_profile(profile_):
    if profile_ == "0":
        profile_ = "Default"
    else:
        profile_ = "Profile "+profile_

    user = [
        os.path.expanduser("~/.config/google-chrome/"+profile_+"/Preferences"),
        os.path.expanduser("~/Library/Application Support/Google/Chrome/"+profile_+"/Preferences"),
        os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\"+profile_+"\\Preferences")
    ]

    found = False
    for f in user:
        if os.path.exists(f):
            try:
                email, full, name = getUser(f)
                found = True
            except:
                found = False
                pass
    if not found:
        raise Exception("Invalid profile.")
    return email, full, name


def get_profile(profile):
    if profile == "all":
        for x in range(0, 100):
            try:
                email, full, name = retrieve_profile(str(x))
                if len(full) < 20:
                    tab = "\t"
                else:
                    tab = ""
                print("User[" + str(x) + "]: {", full, "}\t" + tab + " [", email, "]")
            except:
                exit(1)
    else:
        try:
            email, full, name = retrieve_profile(profile)
            print("User: {", full, "} [" + email + "]")
        except Exception as e:
            print (e)


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Script to extract bookmarks from Google Chrome to Microsoft Excel Spreadsheet."
    )
    parser.add_argument(
        "--profile",
        "-p",
        help="Profile number to extract: 'all' is Default.",
        default = "all"
    )

    args = vars(parser.parse_args())
    get_profile(**args)
