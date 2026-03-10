# code/plot_bloch_braiding.py
"""
Titolo: Evoluzione sulla sfera di Bloch durante sequenza di braiding anyonico
Descrizione: Simula l'evoluzione di uno stato qubit logico (approssimato)
             durante un'operazione di braiding che accumula una fase topologica
             di e^{i 4π/5} (144°), tipica di anyon Fibonacci.
             La traiettoria mostra l'accumulo di fase geometrica protetta.
Output: fig_bloch_braiding.pdf  (o .png se preferisci)
"""

import qutip as qt
import numpy as np
import matplotlib.pyplot as plt
from qutip.bloch import Bloch

# ────────────────────────────────────────────────
# Parametri fisici
# ────────────────────────────────────────────────
tau_b       = 60.0          # durata totale braiding (ns)
n_points    = 180           # numero di punti per traiettoria fluida
phase_total = 4 * np.pi / 5 # fase topologica target (Fibonacci anyon)

# Frequenza angolare effettiva per raggiungere la fase desiderata
omega = phase_total / tau_b

times = np.linspace(0, tau_b, n_points)

# Hamiltoniano effettivo: rotazione continua intorno asse x
# (approssimazione comune per visualizzare gate di fase topologica)
H = omega * qt.sigmax()

# Stato iniziale: spesso si parte da |+⟩ = (|0⟩ + |1⟩)/√2
# per vedere chiaramente l'accumulo di fase relativa
psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()

# Evoluzione unitaria (senza decoerenza per chiarezza della traiettoria ideale)
result = qt.mesolve(H, psi0, times, c_ops=[], e_ops=[qt.sigmax(), qt.sigmay(), qt.sigmaz()])

# ────────────────────────────────────────────────
# Plot Bloch sphere
# ────────────────────────────────────────────────
b = Bloch(fig=plt.figure(figsize=(7.2, 7.2)))

# Aggiungi traiettoria completa
b.add_points([result.expect[0], result.expect[1], result.expect[2]], meth='s')

# Aggiungi vettore finale (evidenziato)
b.add_vectors([result.expect[0][-1], result.expect[1][-1], result.expect[2][-1]])

# Opzionale: punto iniziale
b.add_points([[result.expect[0][0]], [result.expect[1][0]], [result.expect[2][0]]],
              meth='s') # Removed color, ms, alpha as they are not supported for add_points with meth='s'

b.render() # Removed 'title' argument as it's not supported
plt.title("Evoluzione dello stato qubit logico durante braiding\nFase topologica protetta $e^{i 4\pi/5}$",
          fontsize=13, pad=20)

plt.tight_layout()
plt.savefig("fig_bloch_braiding.pdf", dpi=300, bbox_inches='tight')
# plt.savefig("fig_bloch_braiding.png", dpi=300, bbox_inches='tight')  # alternativa
plt.close()

print("Salvato: fig_bloch_braiding.pdf")