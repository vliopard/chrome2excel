import json
import tools
import preset

from argparse import ArgumentParser


def get_user(user_path):
    user_name = json.loads(open(user_path, encoding='utf-8').read())["account_info"][0]
    return user_name['email'], user_name['full_name'], user_name['given_name']


def retrieve_profile(profile):
    user_data = tools.get_chrome_element(profile, preset.preferences)
    if not user_data:
        raise Exception(preset.message["invalid_profile"])
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
    if profile == preset.all_profiles:
        for number in range(0, 100):
            try:
                email, full_name, display_name = retrieve_profile(number)
                if len(full_name) < 20:
                    tab = preset.tab
                else:
                    tab = preset.empty
                tools.display(preset.message["user"] + "[" + str(number) + "]: {", full_name, "}" + preset.tab + tab + " [", email, "]")
            except Exception:
                pass
    else:
        try:
            email, full_name, display_name = retrieve_profile(profile)
            tools.display(preset.message["user"] + ": {", full_name, "} [" + email + "]")
        except Exception as error:
            tools.display(error)


if __name__ == "__main__":
    argument_parser = ArgumentParser(
        description=preset.message["profile_description"]
    )
    argument_parser.add_argument(
        "--profile",
        "-p",
        help=preset.message["profile_help"],
        default=preset.all_profiles
    )

    arguments = vars(argument_parser.parse_args())
    get_profile(**arguments)
