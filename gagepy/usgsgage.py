# -*- coding: utf-8 -*-
"""
    gagepy.usgsgage
    ~~~~~~~~~~~~~~~

    Class that contains data and functionality of a United States Geological
    Survey (USGS) gage.

    :copyright: 2015 by Jeremiah Lant, see AUTHORS
    :license: United States Geological Survey (USGS), see LICENSE file
"""

import os
from jinja2 import Template, PackageLoader, Environment
from .parameter import Parameter
from .output import render_summary

class USGSGage(object):
    """A class that contains data and functionality of a United States Geological
    Survey (USGS) gage.

    :param name: Name of USGS gage
    :type name: string
    :param parameters: List of Parameter objects that contain data and functionality of a timeseries data parameter.
    :type parameters: list

    .. seealso::
       :class:`~gagepy.parameter.Parameter`

    >>> import numpy as np
    >>> from datetime import datetime
    >>> name = "USGS 03290500 KENTUCKY RIVER AT LOCK 2 AT LOCKPORT, KY"
    >>> dates = np.array([
    ...     datetime(2015, 8, 1, 0, 0),
    ...     datetime(2015, 8, 2, 0, 0),
    ...     datetime(2015, 8, 3, 0, 0),
    ...     datetime(2015, 8, 4, 0, 0),
    ...     datetime(2015, 8, 5, 0, 0)])
    >>> parameters = [
    ...    Parameter(name = "Discharge",
    ...              dates = dates,
    ...              values = np.array([100, 110, 105, 107, 112]),
    ...              units = "cubic feet per second (Mean)",
    ...              code = "06_00060_00003"),
    ...    Parameter(name = "Stage",
    ...              dates = dates,
    ...              values = np.array([10, 20, 25, 15, 5]),
    ...              units = "feet",
    ...              code = "03_00065")
    ... ]
    >>> usgs_gage = USGSGage(name, parameters)
    >>> usgs_gage.name
    USGS 03290500 KENTUCKY RIVER AT LOCK 2 AT LOCKPORT, KY
    """

    template_rst = "gage-summary-template.rst"
    template_html = "gage-summary-template.html"

    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

    def get_summary_data(self):
        """Return a dictionary of the data for the summary"""
        return {"gage_name": self.name,
                "num_params": len(self.parameters),
                "parameters": self.parameters,
        }

    def __str__(self):
        """Return a formatted view of the data"""

        return render_summary(self.get_summary_data(), self.template_rst)
