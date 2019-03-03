import socket
import requests

from paths import resource_path


def get_version():
    version = 'unkown'
    try:
        with open(resource_path('version.txt')) as f:
            version = f.readline()
    except Exception as e:
        print(e)
    return version


def is_outdated():
    socket.setdefaulttimeout(1)  # second
    version_url = "https://raw.githubusercontent.com/rgargente/dcsrosetta/master/version.txt"
    try:
        last_version = requests.get(version_url).text
        last_version = last_version.readline()
    except:
        return False  # Lets be conservative here
    return get_version() != last_version
