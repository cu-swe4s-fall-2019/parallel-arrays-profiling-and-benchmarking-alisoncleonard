import matplotlib
import matplotlib.pyplot as plt
import sys
import os.path
from os import path
matplotlib.use('Agg')

"""Plotting functions using matplotlib

    * boxplot
    * histogram
    * combo
"""


def boxplot(out_file_name, title, x_axis, y_axis, lists, x_ticks):

    """Create a boxplot from a list of data and save the graph to an
    output file. To make a plot with multiple boxes, pass a list of lists.

    Parameters
    ___________

    out_file_name:
        The file name the graph will be saved under. Must use a supported file
        extension, such as .png. Input as a string.

    title: Title of boxplot, displayed at top of plot. A string.

    x_axis: label for x axis. A string.

    y_axis: label for y axis. A string.

    lists: list of ints or floats
        Data to be graphed. May pass a list of lists to plot multiple samples

    x_ticks: The x-axis labels for each individual box. Pass a list of strings,
            corresponding to the index of sample in lists

    Returns
    _________

    Box plot of the input lists saved as out_file_name in the current directory

    """

# check that the out file will not write over existing data
    if path.exists(out_file_name):
        raise Exception('Output file already exists. Choose a new name')
        sys.exit(1)

    try:
        out_file = out_file_name
        figure_title = title
        figure_xaxis = x_axis
        figure_yaxis = y_axis
        data_to_plot = lists
        sample_labels = x_ticks

        width = 3
        height = 3

        fig = plt.figure(figsize=(width, height), dpi=300)
        ax = fig.add_subplot(1, 1, 1)

        ax.boxplot(data_to_plot)
        ax.set_title(figure_title)
        # set custom labels with the names of each list
        ax.set_xticklabels(sample_labels)
        ax.set_xlabel(figure_xaxis)
        ax.set_ylabel(figure_yaxis)

        plt.savefig(out_file, bbox_inches='tight')

    except ValueError:
        raise ValueError('Can not support file extension. Try .png instead')


def histogram(L, out_file_name):

    """Create a histogram from an list of data and save the graph to an
    output file

    Parameters
    ___________

    L: list of ints or floats
        data to be graphed

    out_file_name:
        The file name the graph will be saved under. Must use a supported file
        extension, such as .png

    Returns
    _________

    a histogram saved as out_file_name in the current directory

    """
    # check that the out file will not write over existing data
    if path.exists(out_file_name):
        raise Exception('Output file already exists. Choose a new name')
        sys.exit(1)

    try:
        out_file = out_file_name

        width = 3
        height = 3

        fig = plt.figure(figsize=(width, height), dpi=300)

        ax = fig.add_subplot(1, 1, 1)

        ax.hist(L, 20)
        ax.set_title('title')
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')

        plt.savefig(out_file, bbox_inches='tight')

    except ValueError:
        raise ValueError('Can not support file extension. Try .png instead')


def combo(L, out_file_name):

    """Create a combination plot with a boxplot and histogram  from an list of
    data and save the graph to an output file

    Parameters
    ___________

    L: list of ints or floats
    data to be graphed

    out_file_name:
    The file name the graph will be saved under. Must use a supported file
    extension, such as .png

    Returns
    _________

    a combination boxplot and histogram, saved as out_file_name in the
    current directory

    """

    # check that the out file will not write over existing data
    if path.exists(out_file_name):
        raise Exception('Output file already exists. Choose a new name')
        sys.exit(1)

    try:

        out_file = out_file_name

        width = 5
        height = 3

        fig = plt.figure(figsize=(width, height), dpi=300)

        ax = fig.add_subplot(1, 1, 1)

        ax.boxplot(L)
        ax.hist(L, 20)
        # combo plot uses same title and axis labels for both plots
        ax.set_title('title')
        ax.set_xlabel('Values')
        ax.set_ylabel('Histogram: frequency; Boxplot: distribution of values')

        plt.savefig(out_file, bbox_inches='tight')

    except ValueError:
        raise ValueError('Can not support file extension. Try .png instead')
