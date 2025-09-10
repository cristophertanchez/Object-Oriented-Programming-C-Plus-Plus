# makeFunction.py
# Wraps the terrain matrix as a callable surface f(x,y) (bilinear interpolation)
# and provides helpers for extrema and volume. Includes a small demo.

import numpy as np
from terrainGenerator import generate_topology, visualize_terrain


# ---- Bilinear interpolation with friendly names ----
def _bilinear_interp(matrix, x, y, x_grid, y_grid):
    """
    Evaluate the surface at (x,y) by blending the four surrounding grid samples.
    - matrix is shape (H, W) with matrix[row, col] = matrix[y_index, x_index]
    - x_grid (W,) maps col index -> physical x
    - y_grid (H,) maps row index -> physical y
    Accepts scalars or arrays for x and y.
    """
    x = np.asarray(x)
    y = np.asarray(y)

    # Clamp query to domain
    x = np.clip(x, x_grid[0], x_grid[-1])
    y = np.clip(y, y_grid[0], y_grid[-1])

    # Convert to fractional grid indices (how many steps from left/bottom)
    dx = (x_grid[-1] - x_grid[0]) / (len(x_grid) - 1) if len(x_grid) > 1 else 1.0
    dy = (y_grid[-1] - y_grid[0]) / (len(y_grid) - 1) if len(y_grid) > 1 else 1.0
    ix = (x - x_grid[0]) / dx
    iy = (y - y_grid[0]) / dy

    # Which cell are we in? (left/right columns, bottom/top rows)
    left_col  = np.floor(ix).astype(int)
    bot_row   = np.floor(iy).astype(int)
    right_col = np.clip(left_col + 1, 0, len(x_grid) - 1)
    top_row   = np.clip(bot_row + 1, 0, len(y_grid) - 1)

    # Fractions inside the cell (0..1 toward right/up)
    frac_x = ix - left_col
    frac_y = iy - bot_row

    # Corner heights from the matrix
    z_bottom_left  = matrix[bot_row, left_col]
    z_bottom_right = matrix[bot_row, right_col]
    z_top_left     = matrix[top_row, left_col]
    z_top_right    = matrix[top_row, right_col]

    # Blend along x at bottom and top edges
    z_bottom = (1 - frac_x) * z_bottom_left + frac_x * z_bottom_right
    z_top    = (1 - frac_x) * z_top_left    + frac_x * z_top_right

    # Blend those across y
    return (1 - frac_y) * z_bottom + frac_y * z_top


def generateFunction(matrix, x_extent=(0.0, 1.0), y_extent=(0.0, 1.0)):
    """
    Turn a 2D elevation matrix into a callable surface f(x, y).
    Returns (f, meta) where f is vectorized and meta contains grids/spacings.
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
        "x_grid": x_grid, "y_grid": y_grid,
        "dx": dx, "dy": dy,
        "shape": (H, W),
        "matrix": matrix,
        "x_extent": x_extent, "y_extent": y_extent,
    }
    return f, meta


def find_extrema(matrix, x_extent=(0.0, 1.0), y_extent=(0.0, 1.0)):
    """Return (min_val,(xmin,ymin)), (max_val,(xmax,ymax)) at grid points."""
    H, W = matrix.shape
    j_min, i_min = np.unravel_index(np.argmin(matrix), (H, W))
    j_max, i_max = np.unravel_index(np.argmax(matrix), (H, W))

    x_grid = np.linspace(x_extent[0], x_extent[1], W)
    y_grid = np.linspace(y_extent[0], y_extent[1], H)

    return (matrix[j_min, i_min], (x_grid[i_min], y_grid[j_min])), \
           (matrix[j_max, i_max], (x_grid[i_max], y_grid[j_max]))


def volume_under_surface(matrix, x_extent=(0.0, 1.0), y_extent=(0.0, 1.0),
                         baseline=0.0, positive_only=False):
    """
    Approximate ∫∫(z - baseline) dA via a Riemann sum over the grid.
    If positive_only=True, negative parts are clipped to zero.
    """
    H, W = matrix.shape
    dx = (x_extent[1] - x_extent[0]) / (W - 1) if W > 1 else 1.0
    dy = (y_extent[1] - y_extent[0]) / (H - 1) if H > 1 else 1.0
    z = matrix - baseline
    if positive_only:
        z = np.maximum(z, 0.0)
    return z.sum() * dx * dy


# ------------ Demo ------------
if __name__ == "__main__":
    # 1) Generate terrain (repeatable via seed)
    terrain = generate_topology(Height=100, Width=120, alpha=1.5, seed=42)

    # 2) (Optional) visualize with y pointing UP and physical axis units
    visualize_terrain(terrain, x_extent=(0, 10), y_extent=(0, 8), y_up=True)

    # 3) Wrap as a continuous surface f(x,y)
    f, meta = generateFunction(terrain, x_extent=(0, 10), y_extent=(0, 8))

    # 4) Sample a few points
    xs = np.array([0.0, 2.5, 5.0, 7.5, 10.0])
    ys = np.array([0.0, 2.0, 4.0, 6.0, 8.0])
    print("f(xs, ys) =", f(xs, ys))

    # 5) Extrema + volume examples
    (zmin, (xmin, ymin)), (zmax, (xmax, ymax)) = find_extrema(terrain, (0, 10), (0, 8))
    print(f"Min z={zmin:.3f} at ({xmin:.2f},{ymin:.2f}); Max z={zmax:.3f} at ({xmax:.2f},{ymax:.2f})")

    vol = volume_under_surface(terrain, (0, 10), (0, 8), baseline=0.0, positive_only=True)
    print(f"Volume above baseline 0: {vol:.4f} (units^3)")
