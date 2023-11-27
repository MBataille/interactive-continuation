# Imports
from PySide6 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib
import numpy as np

# Ensure using PyQt5 backend
matplotlib.use('QT5Agg')

# Matplotlib canvas class to create figure
class MplCanvas(Canvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)


# Matplotlib widget
class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)   # Inherit from QWidget
        self.canvas = MplCanvas()                  # Create canvas object
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.vbl.addWidget(self.toolbar)
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

        self.lines = {}

    def plot(self, *args, name=None, clear=False, **kwargs):
        if clear:
            self.canvas.ax.clear()
        if name:
            self.lines[name], = self.canvas.ax.plot(*args, **kwargs)
        else:
            self.canvas.ax.plot(*args, **kwargs)
        
        self.canvas.draw()

    def set_lims(self, xlims, ylims):
        self.canvas.ax.set_xlim(*xlims)
        self.canvas.ax.set_ylim(*ylims)

    def update(self, name, xs, ys, *args, auto_lims=False, **kwargs):
        self.lines[name].set_data(xs, ys, *args, **kwargs)

        if auto_lims:
            xs_minmax = np.min(xs) * 0.9, np.max(xs) * 1.1
            ys_minmax = np.min(ys) * 0.9, np.max(ys) * 1.1
            
            self.set_lims(xs_minmax, ys_minmax)

        self.canvas.draw()