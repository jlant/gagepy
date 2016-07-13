# -*- coding: utf-8 -*-

"""
    test_rdb
    ~~~~~~~~

    Tests for `gagepy.rdb` module

    .. note::
       StringIO representations of test data files are fixtures in conftest.py

    :copyright: 2015 by Jeremiah Lant, see AUTHORS
    :license: United States Geological Survey (USGS), see LICENSE file
"""

import pytest
import os
import numpy as np
import re
from io import StringIO
from datetime import datetime

from gagepy import rdb
from gagepy.usgsgage import USGSGage
from gagepy.usgsgage import Parameter

def test_parse_gage_name():

    expected = "USGS 03290500 KENTUCKY RIVER AT LOCK 2 AT LOCKPORT, KY"
    line = "#    USGS 03290500 KENTUCKY RIVER AT LOCK 2 AT LOCKPORT, KY"
    match = re.search(rdb.gage_name_re, line)
    actual = match.group(2)

    assert actual == expected


def test_match_parameter_code_with_statistic_code():

    expected = ("#", "06", "00060", "\t00003", "\tDischarge, cubic feet per second (Mean)")
    line = "#\t06\t00060\t00003\tDischarge, cubic feet per second (Mean)"
    match = re.search(rdb.parameter_code_re, line)
    actual = match.groups(0)

    assert actual == expected


def test_match_parameter_code_without_statistic_code():

    expected = ("#", "03", "00065", 0, "\tGage height, feet")
    line = "#\t03\t00065\tGage height, feet"
    match = re.search(rdb.parameter_code_re, line)
    actual = match.groups(0)

    assert actual == expected


def test_parse_parameter_code():

    expected = ("06_00060_00003", "Discharge, cubic feet per second (Mean)")
    line = "#\t06\t00060\t00003\tDischarge, cubic feet per second (Mean)"
    match = re.search(rdb.parameter_code_re, line)
    actual = rdb.parse_parameter_code(match)

    assert actual == expected


def test_parse_daily_column_names():

    expected = [
        "agency_cd",
        "site_no",
        "datetime",
        "06_00060_00003",
        "06_00060_00003_cd"
    ]
    line = "agency_cd\tsite_no\tdatetime\t06_00060_00003\t06_00060_00003_cd"
    match = re.search(rdb.column_names_re, line)
    actual = match.group(0).split("\t")

    assert actual == expected


def test_parse_instantaneous_column_names():

    expected = [
        "agency_cd",
        "site_no",
        "datetime",
        "tz_cd",
        "03_00065",
        "03_00065_cd"
    ]
    line = "agency_cd\tsite_no\tdatetime\ttz_cd\t03_00065\t03_00065_cd"
    match = re.search(rdb.column_names_re, line)
    actual = match.group(0).split("\t")

    assert actual == expected


def test_match_data_row():

    expected = ("USGS", "03290500", "2012-07-01", 0, "171\tA")
    line = "USGS\t03290500\t2012-07-01\t171\tA"
    match = re.search(rdb.data_row_re, line)
    actual = match.groups(0)

    assert actual == expected


def test_parse_daily_date():

    expected = datetime(2015, 8, 1, 0, 0)
    actual = rdb.parse_daily_date("2015-08-01")

    assert actual == expected


def test_parse_instantaneous_date():

    expected = datetime(2015, 8, 1, 0, 15)
    actual = rdb.parse_instantaneous_date(date = "2015-08-01", time = "00:15\tEDT")

    assert actual == expected


def test_parse_description():

    assert rdb.parse_description("Temperature, water, degrees Celsius") == ("Temperature", "degrees Celsius")
    assert rdb.parse_description("Dissolved oxygen, water, unfiltered, milligrams per liter") == ("Dissolved oxygen", "milligrams per liter")


def test_usgs_gage_for_daily_single_parameter(dates_daily, daily_value_file_single_parameter):

    filestream = StringIO(daily_value_file_single_parameter)
    usgs_gage = rdb.read_rdb_in(filestream)

    assert usgs_gage.name == "USGS 03290500 KENTUCKY RIVER AT LOCK 2 AT LOCKPORT, KY"
    assert len(usgs_gage.parameters) == 1
    assert list(usgs_gage.parameters[0].dates) == list(dates_daily)
    assert usgs_gage.parameters[0].code == "06_00060_00003"
    assert usgs_gage.parameters[0].name == "Discharge"
    assert usgs_gage.parameters[0].units == "cubic feet per second (Mean)"
    assert list(usgs_gage.parameters[0].values) == list(np.array([100, 110, 105, 107, 112]))


