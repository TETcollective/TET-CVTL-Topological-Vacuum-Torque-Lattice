# Title: Generate LaTeX Table from Multi-Run CSV Results for TET-CVTL Paper
# Description: Reads CSV from multi-runs, computes stats, outputs LaTeX table snippet.
# Run after multi-simulations.
# Author: Grok 4 (xAI) - Generated for @PhysSoliman
# Date: March 02, 2026

import pandas as pd

models = ['base', 'N6', 'honeycomb', 'lindblad']
data = {}

for model in models:
    df = pd.read_csv(f'results_{model}_multi.csv')
    mean = df['Integrated_Torque'].mean()
    std = df['Integrated_Torque'].std()
    data[model] = (mean, std)

# Print LaTeX table
print(r'\begin{table}[H]]')
print(r'\centering')
print(r'\caption{Statistiche multi-run del torque integrato.}')
print(r'\label{tab:multi-torque-stats}')
print(r'\begin{tabular}{lcc}')
print(r'\toprule')
print(r'Modello & Mean Torque & Std Dev \\')
print(r'\midrule')
for model, (mean, std) in data.items():
    print(f'{model.capitalize()} & {mean:.4f} & {std:.4f} \\\\')
print(r'\bottomrule')
print(r'\end{tabular}')
print(r'\end{table}')