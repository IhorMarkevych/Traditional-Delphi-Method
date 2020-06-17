import scipy.stats
import pandas as pd

r1 = pd.read_csv('round1Data.csv') # read round 1 results (in a format that CAM script generates)
r2 = pd.read_csv('round2Data.csv') # read round 2 results (in a format that CAM script generates)

r1 = r1.loc[r1.Name.isin(r2.Name), :] # subset only questions that are included in round 2(some question from round 1 are dropped during questionary review after obtaining results)

print('Tests for consensus convergence:')
print('----------------------')
print()

print('Mann-Whitney test:')
mwc = scipy.stats.mannwhitneyu(r1.Consensus, r2.Consensus, alternative='two-sided')
print(f'Statistic value is {mwc.statistic}')
print(f'p-value is {mwc.pvalue}')
if mwc.pvalue < 0.05:
    print('Null hypothesis rejected!')
else:
    print('Null hypothesis is NOT rejected!')
print()

print('Median test:')
mc = scipy.stats.median_test(r1.Consensus, r2.Consensus)
print(f'Statistic value is {mc[0]}')
print(f'p-value is {mc[1]}')
if mc[1] < 0.05:
    print('Null hypothesis rejected!')
else:
    print('Null hypothesis is NOT rejected!')
print()

print('Kruskal-Wallis test:')
kwc = scipy.stats.kruskal(r1.Consensus, r2.Consensus)
print(f'Statistic value is {kwc.statistic}')
print(f'p-value is {kwc.pvalue}')
if kwc.pvalue < 0.05:
    print('Null hypothesis rejected!')
else:
    print('Null hypothesis is NOT rejected!')
print()

print()
print()
print()

print('Tests for rank convergence:')
print('----------------------')
print()

print('Mann-Whitney test:')
mwr = scipy.stats.mannwhitneyu(r1.Rank, r2.Rank, alternative='two-sided')
print(f'Statistic value is {mwr.statistic}')
print(f'p-value is {mwr.pvalue}')
if mwr.pvalue < 0.05:
    print('Null hypothesis rejected!')
else:
    print('Null hypothesis is NOT rejected!')
print()

print('Median test:')
mr = scipy.stats.median_test(r1.Rank, r2.Rank)
print(f'Statistic value is {mr[0]}')
print(f'p-value is {mr[1]}')
if mr[1] < 0.05:
    print('Null hypothesis rejected!')
else:
    print('Null hypothesis is NOT rejected!')
print()

print('Kruskal-Wallis test:')
kwr = scipy.stats.kruskal(r1.Rank, r2.Rank)
print(f'Statistic value is {kwr.statistic}')
print(f'p-value is {kwr.pvalue}')
if kwr.pvalue < 0.05:
    print('Null hypothesis rejected!')
else:
    print('Null hypothesis is NOT rejected!')
print()
