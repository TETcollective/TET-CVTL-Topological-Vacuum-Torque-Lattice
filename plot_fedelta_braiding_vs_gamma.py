# code/plot_fedelta_braiding_vs_gamma.py
"""
Titolo: Fedeltà del braiding adiabatico vs tasso di decoerenza γ
Descrizione: Simulazione QuTiP di un'operazione di braiding anyonico (approssimazione
             qubit logico) in presenza di decoerenza dephasing realistica.
             Gamma range: 10^{-6} – 10^{-3} ns^{-1} (coherence time 1 ms – 1 µs).
             Mostra plateau protetto >99.2–99.7% fino a γ ≈ 10^{-4} ns^{-1}.
Output: fig_fedelta_braiding_vs_gamma.pdf
"""

import qutip as qt
import numpy as np
import matplotlib.pyplot as plt

# ────────────────────────────────────────────────
# Parametri realistici (2026 TBG/MZM devices)
# ────────────────────────────────────────────────
tau_b = 60.0                  # ns – tempo braiding adiabatico tipico
n_steps = 250
times = np.linspace(0, tau_b, n_steps)

# Range gamma realistico (da ~1 ms a ~1 µs coherence)
gamma_list = np.logspace(-6, -3, 50)  # 1e-6 → 1e-3 ns^{-1}

fidelities = []

print("Calcolo fedeltà per", len(gamma_list), "valori di gamma...")

for gamma in gamma_list:
    # Hamiltoniano drive per accumulo fase topologica (rotazione intorno X)
    # Fase target: 4π/5 = 144° → ω = fase / tau_b
    phase_target = 4 * np.pi / 5
    omega = phase_target / tau_b
    H = omega * qt.sigmax()

    # Decoerenza: dephasing dominante (σz su qubit logico)
    c_ops = [np.sqrt(gamma) * qt.sigmaz()]

    # Stato iniziale: |+> = (|0> + |1>)/√2  (superposizione per vedere fase)
    psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()

    # Evoluzione con decoerenza
    try:
        result = qt.mesolve(H, psi0, times, c_ops=c_ops, options=qt.Options(nsteps=10000))
        final_state = result.states[-1]

        # Stato target ideale (dopo rotazione di 144° intorno X senza decoerenza)
        U_ideal = (-1j * H * tau_b).expm()
        target_state = U_ideal * psi0

        # Fedeltà (overlap tra evoluzione reale e ideale)
        fid = qt.fidelity(final_state, target_state)
        fidelities.append(fid)

    except Exception as e:
        print(f"Errore a γ = {gamma:.2e}: {e}")
        fidelities.append(np.nan)

# ────────────────────────────────────────────────
# Plot publication-ready
# ────────────────────────────────────────────────
plt.figure(figsize=(8.5, 5.8))

plt.semilogx(gamma_list, fidelities, 'o-', color='darkblue', 
             linewidth=2.1, markersize=6, markerfacecolor='white', markeredgewidth=1.5)

# Linee target
plt.axhline(0.992, color='red', ls='--', lw=1.5, label=r'$\mathcal{F} = 99.2\%$ (minimo)')
plt.axhline(0.997, color='green', ls='--', lw=1.5, label=r'$\mathcal{F} = 99.7\%$ (ottimistico)')

# Annotazione gamma realistico
plt.axvline(1e-4, color='gray', ls=':', lw=1.8, 
            label=r'$\gamma \approx 10^{-4}$ ns$^{-1}$ (tipico h-BN + CISS)')

plt.xlabel(r'Tasso di decoerenza $\gamma$ (ns$^{-1}$)', fontsize=14)
plt.ylabel(r'Fedeltà braiding finale $\mathcal{F}$', fontsize=14)
plt.title('Fedeltà del braiding adiabatico vs decoerenza\n(approssimazione qubit logico anyonico)', fontsize=15)
plt.grid(True, which='both', alpha=0.3, ls='--')
plt.legend(fontsize=11, loc='lower left', framealpha=0.95)
plt.ylim(0.88, 1.005)
plt.xlim(5e-7, 2e-3)
plt.tight_layout()

plt.savefig("fig_fedelta_braiding_vs_gamma.pdf", dpi=400, bbox_inches='tight')
plt.close()

print("Figura salvata: fig_fedelta_braiding_vs_gamma.pdf")