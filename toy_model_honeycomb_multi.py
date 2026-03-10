# Title: Multi-Run Vacuum Torque Extraction Simulation in 2+1D Honeycomb Lattice Toy Model using QuTiP and NetworkX
# Description: Multi-run on honeycomb lattice (N=10 siti approx), with random init and phase for stats.
# Saves CSV. Adjust G for larger lattice if needed.
# Author: Grok 4 (xAI) - Generated for @PhysSoliman
# Date: March 02, 2026

import qutip as qt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx

G = nx.hexagonal_lattice_graph(2, 2)  # ~10 nodes approx
nodes = list(G.nodes)
N = len(nodes)
node_to_idx = {node: idx for idx, node in enumerate(nodes)}
num_runs = 10

# ... (adatta H0, H_drive su edges come precedente)

integrated_torques = []

for run in range(num_runs):
    np.random.seed(run)
    phase = np.random.uniform(0, 2*np.pi)
    args = {'lambda_': 0.5, 'omega': 1.0, 'phase': phase}
    psi0 = qt.tensor([qt.Qobj(np.random.rand(2,1) + 1j*np.random.rand(2,1)).unit() for _ in range(N)])

    # Evolve e compute

    integrated_torques.append(integrated)

mean_torque = np.mean(integrated_torques)
std_torque = np.std(integrated_torques)
print(f"Mean integrated torque (Honeycomb N={N}): {mean_torque:.4f} ± {std_torque:.4f}")

df = pd.DataFrame({'Run': range(num_runs), 'Integrated_Torque': integrated_torques})
df.to_csv('results_honeycomb_multi.csv', index=False)

# Plot
plt.savefig('torque_multi_honeycomb.png')

# Optional lattice plot
nx.draw(G, with_labels=True)
plt.savefig('honeycomb_lattice_multi.png')