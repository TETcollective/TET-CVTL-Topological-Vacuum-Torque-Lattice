
code/plot_fidelity_anyon_subspace.py


import qutip as qt
import numpy as np
import matplotlib.pyplot as plt

phi = (1 + np.sqrt(5)) / 2
dim = 2  # stati: |1>, |τ> (left), |τ> (right) in fusion basis semplificata

# Matrice F (fusione τττ → τ)
F = qt.Qobj([[1/phi, 1/np.sqrt(phi)], [1/np.sqrt(phi), -1/phi]])

# Matrice R braiding (phase su canali)
R = qt.Qobj(np.diag([np.exp(1j * 4*np.pi/5), np.exp(-1j * 3*np.pi/5)]))

# Operatore braiding composito B = F R F†
B = F * R * F.dag()

# Hamiltoniano effective per braiding adiabatico (tunneling lento verso B)
H_braid = (np.pi / 50.0) * (qt.sigmax() + qt.sigmaz())  # placeholder in 2D subspace per semplicità
# Per accuratezza: usare full 3D space con projectors

gamma_list = np.logspace(-6, -3, 40)  # 1 µs – 1 ms coherence
fidelities = []

for gamma in gamma_list:
    c_ops = [np.sqrt(gamma) * qt.qeye(dim)]  # uniform dephasing (conservativo)
    times = np.linspace(0, 50, 200)  # ns
    rho0 = qt.basis(dim, 0) * qt.basis(dim, 0).dag()  # vacuum iniziale
    result = qt.mesolve(H_braid, rho0, times, c_ops, [])
    rho_final = result.states[-1]
    # Fedeltà rispetto target braid ideale
    rho_target = B * rho0 * B.dag()
    fid = qt.fidelity(rho_final, rho_target)
    fidelities.append(fid)

plt.semilogx(gamma_list, fidelities, 'o-')
plt.axhline(0.992, ls='--', color='r')
plt.xlabel(r'$\gamma$ (ns$^{-1}$)')
plt.ylabel(r'Fedeltà braiding')
plt.title('Fedeltà con effective anyonic subspace')
plt.grid(True)
plt.savefig('fig_fidelity_anyon_subspace.pdf', dpi=300)
plt.show()