# encoding: utf-8
"""
FigureCanvasWxAgg widget in a wx.ScrolledWindow
"""

import wx
import logging

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

from matplot import graph

def visualize(data):
    """
    The method that does all magic to to with WX.
    """

    app = wx.App()
    frame = wx.Frame(None, -1, 'WX window')
    win = wx.ScrolledWindow(frame, -1)

    figure = graph(data)
    # The canvas is a «proxy of <Swig Object of type 'wxPanel *' at 0xAddress>»
    canvas = FigureCanvas(frame, -1, figure)

    # If time scale is 20 times longer than number of actors, make it 20 times
    # wider than it is tall.
    canvas.SetSize((int(400 / figure.axes[0].get_data_ratio()), 400))

    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(canvas, 1, wx.LEFT | wx.TOP | wx.GROW)

    # Suspect the sizer trick I'm doing is actually just fucking up stuff for
    # the poor scrollbar project. Will have to ask wxPython devs?
    frame.SetSizer(sizer)
    frame.Fit()
    frame.SetSize(wx.Size(500, 400))
    win.SetScrollbars(20, 20, int(400 / figure.axes[0].get_data_ratio()) / 20, 400 / 20)

    frame.Show()
    app.MainLoop()
