"""
Calcolo Topological Entanglement Entropy (TEE) in toy chain Fibonacci anyons
Usa formula standard TEE = c/6 log(ℓ/ℓ₀) + costanti + termini retrocausali

Autore: Simon Soliman (tetcollective.org)
Data: Marzo 2026
"""

import numpy as np
import matplotlib.pyplot as plt

# Parametri
c = 7/10                        # central charge tricritical Ising / Fibonacci
phi = (1 + np.sqrt(5)) / 2
beta = phi**(-2)                # ≈ 0.381966

ell = np.logspace(0.5, 2.5, 150)  # più punti per curva liscia
ell0 = 1.0

# TEE base
tee_base = (c / 6) * np.log(ell / ell0)

# Termine retrocausale: oscillazione con ampiezza ridotta + offset positivo
amp = 0.15                      # ampiezza controllata
tee_retro = beta * (amp * np.sin(2 * np.pi * ell / 8) + 0.1)  # + offset per TEE > 0

tee_total = tee_base + tee_retro

plt.figure(figsize=(9, 6))
plt.loglog(ell, tee_base, 'k--', lw=2.2, label='TEE standard ($c=7/10$)')
plt.loglog(ell, tee_total, 'b-', lw=2.5, label='TEE + retrocausal kicks')
plt.xlabel(r'Lunghezza di correlazione embodied $\ell$')
plt.ylabel(r'Topological Entanglement Entropy')
plt.title(r'Incremento TEE da retrocausalità debole (RENASCENT-Q)')
plt.legend(loc='upper left')
plt.grid(True, which="both", ls="--", alpha=0.4)
plt.tight_layout()
plt.savefig('code/tee_retrocausal.png', dpi=300, bbox_inches='tight')
plt.show()