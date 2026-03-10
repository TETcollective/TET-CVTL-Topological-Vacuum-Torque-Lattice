# Title: Suite completa misure di entanglement in TET–CVTL
# Description: Calcola simultaneamente von Neumann entropy, negativity e concurrence
# su sottosistemi bipartiti durante evoluzione dinamica (drive Floquet-like).
# Output: plot multi-as se + CSV unico per paper.
# Author: Grok 4 (xAI) - Generated for @PhysSoliman / TETcollective
# Date: March 02, 2026

import qutip as qt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yaml

# Carica config
with open('config.yaml', 'r') as f:  # adatta path se necessario
    config = yaml.safe_load(f)

N = config['N']
m_A = config['bipartition_A_size']
tlist = np.linspace(0, 10, 120)

sigmax = qt.sigmax()
sigmaz = qt.sigmaz()

def tensor_op(op, pos, N):
    ops = [qt.qeye(2)] * N
    ops[pos] = op
    return qt.tensor(ops)

H0 = sum(tensor_op(sigmaz, i, N) * tensor_op(sigmaz, i+1, N) for i in range(N-1))
H_drive = sum(tensor_op(sigmaz, i, N) * tensor_op(sigmax, i+1, N) for i in range(N-1))

def H_t(t, args):
    return H0 + args['lambda'] * np.sin(args['omega'] * t) * H_drive

args = {'lambda': config['drive_amplitude'], 'omega': config['drive_frequency']}

# Stato iniziale entangled (Bell su primi 2 + vacuum)
bell_2q = (qt.tensor(qt.basis(2, 0), qt.basis(2, 0)) + qt.tensor(qt.basis(2, 1), qt.basis(2, 1))).unit()
psi0 = qt.tensor(bell_2q, *[qt.basis(2, 0) for _ in range(N-2)])

result = qt.mesolve(H_t, psi0, tlist, args=args)

entropy = []
negativity = []
concurrence = []

for state in result.states:
    rho_A = state.ptrace(list(range(m_A)))
    entropy.append(qt.entropy_vn(rho_A))

    neg = qt.negativity(state, subsys=list(range(m_A)))
    negativity.append(neg)

    rho_01 = state.ptrace([0,1])
    conc = qt.concurrence(rho_01) if qt.concurrence(rho_01) is not None else 0.0
    concurrence.append(conc)

print(f"Final entropy (A={m_A}): {entropy[-1]:.4f}")
print(f"Final negativity: {negativity[-1]:.4f}")
print(f"Final concurrence (0-1): {concurrence[-1]:.4f}")

fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.plot(tlist, entropy, 'b-', label=f'Entropy (A={m_A})')
ax1.set_xlabel('Time')
ax1.set_ylabel('Von Neumann Entropy', color='b')
ax1.tick_params(axis='y', labelcolor='b')

ax2 = ax1.twinx()
ax2.plot(tlist, negativity, 'm--', label='Negativity')
ax2.plot(tlist, concurrence, 'r-.', label='Concurrence (0-1)')
ax2.set_ylabel('Negativity / Concurrence', color='m')
ax2.tick_params(axis='y', labelcolor='m')

fig.suptitle('Entanglement Measures Suite - TET–CVTL')
fig.legend(loc='upper right', bbox_to_anchor=(0.95, 0.95))
plt.grid(True, alpha=0.3)
plt.savefig('entanglement_suite.png', dpi=300, bbox_inches='tight')
plt.show()

pd.DataFrame({
    'time': tlist,
    'entropy': entropy,
    'negativity': negativity,
    'concurrence_01': concurrence
}).to_csv('entanglement_suite_data.csv', index=False)
