"""
02_advanced_braiding_nonadiabatic_fidelity.py
Braiding non-adiabatico + calcolo fedeltà logica topologica
con Lindblad e QobjEvo per fase modulata
"""

from qutip import *
import numpy as np
import matplotlib.pyplot as plt

N_qubits = 4  # numero anyon/qubit logici
braid_time = 80.0
omega = 2*np.pi / braid_time

# Operatori anyon semplificati (Fibonacci-like braiding)
R = Qobj([[np.exp(-1j*4*np.pi/5), 0], [0, np.exp(1j*2*np.pi/5)]])
phase_drive = QobjEvo([ [qeye(2**N_qubits), lambda t, args: np.exp(1j * args['omega'] * t)] ])

# Hamiltoniano base + drive
H_base = 0.1 * tensor([sigmaz() for _ in range(N_qubits)])
H = [H_base, [phase_drive, lambda t, args: 0.2 * np.sin(args['omega']*t)]]

# Stato iniziale entangled
psi0 = bell_state('00') if N_qubits == 2 else tensor([basis(2,0)]*N_qubits)

c_ops = [np.sqrt(0.01) * sigmam() for _ in range(N_qubits)]

times = np.linspace(0, braid_time, 600)

result = mesolve(H, psi0, times, c_ops=c_ops,
                 e_ops=[entropy_vn(psi0.ptrace(range(N_qubits//2)))])

# Stato target dopo braiding (es. fase non-Abeliana)
psi_target = R * psi0 if N_qubits == 2 else phasegate(np.pi/4) * psi0

fids = [fidelity(state, psi_target) for state in result.states]
print(f"Fedeltà logica finale: {fids[-1]:.5f}")

plt.plot(times, fids, label='Fedeltà logica')
plt.plot(times, result.expect[0], '--', label='Entropia von Neumann')
plt.xlabel('Tempo braiding')
plt.ylabel('Valore')
plt.title('Braiding non-adiabatico con fedeltà topologica')
plt.legend()
plt.grid(True)
plt.show()