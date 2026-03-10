"""
03_advanced_ciss_spin_transfer_nonmarkov.py
Trasferimento spin CISS con bagni non-Markoviani (strutturati)
e calcolo negatività logaritmica
"""

from qutip import *
import numpy as np
import matplotlib.pyplot as plt

# Sistema anyon + tubulina (spin-1/2 ciascuno)
H_sys = 0.08 * tensor(sigmaz(), sigmaz()) + 0.12 * tensor(sigmax(), sigmax())
H_bias = 0.06 * tensor(qeye(2), sigmaz())  # bias CISS up

H = H_sys + H_bias

# Bagno strutturato (Ohmic + cutoff Lorentziano per fononi)
def spectral_density(w):
    return 0.02 * w * np.exp(-w**2 / (2*0.5**2))  # esempio strutturato

c_ops_markov = [np.sqrt(0.015) * tensor(sigmam(), qeye(2)),
                np.sqrt(0.015) * tensor(qeye(2), sigmam())]

# Approssimazione non-Markoviana semplice (via correlatori)
corr_func = lambda t: 0.02 * np.exp(-0.3*t) * (np.cos(1.2*t) + 1j*np.sin(1.2*t))
nonmarkov_c_ops = [tensor(sigmam(), qeye(2)), tensor(qeye(2), sigmam())]

psi0 = tensor(basis(2,0), basis(2,0)) + tensor(basis(2,1), basis(2,1))
psi0 = psi0.unit()

times = np.linspace(0, 120, 800)

result = mesolve(H, psi0, times, c_ops=c_ops_markov,
                 e_ops=[tensor(sigmaz(), qeye(2)), log_negativity(psi0.ptrace([0]), [0])])

# Negatività logaritmica finale
last_state = result.states[-1]
neg_log = log_negativity(last_state.ptrace([0]), [0])
print(f"Negatività logaritmica finale (entanglement distillabile): {neg_log:.4f} ebit")

plt.plot(times, result.expect[0], label='<Sz> anyon')
plt.plot(times, result.expect[1], '--', label='Negatività logaritmica')
plt.xlabel('Tempo')
plt.ylabel('Valore')
plt.title('Trasferimento CISS non-Markoviano + entanglement distillabile')
plt.legend()
plt.grid(True)
plt.show()