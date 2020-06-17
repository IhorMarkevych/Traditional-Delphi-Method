from statsmodels.multivariate.manova import MANOVA
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

data = pd.read_excel('./Data/secondRound.xlsx', sheet_name='Years of experience')
data = data.loc[1:23, ["Job role", "Experts' area"]]
data = np.asarray(data)

responses = pd.read_excel('./Data/secondRound.xlsx', sheet_name='Survey Round 2 Responses')

qs = [x for x in responses.columns[1:] if not 'Experts confidence' in x and not 'Estimation of probability' in x]

table = []
for q in qs:
    res = np.asarray(responses.loc[:,q]).reshape(-1, 1)

    enc = LabelEncoder()
    data_job = enc.fit_transform(data[:, 0]).reshape(-1, 1)
    data_area = enc.fit_transform(data[:, 1]).reshape(-1, 1)
    res = enc.fit_transform(res).reshape(-1, 1)
    dep = pd.DataFrame(np.concatenate([data_job, data_area, res], axis=1), columns=['Job', 'Area', 'Res'])
    
    manova = MANOVA.from_formula('Job + Area ~ Res', dep)
    table.append([q, manova.mv_test().results['Res']['stat'].iloc[0,4]])

print(pd.DataFrame(table, columns=['Question', 'p-value']))