import logging

from matplotlib.figure import Figure
from matplotlib.lines import Line2D

def graph(data):
    """
    The method that makes a matplotlib graph from data.
    """

    fig = Figure(dpi=90)
    axes = fig.add_axes((.05, .085, .92, .865))
    axes.set_xlabel('Time')

    colors = ('r', 'g', 'b', 'c', 'm', 'k', 'y')

    actors = {}
    actor_id = 0
    for from_act, to_act, x0, x1 in data:
        # TODO: Is this ugly?
        for actor in (from_act, to_act):
            if not actor in actors:
                actors[actor] = actor_id
                actor_id += 1
        # TODO: Style the arrows. Make different styles for different signal
        # types, if wanted. Make a legend for these (seperately fro actors?)
        axes.add_line(Line2D((x0, x1),(actors[from_act], actors[to_act])))

    axes.autoscale_view()
    lower_y, upper_y = axes.get_ylim()
    axes.set_ybound(lower=lower_y - .1 * upper_y, upper=upper_y + .1 * upper_y)

    axes.get_yaxis().set_visible(False)

    lower, upper = axes.get_xlim()
    for actor in actors:
        actor_id = actors[actor]
        color = colors[actor_id % len(actors)]
        axes.axhline(y=actor_id, linewidth=upper_y, color=color, label=actor)

    # Semi-unreadable code making half-guesses for margin size
    xmargin = min(.1, .1 * axes.get_data_ratio())
    axes.set_position((xmargin, .085, 1.0 - xmargin * 1.8, .865))

    # Make the legend, place it automatically...
    axes.legend(loc='best')

    return fig
