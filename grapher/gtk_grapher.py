"""
FigureCanvasGTKAgg widget in a gtk.ScrolledWindow
"""

import gtk
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas

from matplot import Graph

import logging

logger = logging.getLogger('bounceitbaby')

def visualize(*args, **kwargs):
    """
    Method that does all magic to to with GTK.

    All arguments passed to grapher.matplot.Graph
    """

    logger.debug('Spawning a GTK window')
    win = gtk.Window()
    win.connect('destroy', lambda x: gtk.main_quit())
    win.set_default_size(800,500)
    win.set_title('BounceItBaby visualizer')

    sw = gtk.ScrolledWindow()
    win.add(sw)
    # TODO: allow arrow/hjkl buttons to scroll
    sw.set_policy(hscrollbar_policy=gtk.POLICY_ALWAYS,
                  vscrollbar_policy=gtk.POLICY_AUTOMATIC)

    logger.debug('Building the Figure from data')
    figure = Graph(*args, **kwargs)
    canvas = FigureCanvas(figure)
    # If time scale is 20 times longer than number of actors, make it 20 times
    # wider than it is tall.
    canvas.set_size_request(int(400 / figure.axes[0].get_data_ratio()), 400)
    sw.add_with_viewport(canvas)

    logger.debug('Displaying GTK window!')
    win.show_all()
    gtk.main()
