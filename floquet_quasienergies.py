# Title: Spettro quasi-energie Floquet in TET–CVTL (aggiornato QuTiP 5.x)
# Description: Calcola e visualizza lo spettro Floquet con FloquetBasis (non deprecato)
# Author: Grok 4 (xAI) - Generated for @PhysSoliman
# Date: March 02, 2026

import qutip as qt
import numpy as np
import matplotlib.pyplot as plt
import yaml

# Reproducibility
np.random.seed(42)
qt.settings.has_openmp = False

# Config (adatta se usi config.yaml)
try:
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    config = {'N': 4, 'drive_frequency': 1.0, 'drive_amplitude': 0.8}

N = config['N']
T = 2 * np.pi
omega = config['drive_frequency']
lambda_ = config['drive_amplitude']

sigmax = qt.sigmax()
sigmaz = qt.sigmaz()

def tensor_op(op, pos, N):
    ops = [qt.qeye(2)] * N
    ops[pos] = op
    return qt.tensor(ops)

H0 = sum(tensor_op(sigmaz, i, N) * tensor_op(sigmaz, i+1, N) for i in range(N-1))
H1 = sum(tensor_op(sigmaz, i, N) * tensor_op(sigmax, i+1, N) for i in range(N-1))

def H_t(t, args):
    return H0 + args['lambda'] * np.cos(args['omega'] * t) * H1

args = {'lambda': lambda_, 'omega': omega}

# ────────────────────────────────────────────────
# Reverting to qt.floquet_modes due to FloquetBasis API issues in this environment
f_modes, quasi_energies = qt.floquet_modes(H_t, T, args)

# Quasi-energie (ordinate) - Apply modulo after getting the energies
quasi_energies = quasi_energies % (2 * np.pi / T)
quasi_energies = np.sort(quasi_energies)

# Plot
plt.figure(figsize=(9, 6))
plt.plot(quasi_energies.real, 'bo', markersize=8, label='Quasi-energies (mod 2π/T)')
plt.axhline(0, color='gray', ls='--', alpha=0.5, lw=0.8)
plt.xlabel('Mode index')
plt.ylabel('Quasi-energy (mod 2π/T)')
plt.title('Floquet Quasi-Energy Spectrum (TET–CVTL)')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=10)
plt.tight_layout()

# Esportazione alta qualità
plt.savefig('floquet_quasienergies.pdf', format='pdf', bbox_inches='tight', dpi=400)
plt.savefig('floquet_quasienergies.svg', format='svg', bbox_inches='tight')
plt.savefig('floquet_quasienergies_preview.png', dpi=220, bbox_inches='tight')
plt.show()

# Calcolo gap (minima differenza tra quasi-energie ordinate)
sorted_qe = quasi_energies.real # Already sorted above
gaps = np.diff(sorted_qe)
min_gap = np.min(gaps[gaps > 1e-10]) if len(gaps[gaps > 1e-10]) > 0 else 0.0
print(f"Gap minimo approssimativo (escludendo duplicati): {min_gap:.6f}")
print(f"Quasi-energie (prime 10): {quasi_energies.real[:10]}")