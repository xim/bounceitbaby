import logging

from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch
from matplotlib.ticker import MaxNLocator

def graph(data):
    """
    The method that makes a matplotlib graph from data.

    Data is a list of tuples. Each tuple:
    (from, to, time_left, time_recv, sigtype)
    If you don't have a sigtype, pass e.g. '', '_' or None
    """

    fig = Figure(dpi=90, figsize=(25, 1))
    axes = fig.add_axes((.05, .085, .92, .865))
    axes.xaxis.set_minor_locator(MaxNLocator(nbins=25))
    axes.set_xlabel('Time')

    colors = ('r', 'g', 'b', 'c', 'm', 'k')
    arrows = [('fancy', (.25, .25, 0)), ('simple', (0, .5, 0)),
            ('wedge', (0, 0, .5)), ('-|>', (.5, 0, 0)), ('->', 'k')]

    actors = {}
    sigtypes = {}
    max_actor_id = -1
    for from_act, to_act, x0, x1, sigtype in data:
        # TODO: Is this ugly? Maybe not ugly enough to do something about it?
        for actor in (from_act, to_act):
            if not actor in actors:
                max_actor_id += 1
                actors[actor] = max_actor_id

        x0, y0, x1, y1 = float(x0), actors[from_act], float(x1), actors[to_act]

        if not sigtype in sigtypes:
            sigtypes[sigtype] = arrows.pop()

        arrow, color = sigtypes[sigtype]
        axes.add_patch(FancyArrowPatch(
                (x0, y0), (x1, y1), linewidth=1.3, color=color,
                arrowstyle=arrow, mutation_scale=20))

    axes.autoscale_view()
    axes.set_ybound(lower=-.1 * max_actor_id, upper=max_actor_id + .1 * max_actor_id)

    axes.yaxis.set_visible(False)

    lower, upper = axes.get_xlim()
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
    if len(sigtypes) > 1:
        for sigtype, (arrow, color) in sigtypes.iteritems():
            arrows.append(FancyArrowPatch(
                    (x0, y0), (x1, y1), linewidth=1.3, color=color,
                    arrowstyle=arrow, mutation_scale=20))
        axes.legend(arrows, sigtypes, loc='lower left')
        axes.add_artist(legend1)

    axes.grid()

    return fig
