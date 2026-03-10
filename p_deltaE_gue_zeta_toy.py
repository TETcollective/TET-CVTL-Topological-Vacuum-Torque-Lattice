import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma  # non strettamente necessario qui, ma ok

# Parametri toy
N_samples = 10000           # numero di fluttuazioni simulate
sigma = 0.5                 # broadening ambientale (meV)
t_mean = 100.0              # valore medio t per zeta (linea critica)

# 1. Densità GUE standard (Wigner surmise per unitary ensemble)
def gue_wigner(x):
    return (32 / np.pi**2) * x**2 * np.exp(-4 * x**2 / np.pi)

# 2. Modulazione zeta (approssimazione toy: oscillazioni log-periodiche)
def zeta_modulation(t):
    return 1.0 + 0.3 * np.sin(2 * np.pi * np.log(t + 1e-6) / np.log(10))

# 3. Generazione Delta E simulati
x_gue = np.random.gamma(3, scale=1/np.sqrt(2), size=N_samples)  # proxy GUE spacing
delta_E_base = x_gue * sigma

# Modulazione zeta (campionata intorno a t_mean)
mod = zeta_modulation(t_mean + np.random.normal(0, 10, N_samples))
delta_E_mod = delta_E_base * np.sqrt(mod)  # scaling toy

# Plot
plt.figure(figsize=(10, 6))
plt.hist(delta_E_mod, bins=80, density=True, alpha=0.6, color='teal', 
         label='Simulazioni GUE + zeta mod')

x = np.linspace(0, 5*sigma, 500)
plt.plot(x, gue_wigner(x/sigma)/sigma, 'k--', lw=2, label='GUE standard')
plt.plot(x, gue_wigner(x/sigma)/sigma * zeta_modulation(t_mean), 'r-', lw=1.8, 
         label='GUE + zeta mod (toy)')

plt.xlabel(r'$\Delta E$ (meV)')
plt.ylabel(r'Probabilità densità $P(\Delta E)$')
plt.title(r'Distribuzione fluttuazioni energetiche: GUE modulata zeta (toy model)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()  # ora attivo, senza warning
plt.savefig('code/p_deltaE_gue_zeta_toy.png', dpi=300, bbox_inches='tight')
plt.show()