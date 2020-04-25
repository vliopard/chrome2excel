import os
import json
import tools

from argparse import ArgumentParser


def getUser(userpath):
    username = json.loads(open(userpath, encoding='utf-8').read())["account_info"][0]
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
            except Exception:
                found = False
                pass
    if not found:
        raise Exception("Invalid profile.")
    return email, full, name


def profile_list():
    user_list = []
    for x in range(0, 100):
        try:
            email, full, name = retrieve_profile(str(x))
            user_list.append([x, full + " - " + email])
        except Exception:
            pass
    return user_list


def get_profile(profile):
    if profile == "all":
        for x in range(0, 100):
            try:
                email, full, name = retrieve_profile(str(x))
                if len(full) < 20:
                    tab = "\t"
                else:
                    tab = ""
                tools.display("User[" + str(x) + "]: {", full, "}\t" + tab + " [", email, "]")
            except Exception:
                pass
    else:
        try:
            email, full, name = retrieve_profile(profile)
            tools.display("User: {", full, "} [" + email + "]")
        except Exception as e:
            tools.display(e)


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Script to list users from Google Chrome."
    )
    parser.add_argument(
        "--profile",
        "-p",
        help="Profile number to extract: 'all' is Default.",
        default="all"
    )

    args = vars(parser.parse_args())
    get_profile(**args)
