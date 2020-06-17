# Traditional Delphi Method

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
