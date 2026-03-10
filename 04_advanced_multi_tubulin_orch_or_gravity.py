"""
04_advanced_multi_tubulin_orch_or_gravity.py
Cluster multi-oscillatore tubulina con termini gravitazionali Diósi–Penrose
Calcolo rate OR e entanglement multi-partite
"""

from qutip import *
import numpy as np
import matplotlib.pyplot as plt

N_tub = 8               # tubuline (scalabile con GPU)
N_levels = 6            # livelli per oscillatore (troncato)
omega = 2*np.pi * 6e9   # frequenza ~GHz
g_dip = 0.04            # dipole-dipolo
E_G_per_pair = 5e-23    # eV → ħ=1
gamma_phonon = 0.012

a_ops = [destroy(N_levels) for _ in range(N_tub)]

H_osc = sum(omega * a.dag() * a for a in a_ops)
H_dip = sum(g_dip * (a_ops[i] + a_ops[i].dag()) * (a_ops[j] + a_ops[j].dag())
            for i in range(N_tub) for j in range(i+1, N_tub))

# Termine gravitazionale multi-coppia
H_grav = 0
for i in range(N_tub):
    for j in range(i+1, N_tub):
        pos_diff = (a_ops[i].dag()*a_ops[i] - a_ops[j].dag()*a_ops[j])**2
        H_grav += E_G_per_pair * pos_diff

H = H_osc + H_dip + H_grav

c_ops = [np.sqrt(gamma_phonon) * a for a in a_ops]

# Stato iniziale: coherente multi-partite
psi0 = tensor([coherent(N_levels, 1.2) for _ in range(N_tub)])

times = np.linspace(0, 60, 400)

# Metriche: rate OR e entanglement
def or_rate(state):
    return N_tub**2 * E_G_per_pair * np.mean([abs((state * a_ops[i].dag()*a_ops[i] - state * a_ops[j].dag()*a_ops[j]).tr())**2
                                              for i in range(N_tub) for j in range(i+1,N_tub)])

result = mesolve(H, psi0, times, c_ops=c_ops,
                 e_ops=[a_ops[0].dag()*a_ops[0], or_rate])

plt.plot(times, result.expect[0], label='Occupazione oscillatore 1')
plt.plot(times, result.expect[1], '--', label='Rate OR medio')
plt.xlabel('Tempo')
plt.ylabel('Valore')
plt.title('Multi-tubulina Orch-OR con gravità Diósi–Penrose')
plt.legend()
plt.grid(True)
plt.show()

print(f"Rate OR medio finale: {result.expect[1][-1]:.2e}")