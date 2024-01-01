import pyvista as pv
import numpy as np


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