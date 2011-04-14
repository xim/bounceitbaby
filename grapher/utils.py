from matplotlib.dates import date2num
from dateutil.parser import parse

def parse_timestamp(timestamp):
    return date2num(parse(timestamp))

class XCoordHelper(object):
    def __init__(self, linear=False, min_xvalue=0, increment=.7):
        if linear:
            self._get_coord = self._get_coord_linear
        else:
            self._get_coord = self._get_coord_nonlinear
        self._odd = False
        self._x_counter = 0
        self._last_x_label = None
        self._min_xvalue = min_xvalue
        self._increment = increment
        self.labels = []
        self.ticks = []

    def __call__(self, *args):
        return self._get_coord(*args)

    def _get_coord_linear(self, value):
        if isinstance(value, basestring):
            value = parse_timestamp(value)
        return value

    def _get_coord_nonlinear(self, value=None):
        new_val = self._min_xvalue + self._x_counter

        if self._odd:
            self._x_counter += self._increment
        elif self._last_x_label != value:
            self._last_x_label = value
            self.labels.append(value)
            self.ticks.append(new_val)

        self._odd = not self._odd

        return new_val
