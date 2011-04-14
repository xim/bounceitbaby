from matplot import Graph

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def save_file(data, linear=False, output_file='out.png'):
    figure = Graph(data, linear=linear)

    # This updates the Figure object with a reference to the FigureCanvasAgg
    # object so it knows how to save to file.
    canvas = FigureCanvas(figure)

    figure.savefig(filename=output_file)
