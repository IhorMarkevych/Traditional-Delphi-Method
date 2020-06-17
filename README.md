# Delphi method

## Traditional Delphi Method

Implementation of Traditional Fuzzy Delphi Method. This script can be used to aggregate experts opinions on ranking of defined items based on conducted questionary survey. Survey is expected to be a list of questions with next answer options:

* 'Strongly agree'
* 'Agree'
* 'Neutral'
* 'Disagree'
* 'Strongly disagree'

Additionally, each expert should provide information for researcher to define empirical "expert importance" coefficient that would correspond to expert's knowledge and experience in particular research area.

Script generates two numeric values and single boolean value for each item. Next values are generated:

* 'Name' is item name;
* 'Rank' is obtained defuzzified rank of question;
* 'Consensus' is obtained conensus rate;
* 'Verdict' is verdict ("Retained" / "Discarder") based on `CONSENSUS_THRESHOLD` threshold variable.

## Statistical testing to ensure convergence
 
There is second script presented which helps evaluate stability and convergence of obtained group opinions and consensus rates for each item.  
  
Next statistical tests are used:
* Mann-Whitney test;
* Median test;
* Kruskal-Wallis test;

*p-value* of *0.05* is used as a threshold for accepting/rejecting null hypothesis in all tests.
  
Corresponding script can be found in `stats.py`.   

## ANOVA to check for bias in distribution of the group’s responses

The third script that contains ANOVA tests whether the different job roles and place of employment are providing statistically different responses. The null hypothesis states that the perceptions about the relevance of each indicator do not vary as a function of the panelist group and place of employment (this information was gathered via survey together with responses).
  
Corresponding script can be found in `anova.py`.  

# License
MIT

# Authors
[Ihor Markevych](mailto:ih.markevych@gmail.com) and [Egbe-Etu Emmanuel Etu](mailto:fw7443@wayne.edu)
