#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    gagepy.cli
    ~~~~~~~~~~

    Main `gagepy` Command Line Interface (CLI)

    :copyright: 2015 by Jeremiah Lant, see AUTHORS
    :license: United States Geological Survey (USGS), see LICENSE file for more details
"""

import click
import os

from . import rdb
from . import utils
from .output import save_summary

class Config(object):

    def __init__(self):
        self.verbose = False
        self.plot = False
        self.html = False
        self.save = None


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option("--verbose", is_flag=True, help="Print summary.")
@click.option("--plot", is_flag=True, help="Show plot.")
@click.option("--html", is_flag=True, help="Save summary as html file.")
@click.option("--save", type=click.Path(), help="Save summary to specified path.")
@click.option("--saveplot", type=click.Path(), help="Save plots to specified path.")
@pass_config
def main(config, verbose, plot, html, save, saveplot):
    config.verbose = verbose
    config.plot = plot
    config.html = html
    config.save = save
    config.saveplot = saveplot


@main.command()
@click.argument("files", nargs=-1, required=True)
@pass_config
def readrdb(config, files):
    """Read rdb file(s)."""

    for file in files:
        click.echo("Processing: {}".format(file))
        usgs_gage = rdb.read_rdb(file)

        if config.html and config.save:
            name = utils.add_ending(file = config.save, suffix = "", ext = "")
            save_summary(data = usgs_gage.get_summary_data(),
                         template_filename = usgs_gage.template_html,
                         output_file = name)
        elif config.html:
            name = utils.add_ending(file = file, suffix = "summary", ext = ".html")
            save_summary(data = usgs_gage.get_summary_data(),
                         template_filename = usgs_gage.template_html,
                         output_file = name)
        elif config.save:
            name = utils.add_ending(file = config.save, suffix = "", ext = "")
            save_summary(data = usgs_gage.get_summary_data(),
                         template_filename = usgs_gage.template_rst,
                         output_file = name)
        else:
            name = utils.add_ending(file = file, suffix = "summary", ext = ".rst")
            save_summary(data = usgs_gage.get_summary_data(),
                         template_filename = usgs_gage.template_rst,
                         output_file = name)

        click.echo("Saving summary: {}".format(name))

        if config.plot:
            for parameter in usgs_gage.parameters:
                parameter.plot()

        if config.saveplot:
            for parameter in usgs_gage.parameters:
                filedir, filename = os.path.split(file)
                path = os.path.join(config.saveplot, filename)
                parameter.plot(path=path)
            click.echo("Saving plots to: {}".format(config.saveplot))

        if config.verbose:
            click.echo("\n{}".format(usgs_gage))

        click.echo("\n")
