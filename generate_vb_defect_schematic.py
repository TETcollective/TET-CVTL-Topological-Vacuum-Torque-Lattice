# =============================================================================
# generate_vb_defect_schematic.py
# =============================================================================
# Genera la figura multi-panel per lo schema del difetto V_B^- in h-BN
# Pannelli:
#   1. Struttura atomica semplificata del reticolo h-BN con vacanza del boro
#   2. Diagramma livelli energetici (Ground State, Metastable, Excited State)
#   3. Spettro ODMR semplificato (contrasto vs frequenza intorno a 3.5 GHz)
#
# Requisiti:
#   pip install matplotlib numpy ase
#
# Esecuzione: python code/generate_vb_defect_schematic.py
# Output: figures/vb_defect_schematic.png (crea cartella figures/ se non esiste)
# =============================================================================

import os
import numpy as np
import matplotlib.pyplot as plt
from ase import Atoms
from ase.visualize.plot import plot_atoms
from matplotlib.patches import FancyArrowPatch

# Crea cartella figures se non esiste
os.makedirs('figures', exist_ok=True)

# Figura con layout 1x3
fig = plt.figure(figsize=(16, 5.5))
gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1], wspace=0.45)
axs = [fig.add_subplot(gs[i]) for i in range(3)]

# ────────────────────────────────────────────────
# Panel 1: Struttura atomica V_B^-
# ────────────────────────────────────────────────
positions = [
    (0.0,   0.0,   0),     # N1
    (1.45,  0.0,   0),     # Posizione vacanza B
    (0.725, 1.26,  0),     # N2
    (2.175, 1.26,  0),     # N3
    (-0.725,1.26,  0),     # B2
    (1.45,  2.52,  0),     # B3
    (2.9,   0.0,   0),     # N4 (estensione)
]
symbols = ['N', 'X', 'N', 'N', 'B', 'B', 'N']
colors   = ['#228B22' if s=='N' else '#4169E1' if s=='B' else '#FF4500' for s in symbols]

atoms = Atoms(symbols=symbols, positions=positions, cell=(5.5, 5.5, 10), pbc=(1,1,0))

plot_atoms(atoms, axs[0], radii=0.58, rotation=('0x,0y,0z'), colors=colors)
axs[0].set_title('Struttura atomica del difetto V$_B^-$', fontsize=13, pad=10)
axs[0].set_axis_off()
axs[0].text(1.45, 0.3, 'V$_B^-$', color='red', fontsize=14, ha='center', fontweight='bold')
axs[0].text(0.0, -0.6, 'N', color='green', fontsize=11)
axs[0].text(2.175, 1.6, 'N', color='green', fontsize=11)

# ────────────────────────────────────────────────
# Panel 2: Livelli energetici
# ────────────────────────────────────────────────
axs[1].set_xlim(0, 13)
axs[1].set_ylim(0, 5.8)
axs[1].axis('off')

# Livelli
axs[1].hlines(0.9, 3.5, 9.5, color='black', lw=3)
axs[1].text(0.8, 0.9, '³A₂′ (GS)', fontsize=12, va='center')
axs[1].hlines(2.6, 3.5, 9.5, color='black', lw=3)
axs[1].text(0.8, 2.6, '¹A′ (MS)', fontsize=12, va='center')
axs[1].hlines(4.5, 3.5, 9.5, color='black', lw=3)
axs[1].text(0.8, 4.5, '³E″ (ES)', fontsize=12, va='center')

# Frecce
arrow_kw = dict(arrowstyle="->", mutation_scale=20, lw=2.2)
axs[1].add_patch(FancyArrowPatch((6.5, 0.9), (6.5, 4.5), color='green', **arrow_kw))
axs[1].add_patch(FancyArrowPatch((7.8, 4.5), (7.8, 0.9), color='red', **arrow_kw))
axs[1].add_patch(FancyArrowPatch((9.2, 4.5), (9.2, 2.6), color='black', ls='dashed', **arrow_kw))
axs[1].add_patch(FancyArrowPatch((9.8, 2.6), (9.8, 0.9), color='black', ls='dashed', **arrow_kw))

axs[1].text(6.7, 2.7, 'Eccitazione ottica', color='green', fontsize=10, rotation=90)
axs[1].text(8.0, 2.7, 'Emissione PL (~2 eV)', color='red', fontsize=10, rotation=90)
axs[1].text(9.4, 3.55, 'ISC', color='black', fontsize=10, rotation=90)
axs[1].text(10.0, 1.75, 'ISC', color='black', fontsize=10, rotation=90)

axs[1].set_title('Livelli energetici del difetto V$_B^-$', fontsize=13, pad=10)

# ────────────────────────────────────────────────
# Panel 3: ODMR
# ────────────────────────────────────────────────
freq = np.linspace(3.0, 4.0, 600)
odmr = 0.32 * np.exp(-((freq - 3.5)**2 / (2 * 0.045**2)))

axs[2].plot(freq, odmr, color='#1f77b4', lw=2.8)
axs[2].set_xlabel('Frequenza (GHz)', fontsize=11)
axs[2].set_ylabel('Contrastro ODMR (%)', fontsize=11)
axs[2].set_title('Spettro ODMR semplificato', fontsize=13, pad=10)
axs[2].grid(True, alpha=0.35, ls='--')
axs[2].set_ylim(0, 0.38)
axs[2].set_xlim(3.0, 4.0)
axs[2].axvline(3.5, color='gray', ls='--', lw=1.2, alpha=0.8)

# Titolo generale
fig.suptitle('Schema del difetto V$_B^-$ in h-BN: struttura atomica, livelli energetici e ODMR',
             fontsize=15, fontweight='bold', y=1.02)

# Salva
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('figures/vb_defect_schematic.png', dpi=400, bbox_inches='tight', pad_inches=0.4)
print("Figura salvata: figures/vb_defect_schematic.png")