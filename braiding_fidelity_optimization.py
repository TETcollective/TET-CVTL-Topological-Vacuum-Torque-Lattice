"""
Ottimizzazione fedeltà braiding adiabatico con QuTiP
Framework TET--CVTL / RENASCENT-Q

Simula evoluzione Lindblad di un qubit toy con:
- Hamiltoniano drive: rotazione π/2 adiabatica (H = (π/(2 τ_b)) σ_x)
- Decoerenza dephasing: c_op = √γ σ_z
- Calcolo fedeltà finale rispetto all'evoluzione unitaria ideale
- Heatmap 2D: fedeltà vs τ_b (tempo adiabatico) e γ (decoerenza)

Autore: Simon Soliman (tetcollective.org)
Data: Marzo 2026
Versione: 1.2 (label LaTeX puliti, no warning escape)

Output:
- fidelity_heatmap.png (in cartella code/)
- Parametri ottimali stampati
"""

import sys
import os
import numpy as np
import qutip as qt
import matplotlib.pyplot as plt

# Verifica se siamo in Colab → installa/aggiorna QuTiP se necessario
IS_COLAB = 'google.colab' in sys.modules
if IS_COLAB:
    print("Ensuring QuTiP is installed...")
    !pip install qutip --upgrade

# --- Parametri simulazione ---
gamma_list = np.logspace(-5, -1, 40)          # γ da 1e-5 a 0.1 ns⁻¹
tau_b_list  = np.logspace(1, np.log10(200), 20)  # τ_b da 10 a 200 ns

# Opzioni solver per stabilità numerica
solver_options = {'nsteps': 50000, 'atol': 1e-7, 'rtol': 1e-5}

# Griglia fedeltà (righe: tau_b, colonne: gamma)
fidelities_grid = np.zeros((len(tau_b_list), len(gamma_list)))

print("Starting fidelity optimization simulation...")

for i, tau_b in enumerate(tau_b_list):
    # Punti temporali proporzionali a τ_b
    N_points = 5000
    times = np.linspace(0, tau_b, N_points)

    # Hamiltoniano ideale per rotazione π/2
    H_drive = (np.pi / (2 * tau_b)) * qt.sigmax()

    # Stato target ideale (evoluzione unitaria completa)
    U_ideal = (-1j * H_drive * tau_b).expm()
    psi0 = qt.basis(2, 0)
    target_rho = U_ideal * psi0 * psi0.dag() * U_ideal.dag()

    for j, gamma in enumerate(gamma_list):
        # Hamiltoniano + collasso operators
        H = H_drive
        c_ops = [np.sqrt(gamma) * qt.sigmaz()]

        rho0 = psi0 * psi0.dag()

        try:
            # Evoluzione Lindblad
            result = qt.mesolve(
                H, rho0, times,
                c_ops=c_ops,
                e_ops=[],
                options=solver_options
            )

            if result.states:
                final_rho = result.states[-1]
                fid = qt.fidelity(final_rho, target_rho)
                fidelities_grid[i, j] = fid
            else:
                fidelities_grid[i, j] = np.nan

        except Exception as e:
            print(f"Errore a τ_b={tau_b:.2f} ns, γ={gamma:.2e}: {e}")
            fidelities_grid[i, j] = np.nan

print("Simulation complete. Fidelity grid generated.")

# --- Creazione Heatmap ---
fig, ax = plt.subplots(figsize=(10, 7))

extent = [
    np.log10(gamma_list.min()),
    np.log10(gamma_list.max()),
    tau_b_list.min(),
    tau_b_list.max()
]

im = ax.imshow(
    fidelities_grid,
    origin='lower',
    aspect='auto',
    cmap='viridis',
    extent=extent
)

cbar = fig.colorbar(im, ax=ax, label=r'Braiding Fidelity $\mathcal{F}$', format='%.3f')
cbar.ax.tick_params(labelsize=10)

ax.set_xlabel(r'$\log_{10} \gamma$ (ns$^{-1}$)', fontsize=12)
ax.set_ylabel(r'$\tau_b$ (ns)', fontsize=12)
ax.set_title(r'Braiding Fidelity Heatmap vs. $\tau_b$ and $\gamma$', fontsize=14)

# Tick personalizzati sull'asse x (log γ)
gamma_ticks = np.logspace(np.log10(gamma_list.min()), np.log10(gamma_list.max()), 5)
ax.set_xticks(np.log10(gamma_ticks))
ax.set_xticklabels([f'{g:.1e}' for g in gamma_ticks])

plt.grid(False)  # opzionale: rimuovi griglia per pulizia

# Salva in alta risoluzione
output_dir = 'code'
os.makedirs(output_dir, exist_ok=True)
save_path = os.path.join(output_dir, 'braiding_fidelity_heatmap.png')
plt.savefig(save_path, dpi=300, bbox_inches='tight')
print(f"Heatmap salvata in: {save_path}")

plt.show()

# --- Parametri ottimali ---
max_fid = np.nanmax(fidelities_grid)
if np.isnan(max_fid):
    print("Attenzione: tutte le fedeltà sono NaN.")
else:
    max_idx = np.unravel_index(np.nanargmax(fidelities_grid), fidelities_grid.shape)
    opt_tau_b = tau_b_list[max_idx[0]]
    opt_gamma = gamma_list[max_idx[1]]

    print("\nParametri ottimali trovati:")
    print(f"  τ_b ottimale: {opt_tau_b:.2f} ns")
    print(f"  γ ottimale:   {opt_gamma:.2e} ns⁻¹")
    print(f"  Fedeltà massima: {max_fid:.4f}")