# -*- coding: utf-8 -*-
"""
    gagepy.output
    ~~~~~~~~~~~~~

    Module of classes that contains data and functionality to create various
    output views of data from a United States Geological Survey (USGS) gage.
    The outputs consist of data summaries in restructured text format and html
    format.  In addition, plots of the data can be output in json objects to be
    embedded in webpages.

    :copyright: 2015 by Jeremiah Lant, see AUTHORS
    :license: United States Geological Survey (USGS), see LICENSE file
"""

import json
from jinja2 import Template, PackageLoader, Environment


def render_summary(data, template_filename):
    """Render a summary of the data.

    :param data: Data to fill template with
    :param type: dictionary
    :param template_filename: The filename of the template to fill
    :type template_filename: string
    """
    loader = PackageLoader("gagepy", "templates")
    env = Environment(loader=loader)
    template = env.get_template(template_filename)

    return template.render(data)


def save_summary(data, template_filename, output_file):
    """Save summary as a restructured text file.

    :param data: Data to fill template with
    :param type: dictionary
    :param template_filename: The filename of the template to fill
    :type template_filename: string
    :param output_file: The full path with filename of the output file to write
    :type output_file: string
    """
    if isinstance(output_file, str):
        with open(output_file, "w") as f:
            f.write(render_summary(data, template_filename))
