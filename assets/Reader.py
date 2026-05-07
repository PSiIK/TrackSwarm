import numpy as np
import matplotlib.pyplot as plt
def generuj_obraz_z_log_odds(nazwa_pliku):
    surowy_grid = np.load(nazwa_pliku)
    prob_grid = 1.0 - (1.0 / (1.0 + np.exp(surowy_grid)))
    obrazek = 1.0 - prob_grid
    plt.imshow(obrazek, cmap='gray', origin='lower')
    plt.colorbar(label='Prawdopodobieństwo braku przeszkody')
    plt.title(f"Wygenerowano z: {nazwa_pliku}")
    nazwa_png = nazwa_pliku.replace(".npy", ".png")
    plt.savefig(nazwa_png, dpi=300)
    plt.show()
generuj_obraz_z_log_odds("submap2.npy")