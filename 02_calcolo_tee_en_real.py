"""
02_calcolo_tee_en_real.py
Calcola TEE e negatività logaritmica E_N manualmente (compatibile QuTiP 5+)
"""

from qutip import *
import numpy as np

# Sostituisci con il tuo stato (gs o result.states[-1])
state = gs

N = 12
subsystem = list(range(N//2))

rho_A = state.ptrace(subsystem)
S_total = entropy_vn(state)
S_A = entropy_vn(rho_A)

tee_proxy = S_A - np.log(2)
print(f"TEE proxy: {tee_proxy:.5f} (ideale: 0.34657)")

# Negatività logaritmica manuale
rho_TA = partial_transpose(rho_A, subsystem, [0])
evals = rho_TA.eigenenergies()
neg_sum = np.sum(np.abs(evals[evals < 0]))
en = np.log2(2 * neg_sum + 1)
print(f"E_N manuale: {en:.5f} (ideale: ≈ 0.5)")