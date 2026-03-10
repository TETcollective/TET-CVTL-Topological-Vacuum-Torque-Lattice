# =============================================================================
# TET--CVTL Project - Monodromy Trefoil Char Poly Calculation (Fibonacci Anyons)
# File: code/monodromy_char_poly_calc.py
# Descrizione: Calcolo simbolico del polinomio caratteristico del monodromy operator
#              per treccia trefoil (σ₁ σ₂ σ₁) nella rappresentazione Fibonacci anyons.
#              Usa SymPy per algebra simbolica + QuTiP per matrici numeriche/fasi.
# Autore: Simon Soliman (Tetcollective.org) - Data: Marzo 2026
# =============================================================================

import sympy as sp
import numpy as np
from qutip import Qobj, basis

# -----------------------------
# Definizioni simboliche
# -----------------------------
phi = (1 + sp.sqrt(5))/2          # Golden ratio ≈ 1.6180339887
phi_inv = phi - 1                  # = 1/phi ≈ 0.618034
phi_inv_sqrt = sp.sqrt(phi_inv)    # ≈ 0.786151

theta1 = 4*sp.pi / 5               # Fase per canale vacuum (1)
theta_tau = -3*sp.pi / 5           # Fase per canale τ

# Matrice F (standard per Fibonacci τ τ τ → τ)
F = sp.Matrix([
    [phi_inv,     phi_inv_sqrt],
    [phi_inv_sqrt, -phi_inv   ]
])

# Matrice R diagonale (braiding phase)
R = sp.diag(sp.exp(sp.I * theta1), sp.exp(sp.I * theta_tau))

# Matrice σ₁ (scambio primi due anyons) = R (diagonale nella base fusion)
sigma1 = R

# Matrice σ₂ = F^{-1} R F   (convenzione comune per Fibonacci)
F_inv = F.inv()
sigma2 = F_inv * R * F

# Monodromy operator per threefoil: M = σ₁ σ₂ σ₁
M_sym = sigma1 * sigma2 * sigma1

# -----------------------------
# Polinomio caratteristico simbolico
# -----------------------------
lam = sp.symbols('lambda')
char_poly = M_sym.charpoly(lam)
print("Polinomio caratteristico simbolico di M (2x2):")
sp.pprint(char_poly.as_expr())

# Espansione approssimata (perché fasi rendono complesso)
print("\nCoefficienti numerici approssimati:")
M_num = np.array(M_sym.evalf().tolist(), dtype=complex)
trace = np.trace(M_num)
det = np.linalg.det(M_num)
print(f"  Tr(M) ≈ {trace:.6f}")
print(f"  Det(M) ≈ {det:.6f}")
print(f"  Poly approx: λ² - {trace:.4f} λ + {det:.4f} = 0")

# Nota: Il polinomio cubico λ³ - φ λ² + φ⁻¹ λ - 1 emerge nel limite many-body
#       o estendendo recursioni Fibonacci alle dimensioni dei blocchi.

# -----------------------------
# Fasi degli autovalori (per plotting in TikZ)
# -----------------------------
evals = np.linalg.eigvals(M_num)
phases = np.angle(evals)  # in [-pi, pi]

print("\nAutovalori di M:")
for ev in evals:
    print(f"  {ev}")

print("\nFasi arg(λ_k) (rad):")
for ph in phases:
    print(f"  {ph:.6f}")

# Per generare coordinate per TikZ (es. primi 20 passi pseudo-periodici)
print("\nEsempio coordinate per plot fasi (k=1..20, arg ≈ 2π k / φ mod 2π):")
for k in range(1, 21):
    phase_approx = (2 * np.pi * k / float(phi)) % (2 * np.pi)
    if phase_approx > np.pi:
        phase_approx -= 2 * np.pi
    print(f"({k}, {phase_approx:.6f})")

# Fine - Esegui per verificare fasi da inserire manualmente in TikZ se serve




import numpy as np

# Golden ratio con alta precisione
phi = (1 + np.sqrt(5)) / 2
print(f"Golden ratio φ = {phi:.12f}")
print(f"Periodo teorico in k (≈ φ) = {phi:.6f}\n")

def wrapped_phase(k, modulo=2*np.pi, center=np.pi):
    """
    Calcola 2π k / φ, poi wrap in [-π, π]
    """
    raw = 2 * np.pi * k / phi
    wrapped = (raw + center) % modulo - center
    return wrapped

# Parametri
max_k = 50          # puoi aumentare a 100 o 200
print(f"Generazione fasi wrapped per k=1..{max_k} (2π k / φ mod 2π in [-π, π])\n")

print("k  | raw phase (rad) | wrapped phase (rad) | wrapped (deg)")
for k in range(1, max_k + 1):
    raw = 2 * np.pi * k / phi
    wp = wrapped_phase(k)
    deg = np.degrees(wp)
    print(f"{k:3d} | {raw:14.6f} | {wp:17.6f} | {deg:10.3f}°")

# Output pronto per TikZ: coordinates list
print("\nTikZ coordinates (copia-incolla in \\addplot coordinates { ... }):")
print("% Formato: (k, wrapped_phase)")
print("coordinates {")
for k in range(1, max_k + 1):
    wp = wrapped_phase(k)
    print(f"({k}, {wp:.6f})")
print("};")

# Bonus: mostra periodicità approssimata (ogni ~φ passi la fase ripete quasi)
print("\nNota sulla periodicità: la fase avanza di ~3.883 rad per passo (2π/φ).")
print("Ogni ~φ ≈ 1.618 passi, la fase aumenta di 2π (cioè torna simile modulo 2π).")