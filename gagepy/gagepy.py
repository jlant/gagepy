# -*- coding: utf-8 -*-
"""
    gagepy.gagepy
    ~~~~~~~~~~~~~

    Main controller.

    :copyright: 2015 by Jeremiah Lant, see AUTHORS
    :license: United States Geological Survey (USGS), see LICENSE file for more details
"""

def hello(msg="World"):
    """Function that prints a message.

    :param msg: message to say
    :type msg: string
    :returns: string
    :raises: something

    .. note::
       You can note something here.

    .. warning::
       You can warn about something here.

    >>> hello()
    Hello World!
    >>> hello(msg="there")
    Hello there!
    """
    return "Hello {}!".format(msg)
