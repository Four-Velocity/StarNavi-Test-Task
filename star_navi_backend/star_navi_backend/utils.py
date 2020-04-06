import os
from time import sleep

import requests as r
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_yaml(tp: str) -> dict:
    """
    Convert YAML to python dict.
    Open dev_settings if exist.
    Other way open prod_settings.
    :param tp: category of settings which will be converted
    :return: dict with data
    """
    try:
        settings = os.path.join(BASE_DIR, "dev_settings.yml")
        with open(settings, 'r') as s:
            data = yaml.load(s, Loader=yaml.Loader)[tp]
    except FileNotFoundError:
        settings = os.path.join(BASE_DIR, "prod_settings.yml")
        with open(settings, 'r') as s:
            data = yaml.load(s, Loader=yaml.Loader)[tp]
    return data


def hard_get(data: dict, set_name: str):
    """
    Get settings value from a dict,
    Use when the setting required.
    :param data: dict with data
    :param set_name: setting name
    :return: setting value
    :raise: ValueError if value does not exist
    """
    try:
        value = data[set_name]
        return value
    except KeyError:
        raise ValueError(f"Provide value for {set_name.upper()}")


def soft_get(data: dict, set_name: str, tp: type):
    """
    Get setting value from a dict, or set it by default,
    Use when setting *not* required.
    :param data: dict with data
    :param set_name: setting name
    :param tp: value type
    :return: setting value
    """
    def default(val):
        defaults = dict(
            api_sleep=0.07,
            end_datetime=None,
            start_datetime=None,
            max_post_length=1024,
            image_generation=True,
            images_chance=0.333,
        )
        print(f"{val.upper()} value is being set from defaults!\n"
              "There is no such value in settings.yml, or it's incorrect")
        return defaults[val]

    try:
        value = data[set_name]
        if type(value) != tp:
            value = default(set_name)
    except KeyError:
        value = default(set_name)
    return value


API_SLEEP = soft_get(get_yaml('generator'), 'api_sleep', float)
ADORABLE_AVATAR = hard_get(get_yaml('project'), 'adorable_avatar')


def generate_adorable_avatar(email: str) -> str:
    """
    Generate user Adorable_avatar using email, and save it.
    Generally any string can be used
    :param email: user email
    :return: avatar uri
    """
    if ADORABLE_AVATAR:
        response = r.request('GET', rf'https://api.adorable.io/avatars/150/{email}')
        sleep(API_SLEEP)
        avatar = os.path.join(BASE_DIR, 'media', 'avatars', f'{email}.png')
        with open(avatar, 'wb') as img:
            img.write(response.content)
    else:
        avatar = None
    return avatar
