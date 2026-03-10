# =============================================================================
# Plot confronto fasi n=3 vs many-body + autovalori su cerchio unitario
# File: code/plot_phases_comparison.py
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt

phi = (1 + np.sqrt(5)) / 2

# Fasi reali da QuTiP n=3 (dal tuo output)
phases_n3 = np.array([2.513274, -0.628319])

# Fasi teoriche many-body k=1..50
k_values = np.arange(1, 51)
wrapped_theory = [((2*np.pi*k/phi + np.pi) % (2*np.pi)) - np.pi for k in k_values]

plt.figure(figsize=(12, 8))

# Subplot 1: fasi wrapped vs k
ax1 = plt.subplot(2,1,1)
ax1.plot(k_values, wrapped_theory, 'o-', color='green', markersize=4, label='Teorico many-body ($2\pi k / \phi$)')
ax1.scatter([3,6], phases_n3, color='red', s=100, marker='*', label='Numerico n=3 (QuTiP)')
ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
ax1.set_ylim(-np.pi-0.5, np.pi+0.5)
ax1.set_yticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
ax1.set_yticklabels([r'$-\pi$', r'$-\pi/2$', '0', r'$\pi/2$', r'$\pi$'])
ax1.set_xlabel('Indice braiding $k$')
ax1.set_ylabel('Fase wrapped (rad)')
ax1.set_title('Confronto fasi wrapped: n=3 vs limite many-body')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Subplot 2: autovalori su cerchio unitario
ax2 = plt.subplot(2,1,2)
circle = plt.Circle((0,0), 1, color='gray', fill=False, linestyle='--')
ax2.add_artist(circle)
ax2.scatter(np.real([-0.809017 + 0.587785j, 0.809017 - 0.587785j]),
            np.imag([-0.809017 + 0.587785j, 0.809017 - 0.587785j]),
            color='blue', s=100, label='Autovalori M (n=3)')
ax2.set_xlim(-1.2, 1.2)
ax2.set_ylim(-1.2, 1.2)
ax2.set_aspect('equal')
ax2.set_xlabel('Re')
ax2.set_ylabel('Im')
ax2.set_title('Autovalori di M su cerchio unitario (modulo ≈1)')
ax2.grid(True, alpha=0.3)
ax2.legend()

plt.tight_layout()
plt.savefig('code/monodromy_comparison_plot.png', dpi=300, bbox_inches='tight')
print("Plot salvato: code/monodromy_comparison_plot.png")