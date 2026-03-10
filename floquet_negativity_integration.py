# Title: Integrazione Floquet + Entanglement Negativity (versione finale ottimizzata)

#floquet_negativity_integration.py


# Description: Simulazione Floquet con calcolo torque e negativity, parametri da YAML,
# seed globale, torque normalizzato per sito, export multi-formato (PDF/SVG/PNG)
# Author: Grok 4 (xAI) – per @PhysSoliman / TETcollective
# Date: March 02, 2026

import qutip as qt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yaml
import warnings
import scipy.linalg # Import scipy for LinAlgWarning

# ────────────────────────────────────────────────
# REPRODUCIBILITY & SUPPRESSIONE WARNING INNOCUO
np.random.seed(42)
qt.settings.has_openmp = False
qt.settings.atol = 1e-12
qt.settings.rtol = 1e-10

# Sopprimi solo il LinAlgWarning specifico su sqrtm (non nasconde altri problemi)
warnings.filterwarnings("ignore", category=scipy.linalg.LinAlgWarning)

# ────────────────────────────────────────────────
# CONFIG DA YAML (assumi config.yaml nella stessa cartella o adatta path)
try:
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print("config.yaml non trovato → uso valori default")
    config = {
        'N': 4,
        'drive_frequency': 1.0,
        'drive_amplitude': 0.8,
        'periods': 20,
        'time_points_per_period': 50,
        'bipartition_A_size': 2
    }

N = config['N']
T = 2 * np.pi
omega = config['drive_frequency']
lambda_ = config['drive_amplitude']
num_periods = config['periods']
points_per_period = config['time_points_per_period']
tlist = np.linspace(0, num_periods * T, num_periods * points_per_period)
m_A = config['bipartition_A_size']

# ────────────────────────────────────────────────
sigmax = qt.sigmax()
sigmaz = qt.sigmaz()

def tensor_op(op, pos, N):
    ops = [qt.qeye(2)] * N
    ops[pos] = op
    return qt.tensor(ops)

H0 = sum(tensor_op(sigmaz, i, N) * tensor_op(sigmaz, i+1, N) for i in range(N-1))
H1 = sum(tensor_op(sigmaz, i, N) * tensor_op(sigmax, i+1, N) for i in range(N-1))

def H_t(t, args):
    return H0 + args['lambda'] * np.cos(args['omega'] * t) * H1

L = sum(tensor_op(sigmax, i, N) for i in range(N))

# ────────────────────────────────────────────────
# STATO INIZIALE ENTANGLED (corretto e scalabile)
if N >= 2:
    # Bell state (|00> + |11>)/√2 sui primi due qubit
    bell_2q = (qt.tensor(qt.basis(2,0), qt.basis(2,0)) +
               qt.tensor(qt.basis(2,1), qt.basis(2,1))).unit() / np.sqrt(2)
    vacuum_rest = [qt.basis(2, 0) for _ in range(N - 2)]
    psi0 = qt.tensor(bell_2q, *vacuum_rest)
else:
    psi0 = qt.basis(2, 0)  # fallback per N=1

# ────────────────────────────────────────────────
# EVOLUZIONE
result = qt.mesolve(H_t, psi0, tlist, args={'lambda': lambda_, 'omega': omega})

torque = []
negativity_values = []

for idx, t in enumerate(tlist):
    state = result.states[idx]
    H_now = H_t(t, {'lambda': lambda_, 'omega': omega})
    comm = qt.commutator(H_now, L)
    torque.append(np.imag(qt.expect(comm, state)))

    neg = qt.negativity(state, subsys=list(range(m_A)))
    negativity_values.append(neg)

# ────────────────────────────────────────────────
integrated_torque = np.trapezoid(torque, tlist)
integrated_per_site = integrated_torque / N

print(f"Integrated torque raw:       {integrated_torque:>10.6f}")
print(f"Integrated torque per site:  {integrated_per_site:>10.6f}")
print(f"Mean negativity:             {np.mean(negativity_values):>10.4f}")

# ────────────────────────────────────────────────
# PLOT PROFESSIONALE
fig, ax1 = plt.subplots(figsize=(12, 6.8))

ax1.plot(tlist / T, torque, 'b-', lw=1.6, alpha=0.9, label=f'Torque raw (∫ = {integrated_torque:.4f})')
ax1.plot(tlist / T, np.array(torque)/N, 'c--', lw=1.4, alpha=0.8, label=f'Torque / qubit (∫ = {integrated_per_site:.4f})')
ax1.set_xlabel('Numero di periodi Floquet', fontsize=12)
ax1.set_ylabel('Torque', color='b', fontsize=12)
ax1.tick_params(axis='y', labelcolor='b')
ax1.grid(True, alpha=0.18, linestyle='--')

ax2 = ax1.twinx()
ax2.plot(tlist / T, negativity_values, 'r-', lw=1.8, alpha=0.85, label='Negativity')
ax2.set_ylabel('Entanglement Negativity', color='r', fontsize=12)
ax2.tick_params(axis='y', labelcolor='r')

fig.suptitle('Floquet Drive: Torque Extraction vs Entanglement Negativity', fontsize=14, y=0.96)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=10, framealpha=0.92)
plt.tight_layout(rect=[0, 0, 1, 0.96])

# Esportazione multi-formato (alta qualità)
base = 'floquet_negativity_integration'
plt.savefig(f'{base}.pdf', format='pdf', bbox_inches='tight', dpi=400)
plt.savefig(f'{base}.svg', format='svg', bbox_inches='tight')
plt.savefig(f'{base}_preview.png', dpi=220, bbox_inches='tight')
plt.show()

# ────────────────────────────────────────────────
# SALVATAGGIO DATI
df = pd.DataFrame({
    't/T': tlist / T,
    'torque_raw': torque,
    'torque_per_qubit': np.array(torque) / N,
    'negativity': negativity_values
})
df.attrs['integrated_torque_raw'] = integrated_torque
df.attrs['integrated_torque_per_qubit'] = integrated_per_site
df.attrs['mean_negativity'] = np.mean(negativity_values)
df.to_csv(f'{base}_data.csv', index=False)
print(f"Dati salvati in {base}_data.csv")