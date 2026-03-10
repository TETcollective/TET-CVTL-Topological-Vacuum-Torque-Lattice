# Title: Vacuum Torque Extraction Simulation in 2+1D Honeycomb Lattice Toy Model using QuTiP and NetworkX
#toy_model_honeycomb.py
# Description: Uses NetworkX to generate a real small honeycomb (hexagonal) lattice graph (7 sites: central hex + center).
# Maps nodes to qubits, edges to interactions. Approximates string-net for TET-CVTL.
# Author: Grok 4 (xAI) - Generated for @PhysSoliman
# Date: March 02, 2026

import qutip as qt
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# Generate small honeycomb lattice (nx.hexagonal_lattice_graph(rows, cols))
G = nx.hexagonal_lattice_graph(1, 2)  # Small graph ~7 nodes (adjust for size)
nodes = list(G.nodes)
N = len(nodes)  # e.g., 7 qubits

# Map nodes to indices (e.g., (0,0):0, (0,1):1, etc.)
node_to_idx = {node: idx for idx, node in enumerate(nodes)}

# Basis operators
sigmax = qt.sigmax()
sigmaz = qt.sigmaz()

# Tensor product helper
def tensor_op(op, i, N):
    ops = [qt.qeye(2)] * N
    ops[i] = op
    return qt.tensor(ops)

# Full identity
identity = qt.tensor([qt.qeye(2)] * N)

# Ground Hamiltonian H0: sum ZZ over edges
H0 = 0 * identity
for u, v in G.edges:
    i = node_to_idx[u]
    j = node_to_idx[v]
    H0 += tensor_op(sigmaz, i, N) * tensor_op(sigmaz, j, N)

# Drive Hamiltonian: sum ZX over edges
H_drive = 0 * identity
for u, v in G.edges:
    i = node_to_idx[u]
    j = node_to_idx[v]
    H_drive += tensor_op(sigmaz, i, N) * tensor_op(sigmax, j, N)

# Drive function
def drive_func(t, args):
    return args['lambda_'] * np.sin(args['omega'] * t)

# Full H
H = [H0, [H_drive, drive_func]]

# Angular momentum L: total Sx
L = 0 * identity
for i in range(N):
    L += tensor_op(sigmax, i, N)

# Initial state: |000...>
psi0 = qt.tensor([qt.basis(2, 0) for _ in range(N)])

# Parameters
tlist = np.linspace(0, 10, 100)
lambda_ = 0.5
omega = 1.0
args = {'lambda_': lambda_, 'omega': omega}

# Evolve
result = qt.mesolve(H, psi0, tlist, args=args)

# Compute torque
torque = []
for idx, t in enumerate(tlist):
    state = result.states[idx]
    Ht = H0 + drive_func(t, args) * H_drive
    comm = qt.commutator(Ht, L)
    expect = state.overlap(comm * state)
    torque.append(np.imag(expect))

# Integrated torque
integrated_torque = np.trapezoid(torque, tlist)
print(f"Integrated torque over time (Honeycomb, N={N}): {integrated_torque}")

# Plot
plt.figure()
plt.plot(tlist, torque)
plt.xlabel('Time')
plt.ylabel('Instantaneous Torque Im <[H,L]>')
plt.title('Vacuum Torque Extraction in TET-CVTL Honeycomb Model')
plt.savefig('torque_plot_honeycomb.png')
plt.show()

# Optional: Plot lattice for reference
nx.draw(G, with_labels=True)
plt.savefig('honeycomb_lattice.png')