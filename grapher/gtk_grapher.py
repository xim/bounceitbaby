"""
adding a FigureCanvasGTK/GTKAgg widget to a gtk.ScrolledWindow
"""

import gtk

from matplotlib.figure import Figure
from matplotlib.lines import Line2D

from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas

def graph(data):

    # from, to, time, time ## color/type
    #data = (('Input', 'Output', 0, .75), ('Output', 'Input', 8.3, 9.45), ('Input', 'Undef', 19.65, 20.85))
    win = gtk.Window()
    win.connect("destroy", lambda x: gtk.main_quit())
    win.set_default_size(800,500)
    win.set_title("GTK window")

    f = Figure(dpi=90)
    a = f.add_axes((.05, .085, .92, .865))
    a.set_xlabel('Time')

    colors = ('r', 'g', 'b', 'c', 'm', 'k', 'y')

    actors = ('Input', 'Output', 'Undef')

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

    a.legend(loc='best')

    dataratio = a.get_data_ratio()
    xmargin = min(.1, .1 * dataratio)
    a.set_position((xmargin, .085, 1.0 - xmargin * 1.8, .865))

    sw = gtk.ScrolledWindow()
    win.add(sw)
    # policy: ALWAYS, AUTOMATIC, NEVER
    sw.set_policy(hscrollbar_policy=gtk.POLICY_ALWAYS,
                  vscrollbar_policy=gtk.POLICY_AUTOMATIC)

    canvas = FigureCanvas(f)
    canvas.set_size_request(int(400 / dataratio), 400)
    sw.add_with_viewport(canvas)

    win.show_all()
    gtk.main()
