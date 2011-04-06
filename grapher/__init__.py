import logging

GRAPH_TYPES = ['Auto', 'WX', 'PNG', 'GTK']

class Grapher(object):
    """
    Basic class for all common functions in Graphs.
    """

    def __init__(self):
        self._data = []

    def set_data(self, data):
        """
        Set data to be processed by the module
        """
        self._data[0:] = data

    def process_data(self, data=None):
        if data is not None:
            self.set_data(data)

class PNG(Grapher):
    def process_data(self, *args, **kwargs):
        super(PNG, self).process_data(*args, **kwargs)
        logging.critical('PNG NOT IMPLEMENTED')
        return False

class WX(Grapher):
    def process_data(self, *args, **kwargs):
        super(WX, self).process_data(*args, **kwargs)
        logging.critical('WX NOT IMPLEMENTED')
        return False

class GTK(Grapher):
    def __init__(self):
        super(GTK, self).__init__()
        import gtk_grapher
        self._grapher = gtk_grapher.graph
    def process_data(self, *args, **kwargs):
        super(GTK, self).process_data(*args, **kwargs)
        self._grapher(self._data)

Auto = GTK
try:
    import gtk_grapher
except ImportError:
    logging.warning('GTK not available for visualization')
    Auto = WX
    try:
        import wxversion
    except ImportError:
        logging.warning('wxPython not available for visualization')
        Auto = PNG
