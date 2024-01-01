import pyvista as pv
import numpy as np

from mne.viz.backends.renderer import _get_renderer


plotter = pv.Plotter(off_screen=True)

# Create a uniform grid
grid = pv.UniformGrid()

# put 1 point in each cell
grid.dimensions = [10, 10, 10]

plotter.add_mesh(grid, show_edges=True)

plotter.screenshot('output.png')

# Now plot the grid!
# grid.plot(show_edges=True, off_screen=True)

# create a screenshot
# grid.screenshot("grid.png")

renderer = _get_renderer(size=(600, 600), bgcolor=(0.5, 0.5, 0.5))

renderer.plotter.off_screen = True
print(renderer)