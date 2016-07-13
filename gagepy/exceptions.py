# -*- coding: utf-8 -*-

"""
    gagepy.exceptions
    ~~~~~~~~~~~~~~~~~

    All exceptions for gagepy code base are defined here.

    :copyright: 2015 by Jeremiah Lant, see AUTHORS
    :license: United States Geological Survey (USGS), see LICENSE file
"""

class GagepyException(Exception):
    """
    Base exception class.  All gagepy custion exception subclass this class.
    """

class InvalidRDB(GagepyException):
    """
    Raised if the rdb file is not a valid rdb file.
    """
