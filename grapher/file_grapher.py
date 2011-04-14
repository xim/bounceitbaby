from matplot import Graph

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def save_png_file(data, linear=False, file_prefix='out'):
    figure = Graph(data, linear=linear)
    canvas = FigureCanvas(figure)

    figure.savefig(filename=file_prefix + '.png')
