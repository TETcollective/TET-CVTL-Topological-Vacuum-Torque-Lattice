# =============================================================================
# TET--CVTL Project - Monodromy Trefoil con QuTiP per Fibonacci Anyons
# File: code/monodromy_fibonacci_qutip.py
# Descrizione: Calcola monodromy operator M = σ₁ σ₂ σ₁ per 3 Fibonacci anyons,
#              estrae autovalori e fasi wrapped, genera coordinate per TikZ plot.
# Autore: Symon (Tetcollective.org) - Data: Marzo 2026
# Dipendenze: qutip, numpy
# =============================================================================

import numpy as np
import qutip as qt
from qutip import Qobj
import os # Import the os module for directory creation

# Golden ratio con alta precisione
phi = (1 + np.sqrt(5)) / 2

# Matrice F (fusion, standard Fibonacci τττ → τ)
F = np.array([
    [phi**(-1),     phi**(-0.5)],
    [phi**(-0.5),   -phi**(-1) ]
], dtype=complex)

# Matrice R (braiding phases, standard)
R = qt.Qobj(np.diag([np.exp(1j * 4*np.pi/5), np.exp(-1j * 3*np.pi/5)]))

# σ₁ = R (scambio primi due anyons)
sigma1 = R

# σ₂ = F⁻¹ R F
F_dag = qt.Qobj(F.conj().T)   # F è reale, quindi F_dag = F.T
F_inv = F_dag.inv()            # Inversa hermitiana
sigma2 = F_inv * R * qt.Qobj(F)

# Monodromy operator per trefoil closure: M = σ₁ σ₂ σ₁
M = sigma1 * sigma2 * sigma1

print("=== Monodromy operator M (2x2) ===")
print(M)

print("\n=== Autovalori di M ===")
evals, evecs = M.eigenstates()
for i, ev in enumerate(evals):
    print(f"\u03BB_{i+1} = {ev:.8f}")

print("\n=== Fasi arg(\u03BB_k) in radianti ===")
phases = [np.angle(ev) for ev in evals]
for i, ph in enumerate(phases):
    print(f"arg(\u03BB_{i+1}) = {ph:.6f} rad  ({np.degrees(ph):.3f}°)")
    # Wrap in [-pi, pi]
    wrapped = ((ph + np.pi) % (2*np.pi)) - np.pi
    print(f"  → wrapped: {wrapped:.6f} rad")

# Generazione fasi wrapped teoriche 2π k / φ per k=1..50
print("\n=== Coordinate TikZ per fasi wrapped (k=1..50) ===")
print("% Formato: (k, wrapped_phase)")
print("coordinates {")
for k in range(1, 51):
    raw = 2 * np.pi * k / phi
    wrapped = ((raw + np.pi) % (2*np.pi)) - np.pi
    print(f"({k}, {wrapped:.6f})")
print("};")

print("\nNota: queste fasi wrapped mostrano periodicità ≈ φ ≈ 1.618")
print("Ogni ~1.618 passi k la fase avanza di ~2π (mod 2π).")

# Plot semplice delle fasi wrapped vs k (salva come PNG per Overleaf)
import matplotlib.pyplot as plt

k_values = np.arange(1, 51)
wrapped_phases = [((2*np.pi*k/phi + np.pi) % (2*np.pi)) - np.pi for k in k_values]

plt.figure(figsize=(10, 6))
plt.plot(k_values, wrapped_phases, 'o-', color='green', markersize=4, label='Fasi wrapped $2\pi k / \phi$')
plt.axhline(y=np.pi, color='gray', linestyle='--', alpha=0.5)
plt.axhline(y=-np.pi, color='gray', linestyle='--', alpha=0.5)
plt.xlabel('Indice braiding $k$')
plt.ylabel('Fase wrapped (rad)')
plt.title('Periodicit\u00E0 delle fasi nel limite many-body ($\\phi$-modulata)')
plt.grid(True, alpha=0.3)
plt.ylim(-np.pi-0.5, np.pi+0.5)
plt.legend()
plt.tight_layout()

# Create the 'code' directory if it doesn't exist
os.makedirs('code', exist_ok=True)
plt.savefig('code/monodromy_phases_wrapped.png', dpi=300, bbox_inches='tight')
print("\nPlot salvato come: code/monodromy_phases_wrapped.png")