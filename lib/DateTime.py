# -*- coding: UTF-8 -*-
""" DateTime Module
"""

import datetime


class DateTime(object):
    """ DateTime class
    """

    @staticmethod
    def format(timestamp):
        """ Get the date using the following format: %Y-%m-%d %H:%M:%S
            :param timestamp: The timestamp
            :return string
        """
        return datetime.datetime.fromtimestamp(
            int(timestamp)
        ).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_hours_minutes(timestamp, format_24h=False):
        """ Get the hours and minutes using the following format:
                %H:%M or %I:%M
            :param timestamp: The timestamp
            :param format_24h: Use the 24h format
            :return string
        """
        hour_format = "%H" if format_24h else "%I"
        return datetime.datetime.fromtimestamp(
            int(timestamp)
        ).strftime(hour_format + ':%M')

    @staticmethod
    def get_day(timestamp):
        """ Get the day of a timestamp
            :param timestamp: The timestamp
            :return string
        """
        return datetime.datetime.fromtimestamp(
            int(timestamp)
        ).strftime('%A')

    @staticmethod
    def get_date(timestamp):
        """ Get the date using the following format: %Y-%m-%d
            :param timestamp: The timestamp
            :return string
        """
        return datetime.datetime.fromtimestamp(
            int(timestamp)
        ).strftime('%Y-%m-%d')

    @staticmethod
    def get_day_index(timestamp):
        """ Get the weekday number
            :param timestamp: The timestamp
            :return string
        """
        return datetime.datetime.fromtimestamp(
            int(timestamp)
        ).strftime('%w')
