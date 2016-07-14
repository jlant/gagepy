# -*- coding: utf-8 -*-

"""
    gagepy.utils
    ~~~~~~~~~~~~

    Utility helper functions for gagepy.

    :authors: 2016 by Jeremiah Lant, see AUTHORS
    :license: United States Geological Survey (USGS), see LICENSE file
"""

import os
import numpy as np
import datetime
import re


def get_file_paths(dirname, file_ext):
    """Return a list of absolute file paths for certain files files in a directory.  Walks through
    subdirectories.

    :param dirname: Name of directory to start walking
    :type dirname: string
    :param file_ext: File extension to look for
    :file_ext type: string
    :returns: List of absolute file paths
    :rtype: list
    """
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            if file_ext and filepath.endswith(file_ext):
                file_paths.append(filepath)

    return file_paths


def get_file_info(filepath):
    """Return a file's directory and name for a file path.

    :param filepath: Path to file
    :type filepath: string
    :returns: File directory and file name
    :type: tuple

    """
    filedir, filename = os.path.split(filepath)
    # filedir is an empty string when file is in current directory
    if not filedir:
        filedir = os.getcwd()

    return filedir, filename


def rmchars(value):
    """Remove special characters from alphanumeric values except for period (.)
    and negative (-) characters.

    :param value: Alphanumeric value
    :type value: string
    :returns: Alphanumeric value stripped of any special characters
    :rtype: string

    >>> import utils
    >>> utils.rmchars(value = "*6.5_")
    '6.5'
    >>> utils.rmchars(value = "ICE")
    'ICE'
    >>> utils.rmchars(value = "-4.2")
    '-4.2'
    >>> utils.rmchars(value = "%&!@#8.32&#*;")
    '8.32'
    """
    value = re.sub("[^A-Za-z0-9.-]+", "", value)
    return value


def is_float(value):
    """Return True if a string value can be converted to a float and False otherwise.

    :param value: Value to check
    :rtype: bool

    >>> import utils
    >>> utils.is_float(value = "2.5")
    True
    >>> utils.is_float(value = "hello world")
    False
    >>> utils.is_float(value = "5.5_")
    False
    """
    try:
        float(value)
        return True

    except ValueError:
        return False


def to_float(value):
    """Convert a value to a float type.

    :param value: Value to convert to float
    :returns: Value as a float
    :rtype: float

    """
    value = rmchars(value)
    if is_float(value):
        return float(value)
    else:
        raise ValueError("Can not convert {} value to a float".format(value))


def to_nan(value, msg=None):
    """Convert a value to a numpy nan and print a message if available.

    :param value: Value to convert to nan
    :type value:
    :param msg: Optional message to print to screen
    :returns: Numpy nan value
    :rtype: float
    """
    if msg:
        print(msg)
    return np.nan


def subset_data(dates, values, start_date, end_date):
    """Return a subset of date and value arrays to match the range of dates
    between a given start_date and end_date.  If start_date and end_date are not
    within the range of dates specified in dates, then the start_date and
    end_date are set to the first and last dates in the dates array.

    :param dates: Array of dates as datetime objects
    :type dates: numpy.ndarray
    :param values: Array of numeric values
    :type values: numpy.ndarray
    :param start_date: A datetime object
    :type start_date: datetime.datetime
    :param end_date: A datetime object
    :type end_date: datetime.datetime
    :returns: A subset of dates and values
    :rtype: tuple
    """
    if len(dates) != len(values):
        raise ValueError("Length of dates {} does not equal length of values {}".format(len(dates), len(values)))
    else:
        # if start_date or end_date are not within dates, set them to the first and last elements in dates
        if start_date < dates[0] or start_date > dates[-1]:
            start_date = dates[0]

        if end_date > dates[-1] or end_date < dates[0]:
            end_date = dates[-1]

        # find start and ending indices; have to convert idx from array to int to slice
        start_idx = int(np.where(dates == start_date)[0])
        end_idx = int(np.where(dates == end_date)[0])

        # subset variable and date range;
        date_subset = dates[start_idx:end_idx + 1]
        values_subset = values[start_idx:end_idx + 1]

        return date_subset, values_subset


def find_start_end_dates(dates1, dates2):
    """Find start and end dates between lists (or arrays) of datetime objects
    that do not have the same length.

    The start date will be the later of two dates.

    The end date will be the earlier of the two dates.

    :param dates1: List or array of datetime objects
    :type dates1: list or numpy.ndarray
    :param dates2: List or array of datetime objects
    :type dates2: list or numpy.ndarray
    :returns: Tuple of start date and end date
    :rtype: tuple
    :raises: ValueError for non overlapping dates
    """
    # convert dates to sets for set intersection
    date1_set = set(dates1)
    date2_set = set(dates2)
    if date1_set.intersection(date2_set):
        # start date
        if dates2[0] > dates1[0]:
            start_date = dates2[0]
        else:
            start_date = dates1[0]

        # end date
        if dates2[-1] > dates1[-1]:
            end_date = dates1[-1]
        else:
            end_date = dates2[-1]

        return start_date, end_date
    else:
       raise ValueError("No overlapping dates.")


def add_ending(file, suffix, ext, delimiter="-"):
    """Add a new ending to a filename,

    :param file: File or path to file
    :type file: string
    :param suffix: Suffix to add to end of file
    :type suffix: string
    :param ext: File extension
    :type ext: string
    :param delimiter: Delimiter, default is the dash character
    :type delimiter: string
    :returns: New file
    :rtype: string

    .. note::
       Spaces in filenames are replaced by delimiter to keep with Unix file naming conventions.

    >>> import utils
    >>> utils.add_ending(file="dv.txt", suffix="summary", ext=".txt")
    'dv-summary.txt'
    >>> utils.add_ending(file="dv.rdb", suffix="summary", ext=".rst", delimiter="_")
    'dv_summary.rst'
    >>> utils.add_ending(file="/home/play/dv.rdb", suffix="summary", ext=".rst")
    '/home/play/dv-summary.rst'
    >>> utils.add_ending(file="daily values.rdb", suffix="summary", ext=".rst")
    'daily-values-summary.rst'
    """
    assert isinstance(file, str), "File must be a string."
    assert isinstance(suffix, str), "Suffix must be a string."
    assert isinstance(ext, str), "Extension must be a string."
    assert isinstance(delimiter, str), "Delimiter must be a string."

    path, fullname = os.path.split(file)
    name, ext_orig = os.path.splitext(fullname)
    parts = name.split()
    if suffix:
        parts.append(suffix)
    if ext:
        newname = delimiter.join(parts) + ext
    else:
        newname = delimiter.join(parts) + ext_orig

    return os.path.join(path, newname)
