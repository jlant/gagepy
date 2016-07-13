# -*- coding: utf-8 -*-

"""
    test_utils
    ~~~~~~~~~~

    Tests for helper functions.

    :copyright: 2015 by Jeremiah Lant, see AUTHORS
    :license: United States Geological Survey (USGS), see LICENSE file
"""

import pytest
import numpy as np
from gagepy import utils
from datetime import datetime
import os

def test_is_float():

    assert utils.is_float(6.25) == True
    assert utils.is_float("6.25") == True
    assert utils.is_float("2.5_") == False
    assert utils.is_float("hello") == False


def test_to_float():

    assert utils.to_float("6.25") == 6.25
    assert utils.to_float("*2.5_") == 2.5


def test_rmchars():

    assert utils.rmchars("6.5_") == "6.5"
    assert utils.rmchars("*$^**(@4.25_+;") == "4.25"
    assert utils.rmchars("-4.1") == "-4.1"


def test_subset_data_dates_within_range(dates_and_values):

    start = datetime(2015, 1, 4)
    end = datetime(2015, 1, 10)

    expected_dates = np.array([datetime(2015, 1, 4, 0, 0),
                               datetime(2015, 1, 5, 0, 0),
                               datetime(2015, 1, 6, 0, 0),
                               datetime(2015, 1, 7, 0, 0),
                               datetime(2015, 1, 8, 0, 0),
                               datetime(2015, 1, 9, 0, 0),
                               datetime(2015, 1, 10, 0, 0)])

    expected_values = np.array([3, 4, 5, 6, 7, 8, 9])

    actual_dates, actual_values = utils.subset_data(dates = dates_and_values[0],
                                                    values = dates_and_values[1],
                                                    start_date = start,
                                                    end_date = end)

    assert list(actual_dates) == list(expected_dates)
    assert list(actual_values) == list(expected_values)


def test_subset_data_dates_outside_range(dates_and_values):

    start = datetime(2014, 12, 1)
    end = datetime(2015, 1, 20)

    expected_dates = np.array([datetime(2015, 1, 1, 0, 0),
                               datetime(2015, 1, 2, 0, 0),
                               datetime(2015, 1, 3, 0, 0),
                               datetime(2015, 1, 4, 0, 0),
                               datetime(2015, 1, 5, 0, 0),
                               datetime(2015, 1, 6, 0, 0),
                               datetime(2015, 1, 7, 0, 0),
                               datetime(2015, 1, 8, 0, 0),
                               datetime(2015, 1, 9, 0, 0),
                               datetime(2015, 1, 10, 0, 0),
                               datetime(2015, 1, 11, 0, 0)])

    expected_values = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    actual_dates, actual_values = utils.subset_data(dates = dates_and_values[0],
                                                    values = dates_and_values[1],
                                                    start_date = start,
                                                    end_date = end)

    assert list(actual_dates) == list(expected_dates)
    assert list(actual_values) == list(expected_values)

def test_find_start_end_dates_shorter_range(dates_and_values, dates_shorter):

    expected_start_date = datetime(2015, 1, 3, 0, 0)
    expected_end_date = datetime(2015, 1, 11, 0, 0)

    actual_start_date, actual_end_date = utils.find_start_end_dates(dates_and_values[0], dates_shorter)

    assert actual_start_date == expected_start_date
    assert actual_end_date == expected_end_date


def test_find_start_end_dates_longer_range(dates_and_values, dates_longer):

    expected_start_date = datetime(2015, 1, 1, 0, 0)
    expected_end_date = datetime(2015, 1, 11, 0, 0)

    actual_start_date, actual_end_date = utils.find_start_end_dates(dates_and_values[0], dates_longer)

    assert actual_start_date == expected_start_date
    assert actual_end_date == expected_end_date


def test_add_ending():

    assert utils.add_ending(file="dv.txt", suffix="summary", ext=".txt") == "dv-summary.txt"
    assert utils.add_ending(file="dv.txt", suffix="", ext=".rst") == "dv.rst"
    assert utils.add_ending(file="dv.txt", suffix="", ext="") == "dv.txt"
    assert utils.add_ending(file="dv.txt", suffix="summary", ext="") == "dv-summary.txt"
    assert utils.add_ending(file="dv.rdb", suffix="summary", ext=".rst", delimiter="_") == "dv_summary.rst"
    assert utils.add_ending(file=os.path.join(os.path.sep, "home", "play", "dv.rdb"), suffix="summary", ext=".rst") == os.path.join(os.path.sep, "home", "play", "dv-summary.rst")
    assert utils.add_ending(file="daily values.rdb", suffix="summary", ext=".rst") == "daily-values-summary.rst"
    assert utils.add_ending(file="usgs daily values.rdb", suffix="summary", ext=".rst", delimiter="_") == "usgs_daily_values_summary.rst"

    with pytest.raises(AssertionError) as error:
        utils.add_ending(file=True, suffix="summary", ext=".txt")

    with pytest.raises(AssertionError) as error:
        utils.add_ending(file="dv.txt", suffix=2, ext=".txt")

    assert str(error.value) == "Suffix must be a string."

    with pytest.raises(AssertionError) as error:
        utils.add_ending(file="dv.txt", suffix="summary", ext=4.5)

    assert str(error.value) == "Extension must be a string."

    with pytest.raises(AssertionError) as error:
        utils.add_ending(file="dv.txt", suffix="summary", ext=".txt", delimiter=5)

    assert str(error.value) == "Delimiter must be a string."
