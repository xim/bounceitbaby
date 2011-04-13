import logging

from matplotlib.dates import DateFormatter, date2num
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch
from matplotlib.ticker import MaxNLocator

from utils import parse_timestamp

def graph(data):
    """
    The method that makes a matplotlib graph from data.

    Data is a list of importer.DataItem objects
    """

    fig = Figure(dpi=90, figsize=(25, 1))
    axes = fig.add_axes((.05, .085, .92, .865))
    axes.xaxis.set_minor_locator(MaxNLocator(nbins=25))

    time_format = DateFormatter('%H:%M:%S')
    axes.xaxis.set_major_formatter(time_format)
    axes.set_xlabel('Time')

    colors = ('r', 'g', 'b', 'c', 'm', 'k')
    arrows = [('fancy', (.25, .25, 0)), ('simple', (0, .5, 0)),
            ('wedge', (0, 0, .5)), ('-|>', (.5, 0, 0)), ('->', 'k')]

    actors = {}
    msg_types = {}
    max_actor_id = -1
    min_xvalue = 999999
    max_xvalue = 0
    for item in data:
        # TODO: Is this ugly? Maybe not ugly enough to do something about it?
        for actor in (item.recipient, item.sender):
            if not actor in actors:
                max_actor_id += 1
                actors[actor] = max_actor_id

        x0, y0 = item.sent_time, actors[item.sender]
        x1, y1 = (item.rcvd_time or x0), actors[item.recipient]

        if isinstance(x0, basestring):
            x0 = date2num(parse_timestamp(x0))
        if isinstance(x1, basestring):
            x1 = date2num(parse_timestamp(x1))

        if x0 < min_xvalue:
            min_xvalue = x0
        if x1 > max_xvalue:
            max_xvalue = x1

        if not item.msg_type in msg_types:
            msg_types[item.msg_type] = arrows.pop()

        arrow, color = msg_types[item.msg_type]
        logging.debug('Adding arrow from (%s, %s) to (%s, %s)' % (
                x0, y0, x1, y1))
        try:
            axes.add_patch(FancyArrowPatch(
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

    axes.set_ybound(lower=-.1 * max_actor_id, upper=max_actor_id + .1 * max_actor_id)
    x_margin = (max_xvalue - min_xvalue) * .01
    axes.set_xbound(lower=min_xvalue - x_margin, upper=max_xvalue + x_margin)

    axes.yaxis.set_visible(False)

    for actor in actors:
        a_id = actors[actor]
        color = colors[a_id % len(actors)]
        axes.axhline(y=a_id, linewidth=max_actor_id, color=color, label=actor)

    # Semi-unreadable code making half-guesses for margin size
    xmargin = min(.1, .1 * axes.get_data_ratio())
    axes.set_position((xmargin, .085, 1.0 - xmargin * 1.8, .865))

    # Make the legends, place them automatically...
    legend1 = axes.legend(loc='upper left')
    arrows = []
    if len(msg_types) > 1:
        for _, (arrow, color) in msg_types.iteritems():
            arrows.append(FancyArrowPatch(
                    (x0, y0), (x1, y1), linewidth=1.3, color=color,
                    arrowstyle=arrow, mutation_scale=20))
        axes.legend(arrows, msg_types, loc='lower left')
        axes.add_artist(legend1)

    axes.grid()

    return fig
