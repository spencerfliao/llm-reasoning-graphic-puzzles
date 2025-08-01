import numpy as np
from pathlib import Path

tsvs = list(Path('../data/interannotator_agreement').glob('*.tsv'))

data = []
for tsv in tsvs:
    data += np.genfromtxt(tsv, delimiter='\t', skip_header=1, dtype=str)[:, 1:3].flatten().tolist()
data = [int(x) for x in data if x.isdigit()]

print(f'Interannotator Agreement Score: {np.mean(data)}')

