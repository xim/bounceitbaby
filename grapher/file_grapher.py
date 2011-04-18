# encoding: utf-8

from matplot import Graph

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from logging_helper import logger

def save_file(data, linear=False, output_file='out.png'):
    """
    Saves the Figure to a file. This is highly automagic, handled by the
    FigureCanvasAgg backend of matplotlib.
    """
    logger.debug('Building Figure from data')
    figure = Graph(data, linear=linear)

    # This updates the Figure object with a reference to the FigureCanvasAgg
    # object so it knows how to save to file.
    canvas = FigureCanvas(figure)
    logger.info('Saving figure to %s' % output_file)
    figure.savefig(filename=output_file, facecolor='.75')
    logger.info(u'… %s done!' % output_file)
