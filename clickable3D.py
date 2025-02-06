import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

def on_click(event):
    if event.inaxes != ax:
        return

    # Get the 2D coordinates of the click
    x2d, y2d = event.xdata, event.ydata
    
    # Find the z coordinate by interpolating the surface data
    z2d = griddata((X.flatten(), Y.flatten()), Z.flatten(), (x2d, y2d), method='linear')
    
    if not np.isnan(z2d):
        print(f"Clicked surface at coordinates: x={x2d:.2f}, y={y2d:.2f}, z={z2d:.2f}")
    else:
        print("Click was not on the surface")

# Create a simple surface (a paraboloid)
x = np.linspace(-2, 2, 30)
y = np.linspace(-2, 2, 30)
X, Y = np.meshgrid(x, y)
Z = X**2 + Y**2

# Create the plot
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
surf = ax.plot_surface(X, Y, Z, cmap='viridis')

# Add a title
ax.set_title('Click anywhere on the surface')

# Connect the click event
fig.canvas.mpl_connect('button_press_event', on_click)

# Add labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()