import logging
import sys

GRAPH_TYPES = ['Auto', 'WX', 'PNG', 'GTK']

class Grapher(object):
    """
    Basic class for all common functions in Graphs.

    Which currently is nothing.
    """
    def __init__(self):
        """
        __init__ of Grapher classes should throw ImportError if a needed
        library is missing.
        """

class ExportFileGrapher(Grapher):
    """
    All graphers that export to a file inherit from here.
    """

class PNG(ExportFileGrapher):
    """
    Save to a PNG file
    """
    def process_data(self, *args, **kwargs):
        logging.critical('PNG NOT IMPLEMENTED')
        sys.exit(1)

class UIGrapher(Grapher):
    """
    UI grapher classes inherit from this.
    """
    def process_data(self, data):
        self._grapher(data)

class WX(UIGrapher):
    def __init__(self):
        import wx_grapher
        self._grapher = wx_grapher.visualize

class GTK(UIGrapher):
    def __init__(self):
        import gtk_grapher
        self._grapher = gtk_grapher.visualize

class Auto(Grapher):
    def __init__(self):
        self.outputs = [WX, GTK, PNG]
        self._output = None

    def try_inits(self):
        for output in self.outputs:
            try:
                self._output = output()
                return
            except ImportError:
                logging.debug('%s not available for output' % \
                        type(output).__name__)
        raise ImportError('Could not find any valid output modules')

    def process_data(self, data):
        if self._output is None:
            self.try_inits()
        self._output.process_data(data)
