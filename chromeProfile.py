import json
import tools
import preset

from argparse import ArgumentParser


def get_user(user_path):
    user_name = json.loads(open(user_path, encoding='utf-8').read())["account_info"][0]
    return user_name['email'], user_name['full_name'], user_name['given_name']


def retrieve_profile(profile):
    user_data = preset.get_chrome_element(profile, "Preferences")
    if not user_data:
        raise Exception("Invalid profile.")
    return get_user(user_data)


def profile_list():
    user_list = []
    for number in range(0, 100):
        try:
            email, full_name, display_name = retrieve_profile(number)
            user_list.append([number, full_name + " - " + email])
        except Exception:
            pass
    return user_list


def get_profile(profile):
    if profile == "all":
        for number in range(0, 100):
            try:
                email, full_name, display_name = retrieve_profile(number)
                if len(full_name) < 20:
                    tab = "\t"
                else:
                    tab = ""
                tools.display("User[" + str(number) + "]: {", full_name, "}\t" + tab + " [", email, "]")
            except Exception:
                pass
    else:
        try:
            email, full_name, display_name = retrieve_profile(profile)
            tools.display("User: {", full_name, "} [" + email + "]")
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
