import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy

CONSENSUS_THRESHOLD = 64

# example of data reading

data = pd.read_excel('./Data/secondRound.xlsx', sheet_name='Survey Round 2 Responses')
data = data.drop(columns='Experts')
data = data.iloc[:, [not 'Experts confidence' in x and not 'Estimation of probability' in x for x in data.columns]]
expImp = pd.read_excel('./Data/secondRound.xlsx', sheet_name='Years of experience')
expImp = expImp.loc[1:23, 'Unnamed: 6']

# -----------------------------------------

def mapToFuzzyNumbers(option):
    '''
    Maps selected option on a Likert scale to fuzzy number.
    
    Arguments:
        `option` - string, selected option.
        Possible values:
            * 'Strongly agree'
            * 'Agree'
            * 'Neutral
            * 'Disagree'
            * 'Strongly disagree'
        Otherwise will fall back to default value which corresponds to "Not answered" and is close to "Strongly disageee".
        
    Returns:
        tuple of three float numbers, fuzzy number that corresponds to selected option.
    '''
    
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

def distance(m, n):
    '''
    Fuzzy distance between three numbers
    
    Arguments:
        `m`, `n` - tuples or lists of three elements that corresponds to two fuzzy numbers.
        
    Returns:
        float, fuzzy distance between given numbers.
    '''
    
    return (((m[0] - n[0]) ** 2 
            + (m[1] - n[1]) ** 2 
            + (m[2] - n[2]) ** 2) / 3)  ** 0.5
             
def average(d):
    return [sum(x) / len(x) for x in zip(*d)]

def defuzzify(x, averageMethod):
    '''
    Implements average defuzzification method - weighted and simple average.
    
    Arguments:
        `x` - fuzzy number to be defuzzified, tuple or list of three elements;
        `averageMethod` - string, selected method. Can be 'weighted' for weighted average or 'average' for simple average.
        
    Returns:
        float, defuzzified value.
    
    '''
    
    if averageMethod == 'weighted':
        return (x[0] + 2 * x[1] + x[2]) / 4
    if averageMethod == 'average':    
        return (x[0] + x[1] + x[2]) / 3
    
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
def defuzzifyCOA(x):
    '''
    Implements Center of Area defuzzification method for triangular membership function.
    
    Arguments:
        `x` - fuzzy number to be defuzzified, tuple or list of three elements.
        
    Returns:
        float, defuzzified value.
    '''

    return skfuzzy.defuzzify.defuzz(np.array([i for i in np.arange(0, 1, 0.001)]), 
                                    np.array([memb(i, x) for i in np.arange(0, 1, 0.001)]), 
                                    'centroid')
    
def delphiMethod(data, question, defuzzifyMethod='average', averageMethod='weighted'):
    '''
    Traditional Delphi method implementation.
    
    Arguments:
        `data` - pandas dataframe with collected responses, each column corresponds to question, each row to expert;
        `question` - string, column name in `data`. Delphi method will be evaluated at given column;
        `defuzzifyMethod` - string, defuzzification method. Can be 'average' for average (weighted or simple) or 'COA' for Center of Area;
        `averageMethod` - string, if `defuzzifyMethod` is `average` specifies whether to use weighted average ('weighted') or simple average ('average').
        
    Returns:
        (rank, cons, verdict) - tuple of three elements, where
            `rank` - float, obtained defuzzified rank;
            cons - float, obtained consensus rate;
            `verdict` - string, 'Retained'/'Discarded', whether question should be retained or discarded based on consensus and `CONSENSUS_THRESHOLD` variable.
        
    '''
    subData = data[question]
    k = len(subData)
    mappedData = subData.apply(mapToFuzzyNumbers)
    aver = average(mappedData)
    if defuzzifyMethod == 'COA':
        rank = defuzzifyCOA(np.array(aver))
    else:
        rank = defuzzify(aver, averageMethod)
    def distanceToAver(x):
        return distance(x, aver)
    
    distances = mappedData.apply(distanceToAver)
    cons = sum(distances < 0.2) / k * 100
    
    if cons >= CONSENSUS_THRESHOLD:
        verdict = 'Retained'
    else:
        verdict = 'Discarded'
    
    return rank, cons, verdict

# -------------------------
# -------------------------

# calculate and display obtained results

ranking = pd.DataFrame(columns=['Name', 'Rank', 'Consensus', 'Verdict'])
for col in data.columns: 
    res = delphiMethod(data, col, 'weighted') #'weighted' or 'average'
    ranking.loc[len(ranking)] = [col, res[0], res[1], res[2]]
    
ranking = ranking.sort_values(by=['Rank'], ascending=False)
ranking = ranking.set_index('Name')

display(ranking)

# display barchart of obtained rankings

ranking[['Rank']].plot.bar()
plt.title('Rank')
plt.show()

# display barchart of obtained consensus rates with CONSENSUS_THRESHOLD horizontal line.

line = ranking[['Consensus']]
for col in line.columns:
    line[col].values[:] = CONSENSUS_THRESHOLD
    
fig, ax = plt.subplots(1, 1)
ranking[['Consensus']].plot.bar(ax=ax)
line.plot.line(ax=ax)
plt.title('Consensus')
plt.show()

# save results to csv

ranking.to_csv('trad_res.csv')