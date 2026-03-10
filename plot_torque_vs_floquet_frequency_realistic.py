# code/plot_torque_vs_floquet_frequency_realistic.py
"""
Titolo: Torque medio estratto dal vuoto vs frequenza drive Floquet
Descrizione: Modello toy scaling realistico per estrazione dinamica di torque 
             dal vuoto quantistico tramite drive Floquet anyonico (range 1–12 GHz).
             Torque ~ scaling con ω^{1.2} e ampiezza gate δV.
Output: fig_torque_floquet_realistic.pdf
"""



import qutip as qt
import numpy as np
import matplotlib.pyplot as plt

# Parametri Floquet
freqs = np.linspace(1, 12, 50)  # GHz
omega_d = 2 * np.pi * freqs * 1e9  # rad/s
delta_V = 30e-3  # V

# Toy model: energia assorbita per ciclo ~ torque * angular disp.
# Torque medio ~ (ħ ω_d / 2π) * (δV / V_char)^2 * χ(ω_d) susceptibility
torque = 1e-20 * (freqs)**1.2 * (delta_V / 0.1)**2 * (1 + 0.5 * np.sin(2*np.pi*freqs/3))

plt.plot(freqs, torque * 1e18, 's-', color='purple')
plt.xlabel('Frequenza Floquet (GHz)')
plt.ylabel(r'$\langle \tau_{vac} \rangle$ (aN·m = 10^{-18} N·m)')
plt.yscale('log')
plt.title('Torque estratto vs freq. Floquet (scaling realistico)')
plt.grid(True)
plt.savefig('fig_torque_floquet_realistic.pdf', dpi=300)
plt.show()