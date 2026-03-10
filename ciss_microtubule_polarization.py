"""
Toy model trasferimento polarizzazione spin via CISS in microtubuli
(compatibile RENASCENT-Q embodied layer)

Autore: Simon Soliman (tetcollective.org)
Data: Marzo 2026
"""

import numpy as np
import matplotlib.pyplot as plt

eta_ciss = np.linspace(0.1, 0.9, 50)     # efficienza CISS
n_steps = 100                            # passi trasporto carica
p_initial = 0.05                         # polarizzazione iniziale

# Decadimento esponenziale modificato da CISS
p_final = p_initial * np.exp(-n_steps / (5 + 20 * eta_ciss**2))

plt.figure(figsize=(8,5))
plt.plot(eta_ciss, p_final, 'darkgreen', lw=2.5)
plt.xlabel(r'Efficienza CISS $\eta$')
plt.ylabel(r'Polarizzazione residua dopo 100 passi')
plt.title('Amplificazione coerenza via CISS nei microtubuli')
plt.axhline(0.01, color='gray', ls='--', label='soglia decoerenza termica')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('ciss_polarization_transfer.png', dpi=180)
plt.show()