import os


def mkdirp(path):
    """Do ``mkdir -p {path}``"""
    if not os.path.isdir(path):
        os.makedirs(path)
