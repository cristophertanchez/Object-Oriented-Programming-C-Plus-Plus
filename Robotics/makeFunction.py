# makeFunction.py
# Requires terrainGenerator.py in the same folder.
# Implements: generateFunction(matrix, x_extent, y_extent) -> callable f(x, y)

import numpy as np
from terrainGenerator import generate_topology  # provided by the assignment

def _bilinear_interp(z, x, y, x_grid, y_grid):
    """
    Bilinear interpolation on a rectilinear grid.
    z: (H, W) array on grid (x_grid, y_grid)
    x, y: arrays or scalars in continuous coordinates within [x_grid[0], x_grid[-1]] and [y_grid[0], y_grid[-1]]
    Returns interpolated z at (x, y) with shape broadcast from x,y.
    """
    x = np.asarray(x)
    y = np.asarray(y)

    # Clip to domain
    x = np.clip(x, x_grid[0], x_grid[-1])
    y = np.clip(y, y_grid[0], y_grid[-1])

    # Convert to fractional indices
    dx = (x_grid[-1] - x_grid[0]) / (len(x_grid) - 1)
    dy = (y_grid[-1] - y_grid[0]) / (len(y_grid) - 1)

    ix = (x - x_grid[0]) / dx
    iy = (y - y_grid[0]) / dy

    i0 = np.floor(ix).astype(int)
    j0 = np.floor(iy).astype(int)
    i1 = np.clip(i0 + 1, 0, len(x_grid) - 1)
    j1 = np.clip(j0 + 1, 0, len(y_grid) - 1)

    tx = ix - i0
    ty = iy - j0

    # Gather the four corners
    z00 = z[j0, i0]
    z10 = z[j0, i1]
    z01 = z[j1, i0]
    z11 = z[j1, i1]

    # Bilinear blend
    z0 = (1 - tx) * z00 + tx * z10
    z1 = (1 - tx) * z01 + tx * z11
    return (1 - ty) * z0 + ty * z1


def generateFunction(matrix, x_extent=(0.0, 1.0), y_extent=(0.0, 1.0)):
    """
    Turn a 2D elevation matrix into a callable surface f(x, y).

    Parameters
    ----------
    matrix : np.ndarray of shape (Height, Width)
        Elevation values (e.g., 0..1).
    x_extent : (xmin, xmax)
    y_extent : (ymin, ymax)

    Returns
    -------
    f : function
        Callable f(x, y) that supports scalars or NumPy arrays and returns elevations.
    meta : dict
        Useful metadata: grid vectors, cell sizes, shape, and the original matrix.
    """
    matrix = np.asarray(matrix)
    H, W = matrix.shape

    x_grid = np.linspace(x_extent[0], x_extent[1], W)
    y_grid = np.linspace(y_extent[0], y_extent[1], H)
    dx = (x_extent[1] - x_extent[0]) / (W - 1) if W > 1 else 1.0
    dy = (y_extent[1] - y_extent[0]) / (H - 1) if H > 1 else 1.0

    def f(x, y):
        return _bilinear_interp(matrix, x, y, x_grid, y_grid)

    meta = {
        "x_grid": x_grid,
        "y_grid": y_grid,
        "dx": dx,
        "dy": dy,
        "shape": (H, W),
        "matrix": matrix,
        "x_extent": x_extent,
        "y_extent": y_extent,
    }
    return f, meta


# ---------- Analysis helpers (optional but handy) ----------

def find_extrema(matrix, x_extent=(0.0, 1.0), y_extent=(0.0, 1.0)):
    """
    Return (min_val, (xmin, ymin)), (max_val, (xmax, ymax)) based on grid samples.
    """
    H, W = matrix.shape
    j_min, i_min = np.unravel_index(np.argmin(matrix), (H, W))
    j_max, i_max = np.unravel_index(np.argmax(matrix), (H, W))

    x_grid = np.linspace(x_extent[0], x_extent[1], W)
    y_grid = np.linspace(y_extent[0], y_extent[1], H)

    min_val = matrix[j_min, i_min]
    max_val = matrix[j_max, i_max]
    return (min_val, (x_grid[i_min], y_grid[j_min])), (max_val, (x_grid[i_max], y_grid[j_max]))


def volume_under_surface(matrix, x_extent=(0.0, 1.0), y_extent=(0.0, 1.0), baseline=0.0, positive_only=False):
    """
    Approximate volume via Riemann sum over the grid.
    If positive_only=True, integrates max(z - baseline, 0); else integrates (z - baseline).
    """
    H, W = matrix.shape
    dx = (x_extent[1] - x_extent[0]) / (W - 1) if W > 1 else 1.0
    dy = (y_extent[1] - y_extent[0]) / (H - 1) if H > 1 else 1.0
    cell_area = dx * dy

    z = matrix - baseline
    if positive_only:
        z = np.maximum(z, 0.0)
    return z.sum() * cell_area


# ---------- Minimal demo ----------

if __name__ == "__main__":
    # Example: generate a terrain and wrap it as f(x, y)
    terrain = generate_topology(Height=100, Width=120, alpha=1.5, seed=42)
    f, meta = generateFunction(terrain, x_extent=(0, 10), y_extent=(0, 8))

    # Query the surface at a few points:
    xs = np.array([0.0, 2.5, 5.0, 7.5, 10.0])
    ys = np.array([0.0, 2.0, 4.0, 6.0, 8.0])
    samples = f(xs, ys)  # vectorized

    # Extrema on the sampled grid:
    (zmin, (xmin, ymin)), (zmax, (xmax, ymax)) = find_extrema(terrain, (0, 10), (0, 8))

    # Volume above baseline 0 (heights are 0..1)
    vol = volume_under_surface(terrain, (0,10), (0,8), baseline=0.0, positive_only=True)

    print("Sample f(xs, ys):", samples)
    print(f"Min z={zmin:.3f} at ({xmin:.2f}, {ymin:.2f}); Max z={zmax:.3f} at ({xmax:.2f}, {ymax:.2f})")
    print(f"Volume above baseline 0: {vol:.4f} (units^3)")
