from configparser import ConfigParser


def credentialss(source):
    """
    Get credentials from source file
    :param source: Source file
    :return selected credential
    """
    parser = ConfigParser()
    parser.read('config.ini')
    return parser['all'][source]