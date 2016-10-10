# -*- coding: UTF-8 -*-
""" Web Module
"""

import urllib


class Web(object):
    """ Web class
    """

    @staticmethod
    def download(url, filename):
        """ Download a page to a file
            :param url: The url to download
            :param filename: The filename
        """
        urllib.urlretrieve(url, filename)
