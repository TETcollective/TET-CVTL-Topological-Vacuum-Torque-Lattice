# Title: Multi-Run Vacuum Torque Extraction Simulation in 2+1D Toy Model using QuTiP (Base N=3)
# Description: Executes multiple runs with randomized initial states to estimate mean and std of integrated torque.
# Saves results to CSV for paper analysis. Based on TET-CVTL framework.
# Author: Grok 4 (xAI) - Generated for @PhysSoliman
# Date: March 02, 2026

# ────────────────────────────────────────────────
# MULTI-RUN CON RACCOLTA COMPLETA DEI TORQUE(t)
integrated_torques = []
all_torques = []  # lista di array (uno per run)

for run in range(num_runs):
    np.random.seed(42 + run)
    phase = np.random.uniform(0, 2 * np.pi)

    def H_t_run(t, args):
        return H0 + args['lambda'] * np.cos(args['omega'] * t + phase) * H_drive

    args_run = {'lambda': lambda_, 'omega': omega}

    # Stato iniziale randomizzato (opzionale, ma utile per variabilità)
    psi0_run = qt.tensor([qt.Qobj(np.random.rand(2,1) + 1j*np.random.rand(2,1)).unit()
                          for _ in range(N)])

    result = qt.mesolve(H_t_run, psi0_run, tlist, args=args_run)

    torque_run = []
    for idx, t in enumerate(tlist):
        state = result.states[idx]
        H_now = H_t_run(t, args_run)
        comm = qt.commutator(H_now, L)
        torque_run.append(np.imag(qt.expect(comm, state)))

    integrated = np.trapezoid(torque_run, tlist)
    integrated_torques.append(integrated)
    all_torques.append(torque_run)  # <--- QUI: raccogli il torque(t) di questo run

# Converti in array NumPy (shape: num_runs × len(tlist))
all_torques = np.array(all_torques)

# ────────────────────────────────────────────────
mean_integrated = np.mean(integrated_torques)
std_integrated = np.std(integrated_torques)
mean_per_site = mean_integrated / N

print(f"Mean integrated torque:     {mean_integrated:.4f} ± {std_integrated:.4f}")
print(f"Mean torque per site:       {mean_per_site:.4f}")

# ────────────────────────────────────────────────
# PLOT CON ERROR BAND (ORA FUNZIONA)
mean_t = np.mean(all_torques, axis=0)
std_t = np.std(all_torques, axis=0)

plt.figure(figsize=(11, 6.5))
plt.plot(tlist, mean_t, 'b-', lw=1.8, label=f'Mean torque (∫ = {mean_integrated:.4f} ± {std_integrated:.4f})')
plt.fill_between(tlist, mean_t - std_t, mean_t + std_t, color='b', alpha=0.15, label='±1 std')
plt.xlabel('Time')
plt.ylabel('Torque')
plt.title(f'Multi-Run Torque with Error Band (N={N}, {num_runs} runs)')
plt.legend()
plt.grid(True, alpha=0.25)
plt.tight_layout()

base = 'torque_multi_base'
plt.savefig(f'{base}.pdf', format='pdf', bbox_inches='tight', dpi=400)
plt.savefig(f'{base}.svg', format='svg', bbox_inches='tight')
plt.savefig(f'{base}_preview.png', dpi=220, bbox_inches='tight')
plt.show()

# Salva CSV
pd.DataFrame({
    'Run': range(num_runs),
    'Integrated_Torque': integrated_torques,
    'Integrated_Per_Site': [x / N for x in integrated_torques]
}).to_csv(f'{base}_results.csv', index=False)