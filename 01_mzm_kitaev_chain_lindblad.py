"""
01_mzm_kitaev_chain_lindblad.py
Simulazione QuTiP di catena Kitaev con Majorana zero modes (MZMs)
Dinamica open-system con Lindblad master equation
Obiettivo: verificare persistenza MZMs e decoerenza termica
Autore: ispirato a TET-CVTL framework (2026)
"""

import numpy as np
from qutip import *

# Parametri fisici (unità: ħ = 1)
N = 20              # numero siti (deve essere pari)
t = 1.0             # hopping normale
Delta = 0.8         # pairing superconduttivo
mu = 0.0            # potenziale chimico (regime topologico per |mu| < 2t)
gamma_deph = 0.02   # rate dephasing (fononi, quasi-particelle)
gamma_relax = 0.01  # rate rilassamento

# Operatori Majorana (per sito j)
def majorana(c, j):
    return (c[2*j] + c[2*j].dag()) / np.sqrt(2), \
           1j * (c[2*j] - c[2*j].dag()) / np.sqrt(2)

# Costruzione Hamiltoniano Kitaev
c = [destroy(N) for _ in range(N)]  # fermioni (non Majorana basis)
H = 0
for j in range(N-1):
    H += -t * (c[j].dag() * c[j+1] + c[j+1].dag() * c[j])
    H += Delta * (c[j] * c[j+1] + c[j+1].dag() * c[j].dag())
H += -mu * sum(c[j].dag() * c[j] for j in range(N))

H = (H + H.dag()) / 2  # hermitiano

# Stati iniziali: ground state approssimato (vuoto per semplicità)
psi0 = tensor([basis(2,0) for _ in range(N)])   # tutti vuoti

# Collassi Lindblad
c_ops = []
# Dephasing su tutti i siti
for j in range(N):
    c_ops.append(np.sqrt(gamma_deph) * c[j].dag() * c[j])
# Rilassamento (perdita particelle)
for j in range(N):
    c_ops.append(np.sqrt(gamma_relax) * c[j])

# Tempo simulazione
times = np.linspace(0, 100, 500)

# Evoluzione master equation
result = mesolve(H, psi0, times, c_ops=c_ops,
                 e_ops=[c[0].dag()*c[0], c[N-1].dag()*c[N-1]])  # occupazione bordi

# Plot occupazione MZMs ai bordi (dovrebbe rimanere ~0.5 se protetti)
import matplotlib.pyplot as plt
plt.plot(times, result.expect[0], label='Left edge <n>')
plt.plot(times, result.expect[1], label='Right edge <n>')
plt.xlabel('Time (1/Δ)')
plt.ylabel('Occupation')
plt.title('MZMs Occupation under Decoherence')
plt.legend()
plt.grid(True)
plt.show()

print("Simulazione completata. Fedeltà MZMs persistente:", result.expect[0][-1])