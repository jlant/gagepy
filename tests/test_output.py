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
from gagepy import output

def test_save_usgs_gage_summary_rst(dates_daily):

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

    output.save_summary(data = usgs_gage.get_summary_data(),
                        template_filename = usgs_gage.template_rst,
                        output_file = "tests/usgsgage-summary.rst")


def test_save_usgs_gage_summary_html(dates_daily):
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

    output.save_summary(data = usgs_gage.get_summary_data(),
                        template_filename = usgs_gage.template_html,
                        output_file = "tests/usgsgage-summary.html")


def test_save_parameter_summary_rst(dates_daily):

    parameter = Parameter(name = "Discharge",
                          dates = dates_daily,
                          units = "cubic feet per second (Mean)",
                          code = "06_00060_00003",
                          values = np.array([1, 2, 3, 4, 5]))

    output.save_summary(data = parameter.get_summary_data(),
                        template_filename = parameter.template_rst,
                        output_file = "tests/parameter-summary.rst")


def test_parameter_save_summary_html(dates_daily):

    parameter = Parameter(name = "Discharge",
                          dates = dates_daily,
                          units = "cubic feet per second (Mean)",
                          code = "06_00060_00003",
                          values = np.array([1, 2, 3, 4, 5]))

    output.save_summary(data = parameter.get_summary_data(),
                        template_filename = parameter.template_html,
                        output_file = "tests/parameter-summary.html")
