# -*- coding: UTF-8 -*-
""" Config File/settings module
"""

import ConfigParser


class Config(object):
    """ Save the amazon Alexa's keys
    """

    CONFIG_FILE = "config.ini"
    MAIN_SECTION = "main"
    FIELD_API_KEY_WEATHER = "weather_api_key"
    FIELD_API_KEY_ZIP_CODE = "zip_code"
    DATETIME_SECTION = 'datetime'
    FIELD_DATE_TIME_1_TIMEZONE = 'city_1_timezone'
    FIELD_DATE_TIME_1_LABEL = 'city_1_label'
    FIELD_DATE_TIME_2_TIMEZONE = 'city_2_timezone'
    FIELD_DATE_TIME_2_LABEL = 'city_2_label'

    def __init__(self):
        pass

    @staticmethod
    def get_config(section, key):
        """ Get a config value
        :param key: The key
        :return: string
        """

        config = ConfigParser.ConfigParser()
        config.read(Config.CONFIG_FILE)

        try:
            val = config.get(section, key)
        except ConfigParser.ParsingError as exception:
            print "Error: Cannot parse the config file for key: %s / %s!" %\
                  (key, exception.message)
            return ""
        except Exception as exception:
            print "Error: Invalid key %s, got %s!" % (key, exception.message)
            return ""

        return val
