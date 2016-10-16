# -*- coding: UTF-8 -*-
""" Web server
"""

from lib.Config import Config
from lib.News import News
from lib.Weather import Weather

from flask import Flask
from flask import send_from_directory
from flask import render_template
from os import path, getcwd

WEB_SERVER = Flask(__name__, static_url_path='')


@WEB_SERVER.route('/')
def root():
    """ Main page
        :return: string
    """

    # Weather
    zip_code = Config.get_config(
        Config.WEATHER_SECTION,
        Config.FIELD_API_KEY_ZIP_CODE
    )
    refresh_rate_weather = Config.get_config(
        Config.WEATHER_SECTION,
        Config.FIELD_REFRESH_RATE
    )

    # Get date and time
    extra_clocks_1 = {}
    extra_clocks_2 = {}

    clock_timezone_1 = Config.get_config(
        Config.DATETIME_SECTION,
        Config.FIELD_DATE_TIME_1_TIMEZONE
    )
    clock_label_1 = Config.get_config(
        Config.DATETIME_SECTION,
        Config.FIELD_DATE_TIME_1_LABEL
    )
    clock_timezone_2 = Config.get_config(
        Config.DATETIME_SECTION,
        Config.FIELD_DATE_TIME_2_TIMEZONE
    )
    clock_label_2 = Config.get_config(
        Config.DATETIME_SECTION,
        Config.FIELD_DATE_TIME_2_LABEL
    )

    if clock_timezone_1 != "":
        extra_clocks_1['timezone'] = clock_timezone_1
        extra_clocks_1['label'] = clock_label_1

    if clock_timezone_2 != "":
        extra_clocks_2['timezone'] = clock_timezone_2
        extra_clocks_2['label'] = clock_label_2

    # News
    refresh_rate_news = Config.get_config(
        Config.NEWS_SECTION,
        Config.FIELD_REFRESH_RATE
    )

    return render_template(
        'index.html',
        ZIP_CODE=zip_code,
        CLOCK_1=extra_clocks_1,
        CLOCK_2=extra_clocks_2,
        REFRESH_RATE_WEATHER=int(refresh_rate_weather),
        REFRESH_RATE_NEWS=int(refresh_rate_news)
    )


@WEB_SERVER.route('/static/<path:filename>')
def serve_static(filename):
    """ Static files (js, css)
        :return: string
    """
    root_dir = path.dirname(getcwd())
    return send_from_directory(path.join(root_dir, 'static', 'js'), filename)


# Ajax Calls

@WEB_SERVER.route('/weather/<int:post_id>')
def show_weather(post_id):
    """ Weather json output
        :return: string
    """
    return Weather.get_current_weather(post_id)


@WEB_SERVER.route('/forecast/<int:post_id>')
def show_forecast(post_id):
    """ Weather forecast json output
        :return: string
    """
    return Weather.get_forecast_weather(post_id)


@WEB_SERVER.route('/news/')
def show_news():
    """ News
        :return: string
    """

    news = News(10)
    return news.get_latest_news()


if __name__ == '__main__':

    if not Config.has_config():
        print "Unable to find config.ini file"
    else:
        WEB_SERVER.run(
            debug=True,
            host='0.0.0.0',
            threaded=True
        )