def test_usgs_gage_for_instantaneous_single_parameter(dates_instantaneous, instantaneous_value_file_single_parameter):

    filestream = StringIO(instantaneous_value_file_single_parameter)
    usgs_gage = rdb.read_rdb_in(filestream)

    assert usgs_gage.name == "USGS 11143000 BIG SUR R NR BIG SUR CA"
    assert len(usgs_gage.parameters) == 1
    assert list(usgs_gage.parameters[0].dates) == list(dates_instantaneous)
    assert usgs_gage.parameters[0].code == "03_00065"
    assert usgs_gage.parameters[0].name == "Gage height"
    assert usgs_gage.parameters[0].units == "feet"
    assert list(usgs_gage.parameters[0].values) == list(np.array([5, 10, 15, 4.5, 5.5]))


def test_usgs_gage_for_instantaneous_multi_parameter(dates_instantaneous, instantaneous_value_file_multi_parameter):

    filestream = StringIO(instantaneous_value_file_multi_parameter)
    usgs_gage = rdb.read_rdb_in(filestream)

    assert usgs_gage.name == "USGS 03401385 DAVIS BRANCH AT HIGHWAY 988 NEAR MIDDLESBORO, KY"
    assert len(usgs_gage.parameters) == 3

    assert usgs_gage.parameters[0].code == "02_00065"
    assert usgs_gage.parameters[1].code == "03_00010"
    assert usgs_gage.parameters[2].code == "04_00300"

    assert usgs_gage.parameters[0].name == "Gage height"
    assert usgs_gage.parameters[1].name == "Temperature"
    assert usgs_gage.parameters[2].name == "Dissolved oxygen"

    assert usgs_gage.parameters[0].units == "feet"
    assert usgs_gage.parameters[1].units == "degrees Celsius"
    assert usgs_gage.parameters[2].units == "milligrams per liter"

    assert list(usgs_gage.parameters[0].dates) == list(dates_instantaneous)
    assert list(usgs_gage.parameters[1].dates) == list(dates_instantaneous)
    assert list(usgs_gage.parameters[2].dates) == list(dates_instantaneous)

    assert list(usgs_gage.parameters[0].values) == list(np.array([1, 2, 3, 4, 5]))
    assert list(usgs_gage.parameters[1].values) == list(np.array([5, 10, 15, 20, 25]))
    assert list(usgs_gage.parameters[2].values) == list(np.array([2.0, 1.25, 1.20, 0.5, 0.75]))


def test_usgs_gage_for_daily_single_parameter_bad_data_row_formatting(dates_daily, daily_value_file_single_parameter_bad_formatting):

    filestream = StringIO(daily_value_file_single_parameter_bad_formatting)
    usgs_gage = rdb.read_rdb_in(filestream)

    assert usgs_gage.name == "USGS 03290500 KENTUCKY RIVER AT LOCK 2 AT LOCKPORT, KY"
    assert len(usgs_gage.parameters) == 1
    assert usgs_gage.parameters[0].code == "06_00060_00003"
    assert usgs_gage.parameters[0].name == "Discharge"
    assert usgs_gage.parameters[0].units == "cubic feet per second (Mean)"
    assert list(usgs_gage.parameters[0].dates) == list(dates_daily)
    assert list(usgs_gage.parameters[0].values) == list(np.array([10, 20, 30, 40, 50]))


def test_usgs_gage_for_instantaneous_single_parameter_missing_data(dates_instantaneous, instantaneous_value_file_single_parameter_missing_data):

    filestream = StringIO(instantaneous_value_file_single_parameter_missing_data)
    usgs_gage = rdb.read_rdb_in(filestream)

    assert usgs_gage.name == "USGS 11143000 BIG SUR R NR BIG SUR CA"
    assert len(usgs_gage.parameters) == 1
    assert usgs_gage.parameters[0].code == "03_00065"
    assert usgs_gage.parameters[0].name == "Gage height"
    assert usgs_gage.parameters[0].units == "feet"
    assert list(usgs_gage.parameters[0].dates) == list(dates_instantaneous)

    np.testing.assert_almost_equal(usgs_gage.parameters[0].values, np.array([5, 10, np.nan, np.nan, 5.5]))


def test_usgs_gage_for_instantaneous_single_parameter_bad_characters_data_raises_value_error(dates_instantaneous, instantaneous_value_file_single_parameter_bad_characters):

    filestream = StringIO(instantaneous_value_file_single_parameter_bad_characters)

    with pytest.raises(ValueError) as verror:
        usgs_gage = rdb.read_rdb_in(filestream)

    assert str(verror.value) == "Can not convert Ice value to a float"


def test_read_rdb_raises_invalidrdb():

    gagepy_dirpath = os.path.abspath(__file__ + "/../../")
    bad_filepath = os.path.join(gagepy_dirpath, "README.rst")

    with pytest.raises(Exception) as error:
        usgs_gage = rdb.read_rdb(bad_filepath)

    assert str(error.value) == "{0} is not a valid RDB file.".format(bad_filepath)
