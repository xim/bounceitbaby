import sys

import logging

logger = logging.getLogger('bounceitbaby')

GRAPH_TYPES = ['Auto', 'GTK', 'WX', 'File']

class Grapher(object):
    """
    Basic class for all common functions in Graphs.

    Which currently is nothing.
    """
    def __init__(self, actors, linear=False, output_file='out.png'):
        """
        __init__ of Grapher classes should throw ImportError if a needed
        library is missing. This facilitates the Auto class.
        """
        self._actors = actors
        self._linear_graph = linear
        self._outout_file = output_file

class File(Grapher):
    """
    Save to a graphics file.
    """
    def __init__(self, *args, **kwargs):
        super(File, self).__init__(*args, **kwargs)
        import file_grapher
        self._grapher = file_grapher.save_file

    def process_data(self, data):
        self._grapher(data, self._actors, output_file=self._outout_file,
                linear=self._linear_graph)

class UIGrapher(Grapher):
    """
    UI grapher classes inherit from this.
    """
    def process_data(self, data):
        self._grapher(data, self._actors, self._linear_graph)

class WX(UIGrapher):
    """
    Visualize the graph in a UI window using WX
    """
    def __init__(self, *args, **kwargs):
        super(WX, self).__init__(*args, **kwargs)
        import wx_grapher
        self._grapher = wx_grapher.visualize

class GTK(UIGrapher):
    """
    Visualize the graph in a UI window using GTK
    """
    def __init__(self, *args, **kwargs):
        super(GTK, self).__init__(*args, **kwargs)
        import gtk_grapher
        self._grapher = gtk_grapher.visualize

class Auto(Grapher):
    """
    Visualize the graph in the first suitable output module.
    Priority of output modules is set by self.outputs.
    *args and **kwargs are passed to underlying modules.
    """
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self.outputs = [GTK, WX, File]
        self._output = None

    def try_inits(self):
        """
        Go through each output in self.output and test if we can use it for
        processing data.
        """
        for output in self.outputs:
            logger.debug('Auto grapher trying to load %s for graph' % output)
            try:
                self._output = output(*self._args, **self._kwargs)
                self.process_data = self._output.process_data
                return
            except ImportError:
                logger.debug('%s not available for output' % \
                        output.__name__)
        raise ImportError('Could not find any valid output modules')

    def process_data(self, data):
        "Runs try_inits to find an output module, then runs its process_data."
        if self._output is None:
            self.try_inits()
        self._output.process_data(data)
