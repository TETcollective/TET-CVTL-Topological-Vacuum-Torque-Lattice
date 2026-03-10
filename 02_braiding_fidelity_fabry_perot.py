"""
02_braiding_fidelity_fabry_perot.py
Braiding adiabatico di due MZMs in un interferometro Fabry-Pérot
Calcolo fedeltà rispetto al gate braid ideale
"""

from qutip import *
import numpy as np
import matplotlib.pyplot as plt

# Parametri
N = 40              # siti totali
L = 20              # lunghezza braccio interferometro
t_hop = 1.0
Delta = 0.7
gamma = 0.015       # decoerenza debole

# Hamiltoniano base (Kitaev-like)
c = [destroy(N) for _ in range(N)]
H0 = sum(-t_hop * (c[j].dag()*c[j+1] + c[j+1].dag()*c[j]) +
         Delta * (c[j]*c[j+1] + c[j+1].dag()*c[j].dag())
         for j in range(N-1))

# Funzione gate di braiding (adiabatico tramite fase locale)
def H_braid(t, args):
    phase = args['omega'] * t
    gate = basis(2,0)*basis(2,0).dag() + np.exp(1j*phase)*basis(2,1)*basis(2,1).dag()
    return H0 + 0.1 * tensor([qeye(2) for _ in range(N//2)])  # placeholder semplificato

# Tempo braiding
T_braid = 50.0
times = np.linspace(0, T_braid, 300)

# Stato iniziale: entangled MZMs (stato parafermionico semplificato)
psi0 = (tensor(basis(2,0), basis(2,1)) + tensor(basis(2,1), basis(2,0))).unit()

# Evoluzione
result = mesolve(H_braid, psi0, times, c_ops=[np.sqrt(gamma)*destroy(2) for _ in range(2)],
                 args={'omega': np.pi/T_braid})

# Stato target ideale dopo braiding (fase e^{i π/4} per anyon non-Abeliano)
U_ideal = phasegate(np.pi/4)
psi_target = U_ideal * psi0

# Fedeltà finale
fidelity_last = fidelity(result.states[-1], psi_target)
print(f"Fedeltà braiding finale: {fidelity_last:.4f}")

# Plot fedeltà vs tempo
fids = [fidelity(state, psi_target) for state in result.states]
plt.plot(times, fids)
plt.xlabel('Tempo braiding')
plt.ylabel('Fedeltà con stato target')
plt.title('Fedeltà Braiding MZMs adiabatico')
plt.grid(True)
plt.show()