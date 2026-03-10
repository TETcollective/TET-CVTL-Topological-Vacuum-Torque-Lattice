# =============================================================================
# Genera coordinate TikZ o file .dat per fasi wrapped 2π k / φ
# File: code/generate_tikz_phases.py
# =============================================================================

import numpy as np

phi = (1 + np.sqrt(5)) / 2
max_k = 200  # puoi aumentare

def wrapped_phase(k):
    raw = 2 * np.pi * k / phi
    return ((raw + np.pi) % (2 * np.pi)) - np.pi

print(f"% Coordinate TikZ per fasi wrapped (k=1..{max_k})")
print("coordinates {")
for k in range(1, max_k + 1):
    wp = wrapped_phase(k)
    print(f"({k}, {wp:.6f})")
print("};")

# Opzionale: salva in file .dat per \addplot file
with open('code/phases_wrapped.dat', 'w') as f:
    f.write("% k wrapped_phase\n")
    for k in range(1, max_k + 1):
        wp = wrapped_phase(k)
        f.write(f"{k} {wp:.6f}\n")
print("File 'code/phases_wrapped.dat' creato per TikZ.")