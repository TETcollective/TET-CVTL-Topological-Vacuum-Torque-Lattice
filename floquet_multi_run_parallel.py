# Title: Multi-Run Floquet con parallelizzazione joblib (versione ottimizzata)

#floquet_multi_run_parallel.py

# Description: Esecuzione parallela di più run Floquet, statistiche mean/std,
# torque normalizzato per sito, seed globale, export PDF/SVG/PNG
# Author: Grok 4 (xAI) – per @PhysSoliman
# Date: March 02, 2026

import qutip as qt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yaml
from joblib import Parallel, delayed
import multiprocessing

# ────────────────────────────────────────────────
# REPRODUCIBILITY
np.random.seed(42)
qt.settings.has_openmp = False
qt.settings.atol = 1e-12
qt.settings.rtol = 1e-10

# ────────────────────────────────────────────────
# CONFIG
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

N = config['N']
T = 2 * np.pi
omega = config['drive_frequency']
lambda_ = config['drive_amplitude']
num_periods = config['periods']
points_per_period = config['time_points_per_period']
tlist = np.linspace(0, num_periods * T, num_periods * points_per_period)
num_runs = config['num_runs']
num_cores = config.get('parallel_cores', -1)
if num_cores == -1:
    num_cores = multiprocessing.cpu_count() - 1

# ────────────────────────────────────────────────
sigmax = qt.sigmax()
sigmaz = qt.sigmaz()

def tensor_op(op, pos, N):
    ops = [qt.qeye(2)] * N
    ops[pos] = op
    return qt.tensor(ops)

H0 = sum(tensor_op(sigmaz, i, N) * tensor_op(sigmaz, i+1, N) for i in range(N-1))
H1 = sum(tensor_op(sigmaz, i, N) * tensor_op(sigmax, i+1, N) for i in range(N-1))
L = sum(tensor_op(sigmax, i, N) for i in range(N))

def single_run(run_id):
    np.random.seed(42 + run_id)
    phase = np.random.uniform(0, 2*np.pi)

    # Define args dictionary locally for H_t_run and mesolve
    mesolve_args = {'lambda': lambda_, 'omega': omega}

    def H_t_run(t, args):
        return H0 + args['lambda'] * np.cos(args['omega'] * t + phase) * H1

    psi0 = qt.tensor([qt.Qobj(np.random.rand(2,1) + 1j*np.random.rand(2,1)).unit()
                      for _ in range(N)])

    result = qt.mesolve(H_t_run, psi0, tlist, args=mesolve_args)

    torque_run = []
    for idx, t in enumerate(tlist):
        state = result.states[idx]
        H_now = H_t_run(t, mesolve_args)
        comm = qt.commutator(H_now, L)
        torque_run.append(np.imag(qt.expect(comm, state)))

    integrated = np.trapezoid(torque_run, tlist)
    return integrated, torque_run

# ────────────────────────────────────────────────
print(f"Avvio {num_runs} run paralleli su {num_cores} core...")

results = Parallel(n_jobs=num_cores)(
    delayed(single_run)(i) for i in range(num_runs)
)

integrated_list = [r[0] for r in results]
all_torques = np.array([r[1] for r in results])

mean_int = np.mean(integrated_list)
std_int = np.std(integrated_list)
mean_per_site = mean_int / N
std_per_site = std_int / N

print(f"Mean integrated torque:      {mean_int:.6f} ± {std_int:.6f}")
print(f"Mean torque per site:        {mean_per_site:.6f} ± {std_per_site:.6f}")

# ────────────────────────────────────────────────
# PLOT CON ERROR BAND
mean_t = np.mean(all_torques, axis=0)
std_t = np.std(all_torques, axis=0)

plt.figure(figsize=(11, 6.5))
plt.plot(tlist / T, mean_t, 'b-', lw=1.8, label=f'Mean torque ({mean_int:.4f} ± {std_int:.4f})')
plt.fill_between(tlist / T, mean_t - std_t, mean_t + std_t, color='b', alpha=0.15)
plt.plot(tlist / T, mean_t / N, 'c--', lw=1.4, label=f'Mean / sito ({mean_per_site:.4f})')
plt.xlabel('Numero di periodi Floquet')
plt.ylabel('Torque')
plt.title(f'Floquet Multi-Run Parallelizzato ({num_runs} run)')
plt.legend(loc='upper right')
plt.grid(True, alpha=0.25)
plt.tight_layout()

base = 'floquet_multi_parallel'
plt.savefig(f'{base}.pdf', format='pdf', bbox_inches='tight', dpi=400)
plt.savefig(f'{base}.svg', format='svg', bbox_inches='tight')
plt.savefig(f'{base}_preview.png', dpi=200, bbox_inches='tight')
plt.show()

# ────────────────────────────────────────────────
pd.DataFrame({
    'Run': range(num_runs),
    'Integrated_Torque': integrated_list,
    'Integrated_Per_Site': [x / N for x in integrated_list]
}).to_csv(f'{base}_results.csv', index=False)