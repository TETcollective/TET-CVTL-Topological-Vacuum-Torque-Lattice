import numpy as np
import matplotlib.pyplot as plt

# Parametri realistici per sistemi bio (triptofano/aromatici)
Gamma_0 = 1e9  # s⁻¹, rate spontaneo singolo dipolo ~ ns⁻¹
N = np.logspace(0, 5, 300)  # da 1 a ~100.000 dipoli

# Rate superradiant max (theta=0)
Gamma_sr_max = N * Gamma_0

# Plot 1: Gamma_sr vs N (log-log)
fig1, ax1 = plt.subplots(figsize=(9, 6))
ax1.loglog(N, Gamma_sr_max, 'b-', lw=2.5, label=r'$\Gamma_{\mathrm{sr}} = N \Gamma_0 \text{ (max, } \theta=0^\circ\text{)}$')
ax1.axhline(Gamma_0, color='r', ls='--', lw=1.5, label=r'$\Gamma_0 \approx 10^9 \text{ s}^{\text{-}1} \text{ (singolo)}$')
ax1.set_xlabel('Numero di dipoli coerenti $N$', fontsize=14)
ax1.set_ylabel(r'$\text{Rate di decadimento collettivo } \Gamma_{\mathrm{sr}} \text{ (s}^{\text{-}1}\text{)}$', fontsize=14)
ax1.set_title('Enhancement superradiant vs N (regime cooperativo Dicke)', fontsize=15)
ax1.grid(True, which="both", ls="--", alpha=0.5)
ax1.legend(fontsize=12)
ax1.tick_params(labelsize=12)
plt.tight_layout()
plt.savefig('rate_superradiant_vs_N.png', dpi=300)
plt.show()

# Plot 2: Fattore di forma vs theta
theta_deg = np.linspace(0, 180, 361)
theta_rad = np.deg2rad(theta_deg)
factor_form = ((1 + np.cos(theta_rad)) / 2)**2

fig2, ax2 = plt.subplots(figsize=(9, 6))
ax2.plot(theta_deg, factor_form, 'g-', lw=2.5)
ax2.set_xlabel(r'$\text{Angolo di emissione } \theta \text{ (gradi)}$', fontsize=14)
ax2.set_ylabel(r'$\text{Fattore di forma } \left( \frac{1 + \cos\theta}{2} \right)^2$', fontsize=14)
ax2.set_title(r'$\text{Direzionalità superradiance (fattore di forma vs } \theta \text{)}$', fontsize=15)
ax2.grid(True, alpha=0.5)
ax2.set_ylim(0, 1.05)
ax2.set_xlim(0, 180)
ax2.tick_params(labelsize=12)
plt.tight_layout()
plt.savefig('fattore_forma_vs_theta.png', dpi=300)
plt.show()