"""
03_ciss_spin_transfer_lindblad.py
Trasferimento coerenza spin da stato anyon-like a stato tubulina
tramite effetto CISS (filtro spin selettivo)
"""

from qutip import *
import numpy as np
import matplotlib.pyplot as plt

# Parametri
g_ciss = 0.12       # coupling CISS (effettivo SOC)
eta = 0.65          # efficienza polarizzazione CISS
gamma_deph = 0.03   # dephasing ambiente
gamma_relax = 0.008

# Operatori (spin anyon → spin tubulina)
sz_anyon = sigmaz()
sz_tub = sigmaz()
sx_anyon = sigmax()
H_int = g_ciss * (sz_anyon * sz_tub)  # Ising-like + chiral bias

# Bias CISS (favorisce spin up)
H_bias = eta * 0.05 * sz_tub
H = H_int + H_bias

# Stato iniziale: anyon con spin entangled
psi0 = tensor(bell_state('00'), basis(2,0))  # esempio entangled

# Collassi
c_ops = [np.sqrt(gamma_deph) * sz_anyon,
         np.sqrt(gamma_deph) * sz_tub,
         np.sqrt(gamma_relax) * sigmam()]

times = np.linspace(0, 80, 400)

result = mesolve(H, psi0, times, c_ops=c_ops,
                 e_ops=[sz_tub, tensor(sigmaz(), sigmaz())])

# Plot polarizzazione tubulina
plt.plot(times, result.expect[0], label='<Sz> tubulina (CISS)')
plt.plot(times, result.expect[1], label='Correlatore ZZ')
plt.xlabel('Tempo')
plt.ylabel('Valore atteso')
plt.title('Trasferimento coerenza spin via CISS')
plt.legend()
plt.grid(True)
plt.show()

print("Polarizzazione finale tubulina:", result.expect[0][-1])