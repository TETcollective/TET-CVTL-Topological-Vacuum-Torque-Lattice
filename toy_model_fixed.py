# Title: Fixed Vacuum Torque Extraction Simulation in 2+1D Toy Model using QuTiP
# Description: Simulates a simplified Fibonacci string-net on small lattice with Floquet drive to extract vacuum torque.
# Fixed np.trapz deprecation warning by using np.trapezoid.
# Based on TET-CVTL framework. Uses QuTiP for quantum dynamics.
# Author: Grok 4 (xAI) - Generated for @PhysSoliman

#toy_model_fixed.py

# Date: March 02, 2026

import qutip as qt
import numpy as np
import matplotlib.pyplot as plt

# Define a simple 3-qubit chain for toy model (approximating honeycomb segment)
N = 3  # Number of qubits (expand for larger lattice)

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

# Ground Hamiltonian H0: sum ZZ (string tension proxy)
H0 = 0 * identity
for i in range(N-1):
    H0 += tensor_op(sigmaz, i, N) * tensor_op(sigmaz, i+1, N)

# Drive Hamiltonian: sum ZX (braiding drive proxy)
H_drive = 0 * identity
for i in range(N-1):
    H_drive += tensor_op(sigmaz, i, N) * tensor_op(sigmax, i+1, N)

# Drive function for Floquet: lambda sin(omega t)
def drive_func(t, args):
    return args['lambda_'] * np.sin(args['omega'] * t)

# Full H for time evolution
H = [H0, [H_drive, drive_func]]

# Angular momentum L: total Sx (torque proxy)
L = 0 * identity
for i in range(N):
    L += tensor_op(sigmax, i, N)

# Initial state: |000...> (ground proxy)
psi0 = qt.tensor([qt.basis(2, 0) for _ in range(N)])

# Parameters
tlist = np.linspace(0, 10, 100)  # Time grid
lambda_ = 0.5  # Drive strength
omega = 1.0  # Frequency
args = {'lambda_': lambda_, 'omega': omega}

# Evolve system
result = qt.mesolve(H, psi0, tlist, args=args)

# Compute torque tau(t) = Im <[H(t), L]>
torque = []
for idx, t in enumerate(tlist):
    state = result.states[idx]
    Ht = H0 + drive_func(t, args) * H_drive
    comm = qt.commutator(Ht, L)
    expect = state.overlap(comm * state)  # Complex <comm>
    torque.append(np.imag(expect))

# Integrated torque (fixed with np.trapezoid)
integrated_torque = np.trapezoid(torque, tlist)
print(f"Integrated torque over time: {integrated_torque}")

# Plot results
plt.figure()
plt.plot(tlist, torque)
plt.xlabel('Time')
plt.ylabel('Instantaneous Torque Im <[H,L]>')
plt.title('Vacuum Torque Extraction in TET-CVTL Toy Model')
plt.savefig('torque_plot.png')  # Save plot for reference
plt.show()