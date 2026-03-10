# Title: Vacuum Torque Extraction Simulation in 2+1D Toy Model with N=6 Qubits using QuTiP
# Description: Extended version with larger linear chain (N=6 qubits) for better approximation of lattice effects.
# Based on TET-CVTL framework. Uses QuTiP for quantum dynamics.
# Author: Grok 4 (xAI) - Generated for @PhysSoliman
# Date: March 02, 2026

import qutip as qt
import numpy as np
import matplotlib.pyplot as plt

N = 6  # Larger number of qubits

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

# Ground Hamiltonian H0: sum ZZ over chain
H0 = 0 * identity
for i in range(N-1):
    H0 += tensor_op(sigmaz, i, N) * tensor_op(sigmaz, i+1, N)

# Drive Hamiltonian: sum ZX over chain
H_drive = 0 * identity
for i in range(N-1):
    H_drive += tensor_op(sigmaz, i, N) * tensor_op(sigmax, i+1, N)

# Drive function for Floquet: lambda sin(omega t)
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

# Evolve (note: N=6 is 64D, feasible but slower)
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
print(f"Integrated torque over time (N=6): {integrated_torque}")

# Plot
plt.figure()
plt.plot(tlist, torque)
plt.xlabel('Time')
plt.ylabel('Instantaneous Torque Im <[H,L]>')
plt.title('Vacuum Torque Extraction in TET-CVTL Toy Model (N=6)')
plt.savefig('torque_plot_N6.png')
plt.show()