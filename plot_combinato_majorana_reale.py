"""
plot_combinato_majorana_reale.py
Genera figura combinata per paper: ideale vs simulato (sinistra) + evoluzione realistica (destra)
Salva come combined_majorana_plots.pdf
"""

import matplotlib.pyplot as plt
import numpy as np

# ================================
# I TUOI DATI REALI (sostituisci!)
# ================================
# Dati dal tuo ultimo run realistico (esempio con oscillazioni ~ -0.51)
times = np.linspace(0, 150, 400)  # tempo braiding
corr = -0.51 + 0.08 * np.sin(4 * np.pi * times / 50 + np.random.randn(len(times)) * 0.03)  # SOSTITUISCI con i tuoi corr reali

# ================================
# Plot combinato
# ================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [1, 2]})

# Subplot 1: bar ideale vs simulato (degenere)
ax1.bar(['Ideal'], [-1], color='forestgreen', alpha=0.85, width=0.6, label='Ideal protected (-1)')
ax1.bar(['Simulated'], [0], color='gray', alpha=0.75, width=0.6, label='Simulated (degenerate GS)')
ax1.axhline(0, color='black', lw=0.8, ls=':')
ax1.set_ylabel('Majorana Correlator ⟨γ₁ γ_N⟩', fontsize=13)
ax1.set_title('Ideal vs Simulated (N=12, μ=0)', fontsize=13)
ax1.set_ylim(-1.1, 0.1)
ax1.legend(fontsize=11, loc='upper right')
ax1.grid(True, alpha=0.3, axis='y')

# Subplot 2: evoluzione realistica
ax2.plot(times, corr, lw=2.8, color='darkred', label='⟨γ₁ γ_N⟩ (realistico)')
ax2.axhline(-1, color='forestgreen', ls='--', lw=2.2, alpha=0.9, label='Ideale protetto (-1)')
ax2.axhline(0, color='gray', ls=':', lw=1.5, alpha=0.7, label='Decoerente (0)')
ax2.set_xlabel('Tempo braiding (unità arbitrarie)', fontsize=13)
ax2.set_ylabel('Correlatore Majorana', fontsize=13)
ax2.set_title('Evoluzione con decoerenza + braiding', fontsize=13)
ax2.set_ylim(-1.1, 0.1)
ax2.legend(fontsize=11, loc='upper right')
ax2.grid(True, alpha=0.3)

# Titolo generale e layout
fig.suptitle('Correlatore Majorana: Ideale vs Realistico', fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('combined_majorana_plots.pdf', dpi=300, bbox_inches='tight')
plt.show()

print("Plot combinato salvato come 'combined_majorana_plots.pdf'")