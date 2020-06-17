import pandas as pd
import matplotlib.pyplot as plt


CONSENSUS_THRESHOLD = 64

data = pd.read_excel('./Data/secondRound.xlsx', sheet_name='Survey Round 2 Responses')
data = data.drop(columns='Experts')
data = data.iloc[:, [not 'Experts confidence' in x and not 'Estimation of probability' in x for x in data.columns]]
expImp = pd.read_excel('./Data/secondRound.xlsx', sheet_name='Years of experience')
expImp = expImp.loc[1:23, 'Unnamed: 6']

def mapToFuzzyNumbers(option):
    if option == 'Strongly agree':
        return (0.6, 0.8, 1.0)
    if option == 'Agree':
        return (0.4, 0.6, 0.8)
    if option == 'Neutral':
        return (0.2, 0.4, 0.6)
    if option == 'Disagree':
        return (0.0, 0.2, 0.4)
    if option == 'Strongly disagree':
        return (0.0, 0.0, 0.2)
    return (0.0, 0.05, 0.1)

def distance(m,n):
    return (((m[0] - n[0]) ** 2 
            + (m[1] - n[1]) ** 2 
            + (m[2] - n[2]) ** 2) / 3)  ** 0.5
             
def average(d):
    return [sum(x) / len(x) for x in zip(*d)]

def distanceToAver(x):
    return distance(x, aver)

def defuziffy(x, averageMethod):
    if averageMethod == 'weighted':
        return (x[0] + 2 * x[1] + x[2]) / 4
    if averageMethod == 'average':    
        return (x[0] + x[1] + x[2]) / 3
    
import skfuzzy

def memb(x, R):
    '''
    Triangular membership function.
    
    Arguments:
    `x` - point at which membership function is to be evaluated;
    `R` - fuzzy number, tuple of three floats.
    
    Return:
    float number that coresponds to membership function value of fuzzy number `R` at point `x`.
    '''
    a, b, c = R
    if x < a or x > c:
        return 0
    if x < b and x >= a:
        return (x - a) / (b - a)
    if x <= c and x >= b:
        return (b + c - b - x) / (c - b) 
    
# https://pythonhosted.org/scikit-fuzzy/api/skfuzzy.defuzzify.html
def defuziffyCOA(x):
    return skfuzzy.defuzzify.defuzz(np.array([i for i in np.arange(0, 1, 0.001)]), 
                                    np.array([memb(i, x) for i in np.arange(0, 1, 0.001)]), 
                                    'centroid')
    
import numpy as np
def delphiMethod(question, averageMethod='weighted'):
    subData = data[question]
    k = len(subData)
    mappedData = subData.apply(mapToFuzzyNumbers)
    aver = average(mappedData)
#     rank = defuziffy(aver, averageMethod)
    rank = defuziffyCOA(np.array(aver))
    def distanceToAver(x):
        return distance(x, aver)
    
    distances = mappedData.apply(distanceToAver)
    cons = sum(distances < 0.2) / k * 100
    
    if cons >= CONSENSUS_THRESHOLD:
        verdict = 'Retained'
    else:
        verdict = 'Discarded'
    
    return rank, cons, verdict


ranking = pd.DataFrame(columns=['Name', 'Rank', 'Consensus', 'Verdict'])
for col in data.columns: 
    res = delphiMethod(col, 'weighted') #'weighted' or 'average'
    ranking.loc[len(ranking)] = [col, res[0], res[1], res[2]]
    
ranking = ranking.sort_values(by=['Rank'], ascending=False)
ranking = ranking.set_index('Name')

display(ranking)

ranking[['Rank']].plot.bar()
plt.show()

line = ranking[['Consensus']]
for col in line.columns:
    line[col].values[:] = CONSENSUS_THRESHOLD
    
fig, ax = plt.subplots(1, 1)
ranking[['Consensus']].plot.bar(ax=ax)
line.plot.line(ax=ax)
plt.show()

ranking.to_csv('trad_res.csv')