# Title: Vacuum Torque Extraction Simulation in 2+1D Toy Model with Lindblad Dissipation using QuTiP
#toy_model_lindblad.py
# Description: Adds Lindblad collapse operators for decoherence (gamma rate), simulating open system effects.
# Based on original N=3 chain for TET-CVTL framework.
# Author: Grok 4 (xAI) - Generated for @PhysSoliman
# Date: March 02, 2026

import qutip as qt
import numpy as np
import matplotlib.pyplot as plt

N = 3  # Qubits

# Basis operators
sigmax = qt.sigmax()
sigmaz = qt.sigmaz()
sigmam = qt.sigmam()  # For collapse

# Tensor product helper
def tensor_op(op, i, N):
    ops = [qt.qeye(2)] * N
    ops[i] = op
    return qt.tensor(ops)

# Full identity
identity = qt.tensor([qt.qeye(2)] * N)

# Ground Hamiltonian H0: sum ZZ
H0 = 0 * identity
for i in range(N-1):
    H0 += tensor_op(sigmaz, i, N) * tensor_op(sigmaz, i+1, N)

# Drive Hamiltonian: sum ZX
H_drive = 0 * identity
for i in range(N-1):
    H_drive += tensor_op(sigmaz, i, N) * tensor_op(sigmax, i+1, N)

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

# Lindblad collapse operators: decoherence (bit-flip like, gamma rate)
gamma = 0.01  # Dissipation rate (small)
c_ops = [np.sqrt(gamma) * tensor_op(sigmam, i, N) for i in range(N)]

# Parameters
tlist = np.linspace(0, 10, 100)
lambda_ = 0.5
omega = 1.0
args = {'lambda_': lambda_, 'omega': omega}

# Evolve with dissipation
result = qt.mesolve(H, psi0, tlist, c_ops=c_ops, args=args)

# Compute torque (now on density matrix)
torque = []
for idx, t in enumerate(tlist):
    rho = result.states[idx]  # Density matrix
    Ht = H0 + drive_func(t, args) * H_drive
    comm = qt.commutator(Ht, L)
    expect = qt.expect(comm, rho)  # Complex
    torque.append(np.imag(expect))

# Integrated torque
integrated_torque = np.trapezoid(torque, tlist)
print(f"Integrated torque over time (with Lindblad, gamma={gamma}): {integrated_torque}")

# Plot
plt.figure()
plt.plot(tlist, torque)
plt.xlabel('Time')
plt.ylabel('Instantaneous Torque Im <[H,L]>')
plt.title('Vacuum Torque Extraction in TET-CVTL with Dissipation')
plt.savefig('torque_plot_lindblad.png')
plt.show()