# code/utils.py
import numpy as np

phi = (1 + np.sqrt(5)) / 2

def wrapped_phase(k):
    raw = 2 * np.pi * k / phi
    return ((raw + np.pi) % (2 * np.pi)) - np.pi