# -*- coding: UTF-8 -*-
""" String Module
"""

import re


class String(object):
    """ String class
    """

    @staticmethod
    def ucwords(string):
        """Returns a string with the first character of each word in str
        capitalized, if that character is alphabetic."""
        return " " . join([w[0].upper() + w[1:]
                           for w in re.split(r'\s*', string)])
