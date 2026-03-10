"""
03_plot_combinato_majorana.py
Genera figura combinata: ideale vs simulato + evoluzione realistica
"""

import matplotlib.pyplot as plt
import numpy as np

# Dati reali (sostituisci!)
times = np.linspace(0, 150, 400)
corr = -0.51 + 0.08 * np.sin(4 * np.pi * times / 50)  # sostituisci con tuoi corr

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.bar(['Ideal'], [-1], color='forestgreen', alpha=0.85)
ax1.bar(['Simulated'], [0], color='gray', alpha=0.75)
ax1.set_ylim(-1.1, 0.1)
ax1.set_title('Ideal vs Simulated (μ=0)')

ax2.plot(times, corr, lw=2.8, color='darkred')
ax2.axhline(-1, color='g--', lw=2)
ax2.set_ylim(-1.1, 0.1)
ax2.set_title('Evoluzione realistica')

plt.suptitle('Correlatore Majorana')
plt.tight_layout()
plt.savefig('combined_majorana_plots.pdf', dpi=300)
plt.show()