# -*- coding: utf-8 -*-

"""
    gagepy.rdb
    ~~~~~~~~~~

    Module containing functionality that reads and parses tab-delimited (rdb)
    formatted timeseries files from the United States Geological Survey (USGS)
    National Water Information System (NWIS). Please see
    http://pubs.usgs.gov/of/2003/ofr03123/6.4rdb_format.pdf for more information
    regarding the tab-delimited (rdb) format.

    :copyright: 2015 by Jeremiah Lant, see AUTHORS
    :license: United States Geological Survey (USGS), see LICENSE file
"""

import re
import numpy as np
from datetime import datetime

from .usgsgage import USGSGage
from .parameter import Parameter
from . import utils
from .exceptions import InvalidRDB

# precompiled regular expressions
parameter_code_re = "(#)\D+([0-9]{2})\D+([0-9]{5})(\D+[0-9]{5})?(.+)"  # 4 groups - dd, parameter, statistic, description
gage_name_re = "(#.+)(USGS [0-9]+\s.+)"                                # 2 groups - _, gage name
column_names_re = "(agency_cd)\t(site_no)\t(datetime)\t(tz_cd)?(.+)"   # 5 groups - agency code, site number, datetime, time (may or may not), parameter codes
data_row_re = "(USGS)\t([0-9]+)\t([0-9]{4}-[0-9]{1,2}-[0-9]{1,2})\s?([0-9]{2}:[0-9]{2}\t[A-Z]{3})?(.+)"  # 5 groups - USGS, gage number, datetime, timezone (may or may not), parameter values and qualification code


def read_rdb(filepath):
    """Open file and create a file object for read_file_in(filestream) to process.
    Return a USGSGage object containing all relevant data.  This function is
    responsible to opening the file, removing the file opening responsibility
    from read_file_in(filestream) so that read_file_in(filestream) can be unit tested.

    :param filepath: path to file
    :type filepath: string
    :returns: data
    :rtype: dictionary

    .. seealso::
       :class:`~gagepy.usgsgage.USGSGage`
    """
    with open(filepath, "r") as f:
        try:
            usgs_gage = read_rdb_in(f)
        except:
            raise InvalidRDB("{0} is not a valid RDB file.".format(filepath))

    return usgs_gage


def read_rdb_in(filestream):
    """Function that reads the tab-delimited (rdb) USGS timeseries data file,
    and returns a USGSGage object containing all the data and information contained
    in the data file.

    :param filestream:
    :type filestream: _io.TextIOWrapper
    :returns: data
    :rtype: dict
    """
    lines = filestream.readlines()

    # initialize a dictionary to temporarily the data of interest while reading
    data = {
        "parameters": [],
        "dates": []
    }

    # loop through each line searching for regex matches; if match then parse and add to data dictionary
    for line in lines:
        match_gage_name = re.search(pattern = gage_name_re, string = line)
        match_parameters = re.search(pattern = parameter_code_re, string = line)
        match_column_names = re.search(pattern = column_names_re, string = line)
        match_data_row = re.search(pattern = data_row_re, string = line)

        if match_gage_name:
            gage_name = match_gage_name.group(2)

        # get the parameters available and create a dictionary for each parameter
        elif match_parameters:
            code, description = parse_parameter_code(match = match_parameters)

            data["parameters"].append({"code": code,
                                      "description": description,
                                      "index": None,
                                      "data": []})

        # get the column names and indices of parameters
        elif match_column_names:
            column_names = match_column_names.group(0).split("\t")

            for parameter in data["parameters"]:
                parameter["index"] = column_names.index(parameter["code"])

        # build the lists of dates and parameter data
        elif match_data_row:

            # if timezone is in match object, join the daily date and time zone by a tab character to have parsed properly
            if match_data_row.group(4):
                date = parse_instantaneous_date(date = match_data_row.group(3), time = match_data_row.group(4))
            else:
                date = parse_daily_date(date = match_data_row.group(3))

            data["dates"].append(date)

            # loop through list of parameters and extract the data value based on the index found from column names list
            for parameter in data["parameters"]:
                value = match_data_row.group(0).split("\t")[parameter["index"]]

                # if value is empty, replace with a nan value and print an informative message mentioning nan replacement, otherwise convert the value to a float
                if value == "":
                    value = utils.to_nan(value, msg = "Replacing missing value with nan: {} on {} - {}".format(parameter["code"], date.strftime("%Y-%m-%d %H:%M"), parameter["description"]))
                else:
                    value = utils.to_float(value)

                parameter["data"].append(value)

    # create a list of Parameter objects
    parameters = []
    for parameter in data["parameters"]:
        name, units = parse_description(parameter["description"])
        parameters.append(Parameter(name = name,
                                    dates = np.array(data["dates"]),
                                    values = np.array(parameter["data"]),
                                    units = units,
                                    code = parameter["code"]))

    # create a usgs gage object that contains all the relevant data
    usgs_gage = USGSGage(gage_name, parameters)

    return usgs_gage


