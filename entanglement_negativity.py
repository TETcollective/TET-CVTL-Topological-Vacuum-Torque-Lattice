# Title: Entanglement Negativity nel Toy Model TET-CVTL

#entanglement_negativity.py

# Description: Calcola l'entanglement negativity per sottosistemi bipartiti (es. A|B con |A|=2 qubit)
# durante l'evoluzione dinamica con drive. Negativity >0 indica entanglement distillabile.
# Utile per verificare robustezza topologica / eternal anyon contro decoerenza o drive.
# Usa QuTiP negativity() o implementazione manuale se necessario.
# Author: Grok 4 (xAI) - Generated for @PhysSoliman
# Date: March 02, 2026

import qutip as qt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

N = 4           # numero totale qubit
m_A = 2         # dimensione sottosistema A (primi m_A qubit)

tlist = np.linspace(0, 10, 120)

# Operatori base
sigmax = qt.sigmax()
sigmaz = qt.sigmaz()

def tensor_op(op, pos, N):
    ops = [qt.qeye(2)] * N
    ops[pos] = op
    return qt.tensor(ops)

# Hamiltoniano base (proxy string tension + drive braiding)
H0 = sum(tensor_op(sigmaz, i, N) * tensor_op(sigmaz, i+1, N) for i in range(N-1))
H_drive = sum(tensor_op(sigmaz, i, N) * tensor_op(sigmax, i+1, N) for i in range(N-1))

def H_t(t, args):
    return H0 + args['lambda'] * np.sin(args['omega'] * t) * H_drive

args = {'lambda': 0.5, 'omega': 1.0}

# Initial state: entangled su A (es. stato Bell-like su primi due qubit) + vacuum su resto
# Corrected Bell state for two qubits (|00> + |11>)/sqrt(2)
bell_2q = (qt.tensor(qt.basis(2,0), qt.basis(2,0)) + qt.tensor(qt.basis(2,1), qt.basis(2,1))).unit() # Removed extra division by np.sqrt(2)
# Remaining N-m_A qubits in |0> state
vacuum_rest = [qt.basis(2, 0) for _ in range(N - m_A)]
psi0 = qt.tensor(bell_2q, *vacuum_rest)

# Evoluzione temporale
result = qt.mesolve(H_t, psi0, tlist, args=args)

# Calcolo Negativity per ogni istante
negativity_values = []

for state in result.states:
    # Reduced density matrix su sottosistema A (primi m_A qubit)
    rho_A = state.ptrace(list(range(m_A)))

    # Entanglement negativity: QuTiP ha qt.negativity(rho, subsys=...)
    # Ma per partial transpose su A|B, usiamo qt.negativity(rho totale, subsys=A)
    neg = qt.negativity(state, subsys=list(range(m_A)))
    negativity_values.append(neg)

# Valore finale
print(f"Entanglement Negativity finale (A = primi {m_A} qubit): {negativity_values[-1]:.4f}")
print(f"Massimo negativity osservato: {max(negativity_values):.4f}")

# Plot
plt.figure(figsize=(10, 5))
plt.plot(tlist, negativity_values, 'm-', linewidth=2, label=f'Negativity (A={m_A} | B={N-m_A})')
plt.axhline(0, color='gray', linestyle='--', alpha=0.5)
plt.xlabel('Time')
plt.ylabel('Entanglement Negativity')
plt.title('Entanglement Negativity Dynamics in TET-CVTL Toy Model')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('entanglement_negativity.png')
plt.show()

# Salva dati per paper / analisi
df = pd.DataFrame({
    'time': tlist,
    'negativity': negativity_values
})
df.to_csv('entanglement_negativity_data.csv', index=False)