import numpy as np
import matplotlib.pyplot as plt

def generate_topology(Height, Width, alpha, seed):
    np.random.seed(seed)

    # Frequency grid
    ky = np.fft.fftfreq(Height).reshape(-1, 1)
    kx = np.fft.fftfreq(Width).reshape(1, -1)
    freq = np.sqrt(kx**2 + ky**2)
    freq[0, 0] = 1e-6  # avoid divide-by-zero at DC

    # Random complex spectrum with 1/f^alpha amplitude
    phase = np.exp(1j * 2 * np.pi * np.random.rand(Height, Width))
    amplitude = 1.0 / (freq ** alpha)
    spectrum = amplitude * phase

    # Inverse FFT to get spatial "terrain"
    terrain_complex = np.fft.ifft2(spectrum)
    terrain = np.real(terrain_complex)

    # Normalize to [0, 1]
    terrain -= terrain.min()
    terrain /= (terrain.max() - terrain.min())

    return terrain

terrain1 = generate_topology(Height = 100,Width = 100, alpha = 1.5,seed = 42)

def visualize_terrain(terrain):
    plt.imshow(terrain, cmap='gray')
    # Visualize
    plt.imshow(terrain, cmap="terrain")
    plt.colorbar(label="Relative Elevation")
    plt.title("Data of {terrain.name}")
    plt.show()

#visualize_terrain(terrain1)
#print(terrain1)
