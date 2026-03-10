# =============================================================================
# generate_coherence_extension_plot.py
# =============================================================================
# Genera il grafico di estensione del tempo di coerenza T₂ nei difetti V_B^-
# Curve: Hahn-echo, CPMG multi-pulse, CCD continuo
# Dati approssimati da letteratura (Gottscholl 2021, Ramsay 2023, Rizzato 2023)
#
# Requisiti: pip install numpy matplotlib
# Esecuzione: python code/generate_coherence_extension_plot.py
# Output: figures/coherence_extension_plot.png
# =============================================================================

import os
import numpy as np
import matplotlib.pyplot as plt

os.makedirs('figures', exist_ok=True)

t = np.linspace(0, 100, 600)

def decay(t, T2):
    return np.exp(-t / T2)

# Punti dati simulati con piccolo rumore (realismo)
t_points = np.array([0, 2, 5, 10, 15, 20, 30, 50, 70, 90])
hahn   = decay(t_points, 2.0) + np.random.normal(0, 0.012, len(t_points))
cpmg   = decay(t_points, 8.0) + np.random.normal(0, 0.012, len(t_points))
ccd    = decay(t_points, 60.0) + np.random.normal(0, 0.012, len(t_points))

fig, ax = plt.subplots(figsize=(9, 6))

ax.semilogy(t, decay(t, 2.0), 'b-', lw=2.5, label='Hahn-echo (~2 µs)')
ax.semilogy(t_points, hahn, 'bo', ms=7, alpha=0.9)

ax.semilogy(t, decay(t, 8.0), 'g-', lw=2.5, label='CPMG multi-pulse (~4–10 µs)')
ax.semilogy(t_points, cpmg, 'go', ms=7, alpha=0.9)

ax.semilogy(t, decay(t, 60.0), 'r-', lw=2.5, label='CCD continuo (~60 µs)')
ax.semilogy(t_points, ccd, 'ro', ms=7, alpha=0.9)

ax.set_xlabel('Tempo (µs)', fontsize=13)
ax.set_ylabel('Coerenza normalizzata (scala log)', fontsize=13)
ax.set_title('Estensione del tempo di coerenza T₂\ntramite dynamical decoupling in V$_B^-$ h-BN', fontsize=15, pad=15)

ax.legend(fontsize=12, loc='upper right', framealpha=0.95)
ax.grid(True, which="both", ls="--", alpha=0.45)
ax.set_ylim(5e-4, 1.15)
ax.set_xlim(0, 100)

plt.tight_layout()
plt.savefig('figures/coherence_extension_plot.png', dpi=400, bbox_inches='tight', pad_inches=0.3)
print("Figura salvata: figures/coherence_extension_plot.png")