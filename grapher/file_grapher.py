# encoding: utf-8

import StringIO

from matplot import Graph

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from logging_helper import logger

def _build_figure(data, linear=False):
    logger.debug('Building Figure from data')
    figure = Graph(data, linear=linear)

    # This updates the Figure object with a reference to the FigureCanvasAgg
    # object so it knows how to save to file.
    canvas = FigureCanvas(figure)
    return figure

def save_file(data, linear=False, output_file='out.png'):
    """
    Saves the Figure to a file. This is highly automagic, handled by the
    FigureCanvasAgg backend of matplotlib.
    """
    figure = _build_figure(data, linear)
    logger.info('Saving figure to %s' % output_file)
    figure.savefig(filename=output_file, facecolor='.75')
    logger.info(u'… %s done!' % output_file)

def file_as_filelike(data, linear=False, format='png'):

    figure = _build_figure(data, linear)
    data = StringIO.StringIO()

    logger.debug('Printing figure to %s format' % format)
    figure.savefig(filename=data, facecolor='.75')
    logger.debug(u'… %s output done!' % format)
    data.seek(0)

    return data
