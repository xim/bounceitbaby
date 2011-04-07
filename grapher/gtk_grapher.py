"""
FigureCanvasGTKAgg widget in a gtk.ScrolledWindow
"""

import gtk
import logging

from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas

from matplot import graph

def visualize(data):
    """
    The method that does all magic to to with GTK.
    """

    win = gtk.Window()
    win.connect("destroy", lambda x: gtk.main_quit())
    win.set_default_size(800,500)
    win.set_title("GTK window")

    sw = gtk.ScrolledWindow()
    win.add(sw)
    sw.set_policy(hscrollbar_policy=gtk.POLICY_ALWAYS,
                  vscrollbar_policy=gtk.POLICY_AUTOMATIC)

    figure = graph(data)
    canvas = FigureCanvas(figure)
    # If time scale is 20 times longer than number of actors, make it 20 times
    # wider than it is tall.
    canvas.set_size_request(int(400 / figure.axes[0].get_data_ratio()), 400)
    sw.add_with_viewport(canvas)

    win.show_all()
    gtk.main()
