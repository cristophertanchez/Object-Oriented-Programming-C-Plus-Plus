# terrainGenerator.py
# Generates a 2D terrain matrix using a 1/f^alpha spectrum
# and provides a clean visualizer.

import numpy as np
import matplotlib.pyplot as plt


def generate_topology(Height: int, Width: int, alpha: float = 1.5, seed: int | None = None) -> np.ndarray:
    """
    Create a (Height x Width) NumPy array of values in [0, 1] that look like terrain elevations.
    alpha controls smoothness (larger -> smoother). seed makes it repeatable.
    """
    if seed is not None:
        np.random.seed(seed)

    # Frequency grid (cycles per pixel) for rows (ky) and cols (kx)
    ky = np.fft.fftfreq(Height).reshape(-1, 1)   # (H,1)
    kx = np.fft.fftfreq(Width).reshape(1, -1)    # (1,W)
    freq = np.sqrt(kx**2 + ky**2)
    freq[0, 0] = 1e-6  # avoid divide-by-zero at DC

    # Random phase, amplitude shaped as 1/f^alpha
    phase = np.random.rand(Height, Width) * 2 * np.pi
    spectrum = (1.0 / (freq**alpha)) * (np.cos(phase) + 1j * np.sin(phase))

    # Bring it back to spatial domain and normalize to [0, 1]
    field = np.fft.ifft2(spectrum).real
    field -= field.min()
    denom = field.max() - field.min() + 1e-12
    field /= denom
    return field


def visualize_terrain(
    terrain: np.ndarray,
    x_extent: tuple[float, float] | None = None,
    y_extent: tuple[float, float] | None = None,
    y_up: bool = True,
    title: str = "Generated Terrain",
) -> None:
    """
    Show a heatmap of the terrain. If extents are given, axes are labeled in those units.
    y_up=True makes the plot's y-axis increase upward (matches standard math).
    """
    H, W = terrain.shape
    if x_extent is None:
        x_extent = (0, W - 1)
    if y_extent is None:
        y_extent = (0, H - 1)

    origin = "lower" if y_up else "upper"
    plt.imshow(
        terrain,
        cmap="terrain",
        origin=origin,
        extent=(x_extent[0], x_extent[1], y_extent[0], y_extent[1]),
        aspect="auto",
    )
    plt.colorbar(label="Relative Elevation")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(title)
    plt.show()


if __name__ == "__main__":
    # Quick manual check
    T = generate_topology(Height=100, Width=120, alpha=1.5, seed=42)
    visualize_terrain(T, x_extent=(0, 10), y_extent=(0, 8), y_up=True)
