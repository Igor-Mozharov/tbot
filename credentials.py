import os
from configparser import ConfigParser


def credentialss(source):
    # project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # config_path = os.path.join(project_root, 'config.ini')
    parser = ConfigParser()
    parser.read('config.ini')
    return parser['all'][source]