def parse_daily_date(date):
    """Parse a string of the form yyyy-mm-dd and return a datetime object.

    :param: date
    :type date: string
    :rtype: datetime.datetime

    >>> daily_date = parse_daily_date("2015-08-01")
    >>> daily_date
    datetime.datetime(2015, 8, 1, 0, 0)
    """
    return datetime.strptime(date, "%Y-%m-%d")


def parse_instantaneous_date(date, time):
    """Parse a date string of the form 'yyyy-mm-dd' and a time string of the
    form 'mm:ss\tEDT' and return a datetime object.

    :param: date
    :type date: string
    :param: time
    :type date: string
    :rtype: datetime.datetime

    >>> instantaneous_date = parse_instantaneous_date(date = "2015-08-01", time = "00:15\tEDT")
    >>> instantaneous_date
    datetime.datetime(2015, 8, 1, 0, 15)
    """
    time = time.split("\t")[0]
    date_str = " ".join((date, time))

    return datetime.strptime(date_str, "%Y-%m-%d %H:%M")


def parse_parameter_code(match):
    """Process a regular expression match for a parameter code and a description.
    The parameter code and description string line is made up of 4 parts:

    1. a data descriptor value

    2. a parameter code value

    3. a parameter statistic value (may or may not exist)

    4. a parameter description

    :param match: a regular expression match object
    :type match: _sre.SRE_Match
    :return: parameter code, statistic (if it exists), and description
    :rtype: tuple

    >>> import re
    >>> parameter_code_re = "(#)\D+([0-9]{2})\D+([0-9]{5})(\D+[0-9]{5})?(.+)"
    >>> line = "#\t06\t00060\t00003\tDischarge, cubic feet per second (Mean)"
    >>> match = re.search(rdb.parameter_code_re, line)
    >>> parameter_code = rdb.parse_parameter_code(match)
    >>> parameter_code
    ('06_00060_00003', 'Discharge, cubic feet per second (Mean)')
    """
    # get the data descriptor and the parameter code
    dd = match.group(2)
    param = match.group(3)

    # concatenate dd and param using "_" as in the column names
    code = "_".join((dd, param))

    # get parameter description
    description = match.group(5).strip()

    # if statistic exists, then add that to the string
    if match.group(4):
        statistic =  match.group(4).strip()
        code = "_".join((code, statistic))

    return (code, description)


def parse_description(description):
    """Return the parameter name and unit from the parameter description

    :param description: A description containing a parameter name and unit
    :type description: string
    :returns: Name and units of a parameter
    :rtype: tuple

    >>> description = "Temperature, water, degrees Celsius"
    >>> parse_description(description)
    ('Temperature', 'degrees Celsius')
    """
    name = description.split(",")[0]
    units = description.split(",")[-1].strip()

    return name, units
