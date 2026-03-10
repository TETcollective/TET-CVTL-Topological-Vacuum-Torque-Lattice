# Title: Generatore di Report per Paper da Dati CSV in TET-CVTL

#generate_paper_report.py

# Description: Compila tutti i CSV (multi-run, negativity, ecc.) in tabelle LaTeX aggregate e figure combinate.
# Outputta snippet LaTeX per tabelle e matplotlib per multi-plot.
# Author: Grok 4 (xAI) - Generated for @PhysSoliman
# Date: March 02, 2026

import pandas as pd
import matplotlib.pyplot as plt

# Lista CSV da aggregare (aggiungi i tuoi)
csv_files = ['floquet_negativity_data.csv', 'floquet_multi_results.csv', 'floquet_lindblad_data.csv', 'honeycomb_scaling_data.csv']

stats = {}
for file in csv_files:
    df = pd.read_csv(file)
    if 'Integrated_Torque' in df.columns:
        mean = df['Integrated_Torque'].mean()
        std = df['Integrated_Torque'].std()
        stats[file] = (mean, std)

# Stampa LaTeX tabella aggregata
print(r'\begin{table}[htbp]')
print(r'\centering')
print(r'\caption{Aggregate Stats da Simulazioni TET--CVTL}')
print(r'\begin{tabular}{lcc}')
print(r'\toprule')
print(r'File & Mean Torque & Std \\')
for file, (mean, std) in stats.items():
    print(f'{file} & {mean:.4f} & {std:.4f} \\\\')
print(r'\bottomrule')
print(r'\end{tabular}')
print(r'\end{table}')

# Esempio multi-plot (torque da vari file)
fig, ax = plt.subplots(figsize=(12,8))
for file in csv_files:
    df = pd.read_csv(file)
    if 'torque' in df.columns and 'time' in df.columns:
        ax.plot(df['time'], df['torque'], label=file)
ax.set_xlabel('Time')
ax.set_ylabel('Torque')
ax.set_title('Aggregate Torque da Vari Modelli')
ax.legend()
plt.savefig('aggregate_torque_plot.png')
plt.show()