# encoding: utf-8

import StringIO

from matplot import Graph

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import logging

logger = logging.getLogger('bounceitbaby')

def _build_figure(*args, **kwargs):
    logger.debug('Building Figure from data')
    figure = Graph(*args, **kwargs)

    # This updates the Figure object with a reference to the FigureCanvasAgg
    # object so it knows how to save to file.
    canvas = FigureCanvas(figure)
    return figure

def save_file(data, actors, linear=False, output_file='out.png'):
    """
    Saves the Figure to a file. This is highly automagic, handled by the
    FigureCanvasAgg backend of matplotlib.

    All arguments but output_file passed to grapher.matplot.Graph
    """
    figure = _build_figure(data, actors, linear=linear)
    logger.info('Saving figure to %s' % output_file)
    figure.savefig(filename=output_file, facecolor='.75')
    logger.info(u'… %s done!' % output_file)

def file_as_filelike(data, actors, linear=False, format='png'):
    """
    Saves the Figure to data in a file like object. Formats supported is
    decided by the FigureCanvasAgg backend of matplotlib.

    All arguments but format passed to grapher.matplot.Graph
    """
    figure = _build_figure(data, actors, linear=False)
    data = StringIO.StringIO()

    logger.debug('Printing figure to %s format' % format)
    figure.savefig(filename=data, format=format, facecolor='.75')
    logger.debug(u'… %s output done!' % format)
    data.seek(0)

    return data
