# code/plot_torque_vs_floquet_frequency.py
import qutip as qt
import numpy as np
import matplotlib.pyplot as plt

# Parametri Floquet per drive (GHz range)
freq_range = np.linspace(0.5, 15, 60)   # GHz
delta_V = 30e-3      # V (ampiezza gate drive, realistico)
period = 1 / (freq_range * 1e9) * 1e9   # in ns

# Torque stimato ~ proporcional a energia Casimir-like / drive (toy model)
# τ_vac ~ (ħ ω / c) * (δV / V_0)^2 * sin(phase)  → semplificato
hbar = 1.0545718e-34
c = 3e8
torque_scale = 1e-20   # ordine di grandezza da letteratura (10^{-20}–10^{-18} N·m)

torque = []
for f in freq_range:
    omega = 2 * np.pi * f * 1e9
    # Ampiezza torque oscillante (media su ciclo Floquet)
    tau_avg = torque_scale * (omega / (2*np.pi*1e9))**1.5 * (delta_V / 0.1)**2
    torque.append(tau_avg * 1e18)   # in attoN·m (10^{-18})

plt.figure(figsize=(8, 5.5))
plt.plot(freq_range, torque, 's-', color='purple', markersize=6, lw=2)
plt.xlabel(r'Frequenza drive Floquet (GHz)', fontsize=13)
plt.ylabel(r'Torque medio dal vuoto $\langle \tau_{\mathrm{vac}} \rangle$ (aN·m)', fontsize=13)
plt.title('Estrazione torque dinamico vs frequenza Floquet\n(toy model Casimir + braiding)')
plt.grid(True, alpha=0.3)
plt.yscale('log')
plt.tight_layout()
plt.savefig('fig_torque_vs_floquet.pdf', dpi=400, bbox_inches='tight')
plt.close()
print("Figura torque salvata.")