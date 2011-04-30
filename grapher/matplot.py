from itertools import cycle, count

from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch
from matplotlib.text import Text
from matplotlib.ticker import MaxNLocator, MultipleLocator

from utils import XCoordHelper

import logging

logger = logging.getLogger('bounceitbaby')

class Graph(Figure):

    colors = ('r', 'g', 'b', 'c', 'm', 'k')
    # TODO: The arrow 'simple' makes the library die. A bug. Fixed in
    # matplotlib r8720/r8721 I think.
    # For all the possible arrow styles:
    # http://matplotlib.sourceforge.net/plot_directive/mpl_examples/pylab_examples/fancyarrow_demo.hires.png
    arrows = [('wedge', (.25, .25, 0)), ('->', (0, .5, 0)), ('->', (0, 0, .5)),
            ('-|>', (.5, 0, 0)), ('fancy', 'k')]

    def __init__(self, data, actors, linear=False):
        self._actors = dict(zip(actors, count()))
        self._is_linear = linear
        self._coord = XCoordHelper(linear, increment=len(actors)/10.)

        # Note: later we alter figsize according to scale. All numbers here are
        # guesses and not really used later.
        super(Graph, self).__init__(dpi=90, figsize=(16,6))
        self._axes = self.add_axes((.05, .085, .92, .865))

        # ... Wow, we do a lot of manual housekeeping!
        # Make the arrows infinitely reusable.
        self._arrows = cycle(self.arrows)
        # Remember all distinct message types.
        self._msg_types = {}
        # For remembering the message type at each timestamp. TODO: Kind of
        # sucks for linear graphs?
        self._msgtype_ticks = []
        self._msgtype_labels = []

        # Call all functions on the object, in natural order.
        logger.debug('Iterating %s in %s (linear: %s)' % (data, self, linear))
        self._add_actors()
        self._iterate_data(data)
        logger.debug('Setting graph parameters')
        self._set_axes_options()
        self._set_tick_parameters()
        logger.debug('%s seems to have exited successfully' % self)

    def _iterate_data(self, data):
        for item in data:

            # Extract x and y values into names that make more sense graph-wize
            x0, y0 = item.sent_time, self._actors[item.sender]
            x1, y1 = (item.rcvd_time or x0), self._actors[item.recipient]

            # Translate X values to sensible scale, includes some bookkeeping
            x0 = self._coord(x0)
            x1 = self._coord(x1)

            # If the message type hasn't been seen before, assign a style
            if not item.msg_type in self._msg_types:
                self._msg_types[item.msg_type] = self._arrows.next()

            # Make the arrow
            self._make_arrow(item, x0, y0, x1, y1)

    def _make_arrow(self, item, x0, y0, x1, y1):
            arrow, color = self._msg_types[item.msg_type]
            x_mid, y_mid = (x0 + x1) / 2., (y0 + y1) / 2.
            self._axes.add_patch(FancyArrowPatch(
                    (x0, y0), (x1, y1), linewidth=1.3, color=color,
                    arrowstyle=arrow, mutation_scale=20))
            # And add text if there was any
            # TODO: Rotate by degree if this was linear. The arrow should know
            # its own rotation, right?
            offset = self._coord._increment / 4.
            if item.port_name:
                # TODO: Make the distance relative to the hight of the graph?
                self._axes.add_artist(Text(x_mid - offset, y_mid, item.port_name,
                    rotation='vertical', verticalalignment='center',
                    horizontalalignment='center'))
            if item.data:
                self._axes.add_artist(Text(x_mid + offset, y_mid, item.data,
                    rotation='vertical', verticalalignment='center',
                    horizontalalignment='center'))

            # And do some bookkeeping.
            self._msgtype_ticks.append(x0)
            self._msgtype_labels.append(item.msg_type)

    def _add_actors(self):
        # Add the horizontal lines we want for each actor
        for actor in self._actors:
            a_id = self._actors[actor]
            color = self.colors[a_id % len(self.colors)]
            self._axes.axhline(y=a_id, linewidth=2, color=color)

    def _set_axes_options(self):
        """
        Note: call only after data has been iterated.
        """
        # Set axes bounds to include some margins inside the graph
        max_actor_y = len(self._actors) - 1
        y_margin = .1 * max_actor_y
        self._axes.set_ybound(lower=-y_margin, upper=max_actor_y + y_margin)
        x_margin = self._coord._increment / 2.
        self._axes.set_xbound(lower=self._coord.min_xvalue - x_margin,
                upper=self._coord.max_xvalue + x_margin)

        # Semi-unreadable code making half-guesses for margin size outside the
        # graph. At most .1 in x, at least .16 times the data ratio.
        xmargin = min(.1, .16 * self._axes.get_data_ratio())
        self._axes.set_position((xmargin, .085, 1 - xmargin * 1.8, .865))

        # Activate the nice dotted lines on the tick positions of the x axis
        self._axes.xaxis.grid()

        # Set the figure size, this influences the file export.
        # TODO: 7 in * 90 px/in = 630 px. Maybe allow the user to set size?
        self.set_size_inches((int(7 / self._axes.get_data_ratio()), 7))

    def _set_tick_parameters(self):
        if self._is_linear:
            # If this is a linear graph, make sure it has ticks and timestamps.
            self._axes.xaxis.set_minor_locator(MaxNLocator(nbins=25))
            time_format = DateFormatter('%H:%M:%S')
            self._axes.xaxis.set_major_formatter(time_format)
        else:
            # Nonlinear? Then we want to manually determine ticks on x.
            self._axes.xaxis.set_ticks(self._coord.ticks)
            self._axes.xaxis.set_ticklabels(self._coord.labels)

        self._axes.set_xlabel('Time')

        # Add ticks on the top axis with message types printed
        self._axes2 = self._axes.twiny()
        self._axes2.xaxis.set_ticks(self._msgtype_ticks)
        self._axes2.xaxis.set_ticklabels(self._msgtype_labels)
        self._axes2.set_xlim(*self._axes.get_xlim())

        # Add ticks on the left with the actor names
        self._axes.yaxis.set_ticks(self._actors.values())
        self._axes.yaxis.set_ticklabels(self._actors.keys())
