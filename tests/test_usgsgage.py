# -*- coding: utf-8 -*-

"""
    test_usgsgage
    ~~~~~~~~~~~~~~~

    Tests for `gagepy.usgsgage` class

    :copyright: 2015 by Jeremiah Lant, see AUTHORS
    :license: United States Geological Survey (USGS), see LICENSE file
"""

import pytest
import os
import numpy as np
from gagepy.usgsgage import USGSGage
from gagepy.parameter import Parameter


def test_usgs_gage_name():

    usgs_gage = USGSGage(name = "USGS 03290500 KENTUCKY RIVER AT LOCK 2 AT LOCKPORT, KY",
                         parameters = None)

    assert usgs_gage.name == "USGS 03290500 KENTUCKY RIVER AT LOCK 2 AT LOCKPORT, KY"


def test_usgs_gage_init_single_parameter(dates_daily):

    usgs_gage = USGSGage(name = "USGS 03290500 KENTUCKY RIVER AT LOCK 2 AT LOCKPORT, KY",
                         parameters = [
                            Parameter(name = "Discharge",
                                      dates = dates_daily,
                                      values = np.array([100, 110, 105, 107, 112]),
                                      units = "cubic feet per second (Mean)",
                                      code = "06_00060_00003")
                            ])

    assert usgs_gage.name == "USGS 03290500 KENTUCKY RIVER AT LOCK 2 AT LOCKPORT, KY"
    assert len(usgs_gage.parameters) == 1
    assert list(usgs_gage.parameters[0].dates) == list(dates_daily)
    assert usgs_gage.parameters[0].code == "06_00060_00003"
    assert usgs_gage.parameters[0].name == "Discharge"
    assert usgs_gage.parameters[0].units == "cubic feet per second (Mean)"
    assert list(usgs_gage.parameters[0].values) == list(np.array([100, 110, 105, 107, 112]))


def test_usgs_gage_init_multiple_parameters(dates_daily):

    usgs_gage = USGSGage(name = "USGS 03290500 KENTUCKY RIVER AT LOCK 2 AT LOCKPORT, KY",
                         parameters = [
                            Parameter(name = "Discharge",
                                      dates = dates_daily,
                                      values = np.array([100, 110, 105, 107, 112]),
                                      units = "cubic feet per second (Mean)",
                                      code = "06_00060_00003"),
                            Parameter(name = "Stage",
                                      dates = dates_daily,
                                      values = np.array([10, 20, 25, 15, 5]),
                                      units = "feet",
                                      code = "03_00065")
                            ])

    assert usgs_gage.name == "USGS 03290500 KENTUCKY RIVER AT LOCK 2 AT LOCKPORT, KY"
    assert len(usgs_gage.parameters) == 2
    assert usgs_gage.parameters[0].code == "06_00060_00003"
    assert usgs_gage.parameters[1].code == "03_00065"
    assert usgs_gage.parameters[0].name == "Discharge"
    assert usgs_gage.parameters[1].name == "Stage"
    assert usgs_gage.parameters[0].units == "cubic feet per second (Mean)"
    assert usgs_gage.parameters[1].units == "feet"
    assert list(usgs_gage.parameters[0].dates) == list(dates_daily)
    assert list(usgs_gage.parameters[1].dates) == list(dates_daily)
    assert list(usgs_gage.parameters[0].values) == list(np.array([100, 110, 105, 107, 112]))
    assert list(usgs_gage.parameters[1].values) == list(np.array([10, 20, 25, 15, 5]))


def test_print_usgs_gage_by_not_capturing_stdout(dates_daily):

    usgs_gage = USGSGage(name = "USGS 03290500 KENTUCKY RIVER AT LOCK 2 AT LOCKPORT, KY",
                         parameters = [
                            Parameter(name = "Discharge",
                                      dates = dates_daily,
                                      values = np.array([1, 2, 3, 4, 5]),
                                      units = "cubic feet per second (Mean)",
                                      code = "06_00060_00003"),
                            Parameter(name = "Stage",
                                      dates = dates_daily,
                                      values = np.array([2, 4, 6, 8, 10]),
                                      units = "feet",
                                      code = "03_00065")
                            ])

    print(usgs_gage)
