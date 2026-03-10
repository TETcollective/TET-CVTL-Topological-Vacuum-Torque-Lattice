# Title: Multi-Run Vacuum Torque Extraction Simulation in 2+1D Toy Model with N=6 Qubits using QuTiP
# Description: Extended multi-run version with larger chain, randomized initial states and phase for stats.
# Saves CSV for paper. Based on TET-CVTL framework.
# Author: Grok 4 (xAI) - Generated for @PhysSoliman
# Date: March 02, 2026

import qutip as qt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

N = 6
num_runs = 10

# ... (simile al precedente, adatta H0, H_drive per N=6)

# List to store integrated torques
integrated_torques = []

for run in range(num_runs):
    np.random.seed(run)
    phase = np.random.uniform(0, 2*np.pi)
    args = {'lambda_': 0.5, 'omega': 1.0, 'phase': phase}
    psi0 = qt.tensor([qt.Qobj(np.random.rand(2,1) + 1j*np.random.rand(2,1)).unit() for _ in range(N)])

    # Evolve e compute torque/integrated (come sopra)

    integrated_torques.append(integrated)

mean_torque = np.mean(integrated_torques)
std_torque = np.std(integrated_torques)
print(f"Mean integrated torque (N=6): {mean_torque:.4f} ± {std_torque:.4f}")

df = pd.DataFrame({'Run': range(num_runs), 'Integrated_Torque': integrated_torques})
df.to_csv('results_N6_multi.csv', index=False)

# Plot with error band (adatta come sopra)
plt.savefig('torque_multi_N6.png')