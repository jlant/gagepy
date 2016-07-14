# -*- coding: utf-8 -*-
"""
    gagepy.plotting
    ~~~~~~~~~~~~~~~

    Module that contains functions for plotting.

    :authors: 2016 by Jeremiah Lant, see AUTHORS
    :license: United States Geological Survey (USGS), see LICENSE file
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mpld3
from textwrap import wrap
from .globals import COLORS
from . import utils


class MousePositionDatePlugin(mpld3.plugins.PluginBase):
    """Plugin for displaying mouse position with a datetime x axis."""

    JAVASCRIPT = """
    mpld3.register_plugin("mousepositiondate", MousePositionDatePlugin);
    MousePositionDatePlugin.prototype = Object.create(mpld3.Plugin.prototype);
    MousePositionDatePlugin.prototype.constructor = MousePositionDatePlugin;
    MousePositionDatePlugin.prototype.requiredProps = [];
    MousePositionDatePlugin.prototype.defaultProps = {
    fontsize: 12,
    xfmt: "%Y-%m-%d %H:%M:%S",
    yfmt: ".2f"
    };
    function MousePositionDatePlugin(fig, props) {
    mpld3.Plugin.call(this, fig, props);
    }
    MousePositionDatePlugin.prototype.draw = function() {
    var fig = this.fig;
    var xfmt = d3.time.format(this.props.xfmt);
    var yfmt = d3.format(this.props.yfmt);
    var coords = fig.canvas.append("text").attr("class", "mpld3-coordinates").style("text-anchor", "end").style("font-size", this.props.fontsize).attr("x", this.fig.width - 5).attr("y", this.fig.height - 5);
    for (var i = 0; i < this.fig.axes.length; i++) {
      var update_coords = function() {
        var ax = fig.axes[i];
        return function() {
          var pos = d3.mouse(this);
          x = ax.xdom.invert(pos[0]);
          y = ax.ydom.invert(pos[1]);
          coords.text("(" + xfmt(x) + ", " + yfmt(y) + ")");
        };
      }();
      fig.axes[i].baseaxes.on("mousemove", update_coords).on("mouseout", function() {
        coords.text("");
      });
    }
    };
    """
    def __init__(self, fontsize=14, xfmt="%Y-%m-%d %H:%M:%S", yfmt=".2f"):
        self.dict_ = {"type": "mousepositiondate",
                      "fontsize": fontsize,
                      "xfmt": xfmt,
                      "yfmt": yfmt}


def plot_parameter_html(dates, values, name, units):
    """Return an html string of the figure"""

    # instantiate figure
    fig, ax = plt.subplots(subplot_kw=dict(axisbg="#EEEEEE"))
    fig.set_size_inches(12, 10)

    # colors
    if COLORS.get(name):
        colorstr = COLORS.get(name)
    else:
        colorstr = "k"

    # labels
    ax.grid(color="white", linestyle="solid")
    ax.set_title("{0} ({1})".format(name, units), fontsize=20)

    # plot
    line = ax.plot(dates, values, color=colorstr, linewidth=2)

    # connect plugin
    mpld3.plugins.connect(fig, MousePositionDatePlugin())

    return mpld3.fig_to_html(fig)


def plot_parameter(dates, values, mean, max, min, name, units, path=""):
    """Show and optionally save plot."""

    # instantiate figure
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 10)

    # labels
    ax.grid()
    ax.set_title("{0} ({1})".format(name, units))
    ax.set_xlabel("Date")
    ax.set_ylabel("{0}\n({1})".format(name, wrap(units, 60)[0]))

    # colors
    if COLORS.get(name):
        colorstr = COLORS.get(name)
    else:
        colorstr = "k"

    # plot
    line = ax.plot(dates, values, linewidth=2, color=colorstr)

    # rotate and align the tick labels so they look better
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")

    # show text of mean, max, min values
    text = "mean = {0:>#0.2f}\nmax = {1:>#0.2f}\nmin = {2:>#0.2f}".format(mean, max, min)
    patch_properties = {"boxstyle": "round", "facecolor": "wheat", "alpha": 0.5}
    ax.text(0.05, 0.95, text, transform = ax.transAxes, fontsize = 14,
            verticalalignment = "top", horizontalalignment = "left", bbox = patch_properties)

    # save or show
    if path:
        filename = utils.add_ending(file=path, suffix=name, ext=".png")
        plt.savefig(filename)
    else:
        plt.show()
