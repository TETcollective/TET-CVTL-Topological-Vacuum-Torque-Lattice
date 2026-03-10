import numpy as np
import matplotlib.pyplot as plt

# Parametri toy per visualizzazione dinamica
t = np.linspace(0, 50, 800)          # tempo (unità arbitrarie, più punti per liscia)
omega = 2 * np.pi / 8                # frequenza braiding periodico
beta = 0.381966                      # kick retrocausale phi^{-2}
tau_mean = 1.0                       # torque medio base (unità arb.)
noise_amp = 0.08                     # ampiezza rumore ambientale

# Torque dinamico: modulazione sinusoidale + kick cos + rumore
tau_t = tau_mean * (1 + 0.6 * np.sin(omega * t)) \
      + beta * 0.8 * np.cos(omega * t) \
      + noise_amp * np.random.randn(len(t))

plt.figure(figsize=(11, 6))
plt.plot(t, tau_t, 'b-', lw=2.2, label=r'$\tau_{\mathrm{topo}}(t)$ dinamico')
plt.axhline(tau_mean, color='k', ls='--', lw=1.8, label=r'$\langle \tau \rangle$ medio')
plt.xlabel('Tempo (unità arbitrarie)')
plt.ylabel(r'Torque topologico $\tau(t)$ (unità arbitrarie)')
plt.title('Torque topologico dinamico vs tempo (toy model Lindblad + retrocausal kick)')
plt.legend(fontsize=11, loc='upper right')
plt.grid(True, alpha=0.35, ls='--')
plt.tight_layout()
plt.savefig('code/torque_vs_time_toy.png', dpi=300, bbox_inches='tight')
plt.show()