from matplotlib.dates import date2num
from dateutil.parser import parse

def parse_timestamp(timestamp):
    """
    Parse a timestamp and return a matplotlib compatible float value
    """
    return date2num(parse(timestamp))

class XCoordHelper(object):
    """
    A class for bookkeeping the x values of linear and nonlinear graphs.
    """
    def __init__(self, linear=False, min_xvalue=0, increment=.4):
        """
        min_xvalue and increment are discarded if linear=True
        """
        if linear:
            self.get_coord = self._get_coord_linear
        else:
            self.get_coord = self._get_coord_nonlinear
        self._odd = False
        self._max_xvalue = 0
        self._last_x_label = None
        self._min_xvalue = min_xvalue
        self._increment = increment
        self.labels = []
        self.ticks = []

    def __call__(self, *args):
        """
        Callable for convenience. Calls self.get_coord (which again calls
        _get_coord_{non,}linear).
        """
        return self.get_coord(*args)

    @property
    def min_xvalue(self):
        return self._min_xvalue

    @property
    def max_xvalue(self):
        return self._max_xvalue - self._increment

    @property
    def x_range(self):
        return self.max_xvalue - self.min_xvalue

    def _get_coord_linear(self, value):
        if isinstance(value, basestring):
            value = parse_timestamp(value)
        if self._max_xvalue == 0:
            self._min_xvalue = value
        self._max_xvalue = value
        return value

    def _get_coord_nonlinear(self, value=None):
        new_val = self._min_xvalue + self._max_xvalue

        if self._odd:
            self._max_xvalue += self._increment
        elif self._last_x_label != value:
            self._last_x_label = value
            self.labels.append(value)
            self.ticks.append(new_val)

        self._odd = not self._odd

        return new_val
