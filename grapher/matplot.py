import logging

from matplotlib.dates import DateFormatter, date2num
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch
from matplotlib.ticker import MaxNLocator, MultipleLocator

from utils import parse_timestamp

class Graph(Figure):

    colors = ('r', 'g', 'b', 'c', 'm', 'k')
    arrows = [('fancy', (.25, .25, 0)), ('simple', (0, .5, 0)),
            ('wedge', (0, 0, .5)), ('-|>', (.5, 0, 0)), ('->', 'k')]

    def __init__(self, data, is_linear=True):
        self._is_linear = is_linear

        super(Graph, self).__init__(dpi=90, figsize=(25, 1))
        self._axes = self.add_axes((.05, .085, .92, .865))

        self._arrows = list(self.arrows)
        self._actors = {}
        self._msg_types = {}
        self._max_actor_id = -1
        self._min_xvalue = 999999
        self._max_xvalue = 0

        self.init_axes_parameters()
        self._iterate_data(data)
        self._set_axes_options()

    def init_axes_parameters(self):
        if self._is_linear:
            self._axes.xaxis.set_minor_locator(MaxNLocator(nbins=25))
        else:
            self._axes.xaxis.set_major_locator(MultipleLocator())
        time_format = DateFormatter('%H:%M:%S')
        self._axes.xaxis.set_major_formatter(time_format)
        self._axes.set_xlabel('Time')

    def _iterate_data(self, data):
        for item in data:
            # TODO: Is this ugly? Maybe not ugly enough to do something about it?
            for actor in (item.recipient, item.sender):
                if not actor in self._actors:
                    self._max_actor_id += 1
                    self._actors[actor] = self._max_actor_id

            x0, y0 = item.sent_time, self._actors[item.sender]
            x1, y1 = (item.rcvd_time or x0), self._actors[item.recipient]

            if isinstance(x0, basestring):
                x0 = date2num(parse_timestamp(x0))
            if isinstance(x1, basestring):
                x1 = date2num(parse_timestamp(x1))

            if x0 < self._min_xvalue:
                self._min_xvalue = x0
            if x1 > self._max_xvalue:
                self._max_xvalue = x1

            if not item.msg_type in self._msg_types:
                self._msg_types[item.msg_type] = self._arrows.pop()

            arrow, color = self._msg_types[item.msg_type]
            logging.debug('Adding arrow from (%s, %s) to (%s, %s)' % (
                    x0, y0, x1, y1))
            try:
                self._axes.add_patch(FancyArrowPatch(
                        (x0, y0), (x1, y1), linewidth=1.3, color=color,
                        arrowstyle=arrow, mutation_scale=20))
            except ValueError:
                # Occurs when I try to place two identical arrows on top of each
                # other. TODO: Handle it?
                # (... some time debugging and searching around on the 'net:)
                # OMG, it's a bug in matplotlib fixed in r8720/r8721 ?
                logging.error('Discarding arrow from %s to %s at %s because of a \
    bug in matplotlib.' % (item.sender, item.recipient, item.sent_time))
                pass

    def _set_axes_options(self):
        """
        Note: call only after data has been iterated.
        """
        y_margin = .1 * self._max_actor_id
        self._axes.set_ybound(lower=-y_margin, upper=self._max_actor_id + y_margin)
        x_margin = (self._max_xvalue - self._min_xvalue) * .01
        self._axes.set_xbound(lower=self._min_xvalue - x_margin, upper=self._max_xvalue + x_margin)

        self._axes.yaxis.set_visible(False)

        for actor in self._actors:
            a_id = self._actors[actor]
            color = self.colors[a_id % len(self._actors)]
            self._axes.axhline(y=a_id, linewidth=2, color=color, label=actor)

        # Semi-unreadable code making half-guesses for margin size
        xmargin = min(.1, .1 * self._axes.get_data_ratio())
        self._axes.set_position((xmargin, .085, 1.0 - xmargin * 1.8, .865))

        # Make the legends, place them automatically...
        legend1 = self._axes.legend(loc='upper left')
        arrows = []
        if len(self._msg_types) > 1:
            for _, (arrow, color) in self._msg_types.iteritems():
                arrows.append(FancyArrowPatch(
                        (-1, -1), (-1, -1), linewidth=1.3, color=color,
                        arrowstyle=arrow, mutation_scale=20))
            self._axes.legend(arrows, self._msg_types, loc='lower left')
            self._axes.add_artist(legend1)

        self._axes.grid()
