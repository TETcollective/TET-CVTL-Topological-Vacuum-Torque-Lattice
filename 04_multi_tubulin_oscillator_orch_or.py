"""
04_multi_tubulin_oscillator_orch_or.py
Simulazione cluster di oscillatori tubulina con termini gravitazionali Diósi-Penrose
"""

from qutip import *
import numpy as np

N_tub = 5           # numero tubuline (scalabile)
omega = 2*np.pi*5e9 # frequenza oscillatore (GHz range)
g_dip = 0.05        # coupling dipole-dipolo
E_G = 1e-22         # energia gravitazionale per coppia (eV → ħ=1)
gamma = 0.01

a = [destroy(10) for _ in range(N_tub)]  # Hilbert space troncato a 10 livelli

H_osc = sum(omega * a[i].dag() * a[i] for i in range(N_tub))
H_dip = sum(g_dip * (a[i] + a[i].dag()) * (a[j] + a[j].dag())
            for i in range(N_tub) for j in range(i+1,N_tub))

# Termine gravitazionale semplificato (OR collapse)
H_grav = 0
for i in range(N_tub):
    for j in range(i+1, N_tub):
        H_grav += E_G * (a[i].dag()*a[i] - a[j].dag()*a[j])**2

H = H_osc + H_dip + H_grav

c_ops = [np.sqrt(gamma) * a[i] for i in range(N_tub)]

psi0 = tensor([coherent(10, 1.0) for _ in range(N_tub)])  # stato coerente iniziale

times = np.linspace(0, 50, 200)
result = mesolve(H, psi0, times, c_ops=c_ops,
                 e_ops=[a[0].dag()*a[0], entropy_vn(result.states[-1].ptrace(0))])

print("Tempo collasso stimato (OR):", 1 / (E_G * N_tub**2))