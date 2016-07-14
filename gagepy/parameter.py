# -*- coding: utf-8 -*-
"""
    gagepy.parameter
    ~~~~~~~~~~~~~~~~

    Class that contains data and functionality of a timeseries data parameter.

    :authors: 2016 by Jeremiah Lant, see AUTHORS
    :license: United States Geological Survey (USGS), see LICENSE file
"""


import os
import numpy as np
from jinja2 import Template, PackageLoader, Environment
from .plotting import plot_parameter, plot_parameter_html
from .output import render_summary

class Parameter(object):
    """ A class that contains data and functionality of a timeseries parameter.

    :param name: Name of the parameter
    :type name: string
    :param dates: Array of datetime objects
    :type dates: numpy.ndarray
    :param values: Array of data values
    :type values: numpy.ndarray
    :param units: Units of the parameter
    :type param: string
    :param code: A numeric code identifier of the parameter; default of None

    .. warning::
       Length of dates and length of values must be equal to be a valid
       timeseries parameter.
    """

    template_rst = "parameter-summary-template.rst"
    template_html = "parameter-summary-template.html"

    def __init__(self, name, dates, values, units, code=None):

        assert len(dates) == len(values), "Length of dates {0} does not equal length of values {1}".format(len(dates), len(values))

        self.name = name
        self.dates = dates
        self.values = values
        self.units = units
        self.code = code

    @property
    def mean(self):
        """Get the mean ignoring any NaN values"""

        return np.nanmean(self.values)

    @property
    def max(self):
        """Get the maximum ignoring any NaN values"""

        return np.nanmax(self.values)

    @property
    def min(self):
        """Get the minimum ignoring any NaN values"""

        return np.nanmin(self.values)

    @property
    def max_date(self):
        """Get the date that the maximum value occurred on"""

        max_index = np.nanargmax(self.values)
        return self.dates[max_index]

    @property
    def min_date(self):
        """Get the date that the min value occurred on"""

        min_index = np.nanargmin(self.values)
        return self.dates[min_index]

    def get_summary_data(self):
        """Return a dictionary of the data for the summary"""
        return {"name": self.name,
                "units": self.units,
                "mean": self.mean,
                "max": self.max,
                "min": self.min,
                "max_date": self.max_date,
                "min_date": self.min_date,
                "start_date": self.dates[0],
                "end_date": self.dates[-1],
                "num_vals": len(self.values),
                "plot": self.plot_html(),
        }

    def __str__(self):
        """Return a formatted view of the data"""

        return render_summary(self.get_summary_data(), self.template_rst)


    def plot_html(self):
        """Return an html string represenation of the figure"""

        return plot_parameter_html(self.dates, self.values, self.name, self.units)

    def plot(self, path=""):
        """Show and optionally save plot."""

        plot_parameter(self.dates, self.values, self.mean, self.max, self.min, self.name, self.units, path)
