# Title: Entanglement Measures nel Toy Model TET-CVTL
# Description: Calcola entanglement entropy von Neumann per sottosistemi bipartiti
# e concurrence per coppie di qubit adiacenti durante l'evoluzione con drive.
# Utile per verificare se il braiding eterno / torque extraction genera o preserva entanglement.
# Author: Grok 4 (xAI) - Generated for @PhysSoliman
# Date: March 02, 2026

import qutip as qt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

N = 4           # numero qubit
tlist = np.linspace(0, 10, 120)

# Operatori base
sigmax = qt.sigmax()
sigmaz = qt.sigmaz()

def tensor_op(op, pos, N):
    ops = [qt.qeye(2)] * N
    ops[pos] = op
    return qt.tensor(ops)

# Hamiltoniano (simile al base model)
H0 = sum(tensor_op(sigmaz, i, N) * tensor_op(sigmaz, i+1, N) for i in range(N-1))
H_drive = sum(tensor_op(sigmaz, i, N) * tensor_op(sigmax, i+1, N) for i in range(N-1))

def H_t(t, args):
    return H0 + args['lambda'] * np.sin(args['omega'] * t) * H_drive

args = {'lambda': 0.5, 'omega': 1.0}

# Initial state entangled (es. Bell-like su primi due + vacuum resto)
# Corrected Bell state for two qubits (|00> + |11>)/sqrt(2)
bell_2q = (qt.tensor(qt.basis(2,0), qt.basis(2,0)) + qt.tensor(qt.basis(2,1), qt.basis(2,1))).unit() / np.sqrt(2)
# Remaining N-2 qubits in |0> state
vacuum_rest = [qt.basis(2, 0) for _ in range(N-2)]
psi0 = qt.tensor(bell_2q, *vacuum_rest)

# Evoluzione
result = qt.mesolve(H_t, psi0, tlist, args=args)

# Entanglement entropy von Neumann per primo sottosistema di m qubit
m = 2  # bipartizione 2|N-2
entropy = []
for state in result.states:
    rho_A = state.ptrace(list(range(m)))   # reduced density matrix
    entropy.append(qt.entropy_vn(rho_A))

# Concurrence per coppia adiacente (es. qubit 0-1)
concurrence = []
for state in result.states:
    rho_01 = state.ptrace([0,1])
    conc = qt.concurrence(rho_01)
    concurrence.append(conc if conc is not None else 0.0)

print(f"Entanglement entropy finale (A = primi {m} qubit): {entropy[-1]:.4f}")
print(f"Concurrence finale (qubit 0-1): {concurrence[-1]:.4f}")

# Plot
fig, ax1 = plt.subplots(figsize=(10, 5))

ax1.plot(tlist, entropy, 'b-', label=f'Entanglement Entropy (A={m} qubit)')
ax1.set_xlabel('Time')
ax1.set_ylabel('Von Neumann Entropy', color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.grid(True, alpha=0.3)

ax2 = ax1.twinx()
ax2.plot(tlist, concurrence, 'r--', label='Concurrence (0-1)')
ax2.set_ylabel('Concurrence', color='r')
ax2.tick_params(axis='y', labelcolor='r')

fig.suptitle('Entanglement Dynamics durante Vacuum Torque Extraction')
fig.legend(loc='upper right')
plt.savefig('entanglement_measures.png')
plt.show()

# Salva dati
df = pd.DataFrame({
    'time': tlist,
    'entropy_A': entropy,
    'concurrence_01': concurrence
})
df.to_csv('entanglement_measures_data.csv', index=False)