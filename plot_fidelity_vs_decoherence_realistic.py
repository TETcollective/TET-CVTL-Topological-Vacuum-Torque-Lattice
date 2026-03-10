import sys
IS_COLAB = 'google.colab' in sys.modules
if IS_COLAB:
  print('Ensuring QuTiP is installed...')
  !pip install qutip --upgrade

# code/plot_fidelity_vs_decoherence_realistic.py
import qutip as qt
import numpy as np
import matplotlib.pyplot as plt

# Parametri realistici
tau_b = 50.0          # ns, tempo braiding adiabatico tipico
gamma_list = np.logspace(-6, -2, 50)   # 1e-6 a 1e-2 ns^-1 (realistico per topologico protetto)
N_points = 300
times = np.linspace(0, tau_b, N_points)

fidelities = []

for gamma in gamma_list:
    # Effective Hamiltonian per braiding anyon Fibonacci (string-net like: clock model 3-state)
    # H ~ sum (clock operators) per creare effective braiding drive
    dim = 3  # effective 3-level per Fibonacci fusion space (1 + tau)
    sigma_clock = qt.Qobj([[0,1,0],[0,0,1],[1,0,0]])  # clock shift operator
    tau_clock = qt.Qobj([[1,0,0],[0,np.exp(1j*2*np.pi/3),0],[0,0,np.exp(-1j*2*2*np.pi/3)]])

    # Drive per braiding adiabatico (rotazione lenta nel fusion space)
    H = (2 * np.pi / tau_b) * (sigma_clock + sigma_clock.dag())   # effective braiding drive

    # Decoerenza: dephasing dominante in topologici (Z_2 o phase damping)
    c_ops = [np.sqrt(gamma) * tau_clock]  # dephasing su anyonic charge basis

    # Stato iniziale: logical |0> encoded (es. vacuum fusion)
    rho0 = qt.basis(dim, 0) * qt.basis(dim, 0).dag()

    # Evoluzione
    result = qt.mesolve(H, rho0, times, c_ops, [])

    # Fedeltà rispetto evoluzione ideale (unitaria senza decoerenza)
    U_ideal = (-1j * H * tau_b).expm()
    rho_ideal_final = U_ideal * rho0 * U_ideal.dag()
    fid = qt.fidelity(result.states[-1], rho_ideal_final)
    fidelities.append(fid)

plt.figure(figsize=(8,5.5))
plt.semilogx(gamma_list, fidelities, 'o-', color='darkblue', linewidth=2.2, markersize=5)
plt.axhline(0.992, color='red', ls='--', lw=1.5, label=r'$\mathcal{F}=99.2\%$ (target minimo)')
plt.axhline(0.997, color='green', ls='--', lw=1.5, label=r'$\mathcal{F}=99.7\%$ (target ottimistico)')
plt.xlabel(r'Tasso decoerenza $\gamma$ (ns$^{-1}$)', fontsize=13)
plt.ylabel(r'Fedeltà braiding finale $\mathcal{F}$', fontsize=13)
plt.title('Fedeltà braiding adiabatico vs decoerenza\n(String-net effective model)', fontsize=14)
plt.grid(True, which='both', alpha=0.3)
plt.legend(fontsize=11)
plt.ylim(0.90, 1.005)
plt.tight_layout()
plt.savefig('fig_fidelity_vs_decoherence_realistic.pdf', dpi=400, bbox_inches='tight')
plt.close()
print("Figura salvata: fig_fidelity_vs_decoherence_realistic.pdf")