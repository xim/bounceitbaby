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
    canvas = FigureCanvas(win, -1, figure)

    # Basically: If time scale is 20 times longer than number of actors, make
    # it 20 times wider than it is tall.
    canvas.SetSize((int(400 / figure.axes[0].get_data_ratio()), 400))

    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(canvas, 1, wx.LEFT | wx.TOP | wx.GROW)

    win.SetSizer(sizer)
    win.Fit()
    frame.SetSize(wx.Size(800, 500))
    win.SetScrollbars(20, 20, int(400 / figure.axes[0].get_data_ratio()) / 20, 400 / 20)

    frame.Show()
    app.MainLoop()
