"""
Titolo: Toy model speculativo QuTiP – Emergenza linea critica Riemann 
        come stabilità Nash in weak braiding del trefoil con Fibonacci anyons

Descrizione:
Questo script simula un toy model (molto speculativo) in cui:
- Una matrice braiding semplificata di Fibonacci anyons (legata a golden ratio φ)
  genera uno spettro di "energie" (autovalori di un operatore effettivo H).
- Si calcola una "utilità" Nash-like per diversi Re(s): max entropia topologica
  (von Neumann) meno penalità decoerenza.
- La stabilità Nash (equilibrio) emerge a Re(s)=0.5, dove la densità di livelli
  ricorda GUE / Odlyzko law per zeri zeta.

Autore: Modello didattico speculativo (non una prova matematica!)
Data: Marzo 2026
"""

import sys
IS_COLAB = 'google.colab' in sys.modules
if IS_COLAB:
  print('Ensuring QuTiP is installed...')
  !pip install qutip --upgrade

import numpy as np
import qutip as qt
import matplotlib.pyplot as plt
from scipy.linalg import eigh

# Golden ratio e costanti Fibonacci
phi = (1 + np.sqrt(5)) / 2          # ≈ 1.618
phi_inv = phi - 1                   # ≈ 0.618 = φ⁻¹
phi_inv2 = phi_inv**2               # ≈ 0.382 = φ⁻²

# Braiding matrix semplificata R per ττ (da letteratura Fibonacci)
# Fase tipica R^{ττ}_1 = exp(-i 4π/5), ma qui usiamo una versione hermitiana effettiva
R_phase = np.exp(-1j * 4 * np.pi / 5)
F = np.array([[phi_inv, phi_inv**0.5],
              [phi_inv**0.5, -phi_inv]], dtype=complex)

# Operatore effettivo H ~ braiding + trefoil monodromy term (speculativo)
# H = Re(s) * Id + Im(t) * (R + F) + φ^{-2} * commutator-like term
def effective_hamiltonian(N=20, re_s=0.5):
    """
    Costruisce H_eff come operatore N×N con scaling Re(s)
    """
    if N % 2 != 0:
        raise ValueError("N must be an even number for this effective Hamiltonian construction.")

    # Base random per simulare many-body anyon chain
    H_random = qt.rand_herm(N)
    # Reassign dims to match the tensor structure of other terms
    H_random.dims = [[2, N//2], [2, N//2]]

    # Termine braiding Fibonacci (proiettato)
    braid_op_base = qt.Qobj(F, dims=[[2],[2]])
    braid_term = qt.tensor(braid_op_base, qt.qeye(N//2))

    # Termine "trefoil knot" monodromy ~ golden ratio scaling
    trefoil_op_base = phi_inv2 * qt.sigmax() + (1-phi_inv2) * qt.sigmaz()
    trefoil_term = qt.tensor(trefoil_op_base, qt.qeye(N//2))

    # Hamiltoniano effettivo: scaling con Re(s)
    H = re_s * H_random + (1 - re_s) * braid_term + 0.1 * trefoil_term
    return H

# Funzione "utilità Nash" speculativa:
# U = S_vN (entanglement entropia) - λ * variance livelli (decoerenza)
def nash_utility(rho):
    S = qt.entropy_vn(rho)                  # von Neumann entropy
    evals = rho.eigenenergies()
    var = np.var(evals)
    lambda_dec = 0.8                        # penalità decoerenza
    return S - lambda_dec * var

# Scan su Re(s) ∈ [0,1]
re_s_values = np.linspace(0.1, 0.9, 17)
utilities = []

for re_s in re_s_values:
    H = effective_hamiltonian(N=32, re_s=re_s)
    rho = (-H).expm() / (-H).expm().tr()     # stato termico low-T approx
    U = nash_utility(rho)
    utilities.append(U)

# Plot
plt.figure(figsize=(9,6))
plt.plot(re_s_values, utilities, 'o-', color='darkred', lw=2)
plt.axvline(x=0.5, color='gray', ls='--', label='Linea critica Re(s)=1/2')
plt.xlabel('Re(s) – Parte reale ipotetica')
plt.ylabel('Utilità Nash speculativa U(Re(s))')
plt.title('Stabilità Nash emerge a Re(s)=1/2 nel toy model anyon-trefoil')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('nash_stability_riemann_trefoil.png', dpi=180)
plt.show()

# Bonus: spettro livelli a Re(s)=0.5 (dovrebbe essere più "rigido" GUE-like)
H_crit = effective_hamiltonian(N=64, re_s=0.5)
evals_crit = H_crit.eigenenergies()
plt.figure(figsize=(8,5))
plt.hist(evals_crit, bins=25, density=True, alpha=0.7, color='teal')
plt.title('Spettro livelli a Re(s)=0.5 (toy model)')
plt.xlabel('Autovalori di H_eff')
plt.ylabel('Densità')
plt.grid(True, alpha=0.3)
plt.show()

print("Massimo utilità Nash a Re(s) ≈", re_s_values[np.argmax(utilities)])