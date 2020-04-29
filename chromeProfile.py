import json
import tools
import preset

from argparse import ArgumentParser


def get_user(userpath):
    username = json.loads(open(userpath, encoding='utf-8').read())["account_info"][0]
    return username['email'], username['full_name'], username['given_name']


def retrieve_profile(profile_):
    user = preset.get_chrome_element(profile_, "Preferences")
    if not user:
        raise Exception("Invalid profile.")
    return get_user(user)


def profile_list():
    user_list = []
    for x in range(0, 100):
        try:
            email, full, name = retrieve_profile(x)
            user_list.append([x, full + " - " + email])
        except Exception:
            pass
    return user_list


def get_profile(profile):
    if profile == "all":
        for x in range(0, 100):
            try:
                email, full, name = retrieve_profile(x)
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
