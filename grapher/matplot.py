import logging

from matplotlib.figure import Figure
from matplotlib.lines import Line2D

def graph(data):
    """
    The method that makes a matplotlib graph from data.
    """
    # TODO: Oooh, the horror! Figure out how we are supposed to get this!
    data = list(data)
    actors = set(d[0] for d in data) | set(d[1] for d in data)
    # END Oooh, the horror!

    f = Figure(dpi=90)
    a = f.add_axes((.05, .085, .92, .865))
    a.set_xlabel('Time')

    # TODO: More colors or % len on len(actors) > len(colors)?
    colors = ('r', 'g', 'b', 'c', 'm', 'k', 'y')

    actors = dict((actor, number) for actor, number in \
            zip(actors, range(len(actors))))

    for from_act, to_act, x0, x1 in data:
        a.add_line(Line2D((x0, x1),(actors[from_act], actors[to_act])))

    a.autoscale_view()
    lower_y, upper_y = a.get_ylim()
    a.set_ybound(lower=lower_y - .1 * upper_y, upper=upper_y + .1 * upper_y)

    a.get_yaxis().set_visible(False)

    lower, upper = a.get_xlim()
    for actor in actors:
        color = colors[actors[actor]]
        a.axhline(y=actors[actor], linewidth=upper_y, color=color, label=actor)

    # Semi-unreadable code making half-guesses for margin size
    xmargin = min(.1, .1 * a.get_data_ratio())
    a.set_position((xmargin, .085, 1.0 - xmargin * 1.8, .865))

    # Make the legend, place it automatically...
    a.legend(loc='best')

    return f
