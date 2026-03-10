# Title: Multi-Run Vacuum Torque Extraction Simulation in 2+1D Toy Model with Lindblad Dissipation using QuTiP
# Description: Multi-run with dissipation, random init/phase. Saves CSV for paper.
# Author: Grok 4 (xAI) - Generated for @PhysSoliman
# Date: March 02, 2026

import qutip as qt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

N = 3
num_runs = 10
gamma = 0.01
sigmam = qt.sigmam()

# --- Required definitions for H0, H_drive, c_ops, and torque calculation ---
# Assuming omega = 1.0 from args for T calculation
T = 2 * np.pi

sigmax = qt.sigmax()
sigmaz = qt.sigmaz()

def tensor_op(op, pos, N):
    ops = [qt.qeye(2)] * N
    ops[pos] = op
    return qt.tensor(ops)

# Static Hamiltonian (e.g., string tension)
H0_static = sum(tensor_op(sigmaz, i, N) * tensor_op(sigmaz, i+1, N) for i in range(N-1))

# Drive Hamiltonian (e.g., braiding proxy)
H_drive_op = sum(tensor_op(sigmaz, i, N) * tensor_op(sigmax, i+1, N) for i in range(N-1))

def H_t(t, args):
    # Use args['lambda_'] as defined in the loop
    return H0_static + args['lambda_'] * np.cos(args['omega'] * t) * H_drive_op

# Angular momentum operator (proxy for torque)
L = sum(tensor_op(sigmax, i, N) for i in range(N))

# --- End of required definitions ---

integrated_torques = []

for run in range(num_runs):
    np.random.seed(run)
    phase = np.random.uniform(0, 2*np.pi)
    args = {'lambda_': 0.5, 'omega': 1.0, 'phase': phase}
    psi0 = qt.tensor([qt.Qobj(np.random.rand(2,1) + 1j*np.random.rand(2,1)).unit() for _ in range(N)])
    c_ops = [np.sqrt(gamma) * tensor_op(sigmam, i, N) for i in range(N)]

    # Define tlist for the simulation within each run
    num_periods_sim = 20 # Example, can be made configurable
    points_per_period_sim = 50 # Example, can be made configurable
    tlist = np.linspace(0, num_periods_sim * T, num_periods_sim * points_per_period_sim)

    # Evolve with mesolve(c_ops)
    result = qt.mesolve(H_t, psi0, tlist, c_ops=c_ops, args=args)

    # Compute torque/integrated
    torque_current_run = []
    for idx, t in enumerate(tlist):
        state = result.states[idx]
        # Pass args to H_t function
        H_now = H_t(t, args)
        comm = qt.commutator(H_now, L)
        expect = qt.expect(comm, state)
        torque_current_run.append(np.imag(expect))

    # Calculate integrated torque for the current run
    integrated = np.trapezoid(torque_current_run, tlist)

    integrated_torques.append(integrated)

mean_torque = np.mean(integrated_torques)
std_torque = np.std(integrated_torques)
print(f"Mean integrated torque (Lindblad gamma={gamma}): {mean_torque:.4f} ± {std_torque:.4f}")

df = pd.DataFrame({'Run': range(num_runs), 'Integrated_Torque': integrated_torques})
df.to_csv('results_lindblad_multi.csv', index=False)

# Plot
plt.savefig('torque_multi_lindblad.png')