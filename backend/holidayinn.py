import pandas as pd
import os, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(os.path.join(BASE_DIR, 'titanic.csv'))

print(df.groupby('Sex')['Survived'].sum())
print(df['Survived'].sum())