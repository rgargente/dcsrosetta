import socket
import urllib


def get_version():
    with open('version.txt') as f:
        version = f.readline()
    return version


def is_outdated():
    socket.setdefaulttimeout(1)  # second
    version_url = "https://raw.githubusercontent.com/rgargente/dcsrosetta/master/version.txt"
    try:
        last_version = urllib.urlopen(version_url)
        last_version = last_version.readline()
    except:
        return False  # Lets be conservative here
    return get_version() != last_version
