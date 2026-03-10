# Title: Sweep su rate Lindblad in Floquet open-system per TET–CVTL
# Description: Confronta torque extraction sotto Floquet drive per diversi gamma.
# Mostra robustezza topologica contro decoerenza crescente.
# Author: Grok 4 (xAI) - Generated for @PhysSoliman
# Date: March 02, 2026

import qutip as qt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

N = config['N']
T = 2 * np.pi
omega = config['drive_frequency']
lambda_ = config['drive_amplitude']
num_periods = config['periods']
tlist = np.linspace(0, num_periods * T, num_periods * config['time_points_per_period'])

sigmax = qt.sigmax()
sigmaz = qt.sigmaz()
sigmam = qt.sigmam()

def tensor_op(op, pos, N):
    ops = [qt.qeye(2)] * N
    ops[pos] = op
    return qt.tensor(ops)

H0 = sum(tensor_op(sigmaz, i, N) * tensor_op(sigmaz, i+1, N) for i in range(N-1))
H1 = sum(tensor_op(sigmaz, i, N) * tensor_op(sigmax, i+1, N) for i in range(N-1))

def H_t(t, args):
    return H0 + args['lambda'] * np.cos(args['omega'] * t) * H1

L = sum(tensor_op(sigmax, i, N) for i in range(N))

psi0 = qt.tensor([qt.basis(2, 0) for _ in range(N)])  # ground-like

gammas = [0.0, 0.001, 0.01, 0.1]
colors = ['k', 'b', 'g', 'r']

plt.figure(figsize=(12, 7))

for gamma, col in zip(gammas, colors):
    c_ops = [np.sqrt(gamma) * tensor_op(sigmam, i, N) for i in range(N)] if gamma > 0 else []
    rho0 = psi0 * psi0.dag()
    result = qt.mesolve(H_t, rho0, tlist, c_ops=c_ops, args={'lambda': lambda_, 'omega': omega})

    torque = []
    for idx, t in enumerate(tlist):
        rho = result.states[idx]
        H_now = H_t(t, {'lambda': lambda_, 'omega': omega})
        comm = qt.commutator(H_now, L)
        torque.append(np.imag(qt.expect(comm, rho)))

    integrated = np.trapezoid(torque, tlist)
    print(f"Gamma={gamma}: Integrated torque = {integrated:.4f}")

    plt.plot(tlist / T, torque, color=col, label=f'γ={gamma} (int={integrated:.3f})')

plt.xlabel('Periodi Floquet')
plt.ylabel('Torque istantaneo')
plt.title('Robustezza Torque vs Decoerenza (Floquet + Lindblad sweep)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('floquet_lindblad_gamma_sweep.png', dpi=300, bbox_inches='tight')
plt.show()