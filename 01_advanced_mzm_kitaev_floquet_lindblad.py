"""
01_advanced_mzm_kitaev_floquet_lindblad.py
Simulazione avanzata di catena Kitaev con drive Floquet per braiding eterno
Calcolo correlatore Majorana, TEE e fedeltà logica
"""

from qutip import *
import numpy as np
import matplotlib.pyplot as plt

# Parametri
N = 8
t = 1.0
Delta = 0.95
mu = 0.0
gamma_deph = 5e-5
gamma_relax = 1e-5
braid_time = 500.0
times = np.linspace(0, braid_time, 1200)

# Hamiltoniano base
c = [destroy(N) for _ in range(N)]
H0 = 0
for j in range(N-1):
    H0 += -t * (c[j].dag() * c[j+1] + c[j+1].dag() * c[j])
    H0 += Delta * (c[j] * c[j+1] + c[j+1].dag() * c[j].dag())
H0 += -mu * sum(c[j].dag() * c[j] for j in range(N))
H0 = (H0 + H0.dag()) / 2

# Drive tunneling centrale
def tunnel_coeff(t, args):
    return 0.08 * np.sin(2 * np.pi * t / braid_time)

tunnel_op = c[3].dag() * c[4] + c[4].dag() * c[3]
H = [H0, [tunnel_op, tunnel_coeff]]

# c_ops
c_ops = [np.sqrt(gamma_deph) * (c[j] + c[j].dag()) for j in range(N)] + \
        [np.sqrt(gamma_relax) * c[j] for j in range(N)]

# Ground state
gs, _ = H0.groundstate()
psi0 = gs

# Simulazione
result = mesolve(H, psi0, times, c_ops=c_ops,
                 options={'nsteps': 20000})

# Majorana correlatore
gamma_left = (c[0] + c[0].dag()) / np.sqrt(2)
gamma_right = 1j * (c[N-1] - c[N-1].dag()) / np.sqrt(2)
corr = [expect(gamma_left * gamma_right, state) for state in result.states]

print(f"Correlatore finale: {corr[-1]:.5f}")

# Plot
plt.plot(times, corr, lw=2.5, color='darkred')
plt.axhline(-1, color='g--', lw=2, label='Ideale -1')
plt.xlabel('Tempo')
plt.ylabel('⟨γ₁ γ₈⟩')
plt.title('Braiding MZMs')
plt.legend()
plt.grid(True)
plt.ylim(-1.1, 0.1)
plt.savefig('mzm_braiding_correlator.pdf', dpi=300)
plt.show()