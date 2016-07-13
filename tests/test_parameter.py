# -*- coding: utf-8 -*-

"""
    test_parameter
    ~~~~~~~~~~~~~~~

    Tests for `gagepy.parameter` class

    :copyright: 2015 by Jeremiah Lant, see AUTHORS
    :license: United States Geological Survey (USGS), see LICENSE file
"""

import pytest
import os
import numpy as np
from datetime import datetime
from gagepy.parameter import Parameter

def test_parameter_init(dates_daily):

    parameter = Parameter(name = "Discharge",
                          dates = dates_daily,
                          values = np.array([100, 110, 105, 107, 112]),
                          units = "cubic feet per second (Mean)",
                          code = "06_00060_00003")

    assert list(parameter.dates) == list(dates_daily)
    assert parameter.code == "06_00060_00003"
    assert parameter.name == "Discharge"
    assert parameter.units == "cubic feet per second (Mean)"
    assert list(parameter.values) == list(np.array([100, 110, 105, 107, 112]))


def test_parameter_values_mean_max_min_without_nan(dates_daily):

    parameter = Parameter(name = "Discharge",
                          dates = dates_daily,
                          units = "cubic feet per second (Mean)",
                          code = "06_00060_00003",
                          values = np.array([1, 2, 3, 4, 5]))

    assert parameter.mean == 3.0
    assert parameter.max == 5.0
    assert parameter.min == 1.0


def test_parameter_values_mean_max_min_with_nan(dates_daily):

    parameter = Parameter(name = "Discharge",
                          dates = dates_daily,
                          units = "cubic feet per second (Mean)",
                          code = "06_00060_00003",
                          values = np.array([1, 2, 3, np.nan, 12]))

    assert parameter.mean == 4.5  # sum(values)/len(values) -> 18/4 = 4.5
    assert parameter.max == 12.0
    assert parameter.min == 1.0


def test_max_min_date(dates_daily):

    parameter = Parameter(name = "Discharge",
                          dates = dates_daily,
                          units = "cubic feet per second (Mean)",
                          code = "06_00060_00003",
                          values = np.array([1, 2, 3, 4, 5]))

    assert parameter.max_date == datetime(2015, 8, 5, 0, 0)
    assert parameter.min_date == datetime(2015, 8, 1, 0, 0)


def test_max_min_date_with_nan(dates_daily):

    parameter = Parameter(name = "Discharge",
                          dates = dates_daily,
                          units = "cubic feet per second (Mean)",
                          code = "06_00060_00003",
                          values = np.array([1, 2, np.nan, 4, 5]))

    assert parameter.max_date == datetime(2015, 8, 5, 0, 0)
    assert parameter.min_date == datetime(2015, 8, 1, 0, 0)


def test_print_parameter_by_not_capturing_stdout(dates_daily):

    parameter = Parameter(name = "Discharge",
                          dates = dates_daily,
                          units = "cubic feet per second (Mean)",
                          code = "06_00060_00003",
                          values = np.array([1, 2, 3, 4, 5]))

    print(parameter)
