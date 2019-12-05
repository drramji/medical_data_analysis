import matplotlib
import seaborn as sns
import pandas as pd
import numpy as np
import gzip
sns.set()

scripts = pd.read_csv('./dw-data/201701scripts_sample.csv.gz')


col_names=[ 'code', 'name', 'addr_1', 'addr_2', 'borough', 'village', 'post_code']
practices = pd.read_csv('./dw-data/practices.csv.gz', names = col_names)

chem = pd.read_csv('./dw-data/chem.csv.gz')
# chem.head()

# (1) Calculate the sum, mean, standard deviation, and quartile statistics for each of these quantities. Format your results for each quantity as a list: [sum, mean, standard deviation, 1st quartile, median, 3rd quartile]. Create a tuple with these lists for each quantity as a final result.
summary = scripts.describe().transpose()
summary['total'] = summary['count'] * summary['mean']
summary = summary[['total', 'mean','std','25%', '50%', '75%']]
print("\n1. Brief Summary of Medical Data")
print(summary)

# Iterating a table
summary_stats = [ (row[0], row[1:]) for row in summary.itertuples()]

# (2) How many items of each drug (i.e. 'bnf_name') were prescribed? That is Calculate the total items prescribed for each 'bnf_name'. What is the most commonly prescribed 'bnf_name' in our data? [Hint: Use 'bnf_name' to construct our groups]
total = scripts.groupby('bnf_name')['items'].sum()
# print("\nMax Item Total", total.max(), " Len of Total: ", len(total))
most_common_item = [(total.idxmax(), total[total.idxmax()])]
print("\n2. Most Common Item with bnf_name: \n", most_common_item)

# (3) Find the total items prescribed in each postal code, representing the results as a list of tuples (post code, total items prescribed). Sort the results in ascending order of alphabetically by post code and take only results from the first 100 post codes. Only include post codes if there is at least one prescription from a practice in that post code. [Hint: Some practices have multiple postal codes associated with them. Use the alphabetically first postal code. Join scripts and practices based on the fact that 'practice' in scripts matches 'code' in practices. However, we must first deal with the repeated values of 'code' in practices. Arrange in alphabetically first postal codes.]
unique_practices = (practices
                     .sort_values('post_code')
                     .groupby('code')
                     .first()
                     .reset_index())[['code', 'post_code']]

unique_practices.head()

joined = scripts.merge(unique_practices,
               left_on ='practice',
               right_on ='code',
               how ='left')
joined.head()

post_item_totals = (joined.groupby(['post_code','bnf_name'])['items']
                                    .sum()
                                    .reset_index()
                                    .sort_values(['post_code', 'items'], ascending=False))
# print("\n Post_item_totals")
# print(post_item_totals.head())

max_items = post_item_totals.groupby('post_code').first()
# print("max_items Shape: ", max_items.shape)

post_code_totals = post_item_totals.groupby('post_code')['items'].sum()
# print("\nPost_code_totals Shape: ", post_code_totals.shape)
# print("\n Post Code Total: ")
# print(post_code_totals.head())

max_items['post_totals'] = post_code_totals

max_items['proportion'] = max_items['items'] / max_items['post_totals']
max_items.drop(['items','post_totals'], axis=1, inplace=True)
# max_items.head()

items_by_region = list(max_items.itertuples())[:100]
print("\n3. Items Prescribed by Region: \n", items_by_region[:3])

#(4) Drug abuse is a source of human and monetary costs in health care.
# Let's try to find practices that prescribe an unusually high amount of opioids.

opioids = ['morphine', 'oxycodone', 'methadone', 'fentanyl', 'pethidine', 'buprenorphine', 'propoxyphene', 'codeine']

mask= chem.NAME.str.contains('|'.join(opioids), case=False)
opioids_code = chem[mask]['CHEM SUB']


scripts['opioids'] = scripts['bnf_code'].isin(opioids_code).astype(int)

# Find mean of of opioids present practice wise
opioids_per_practice = scripts.groupby('practice')['opioids'].mean()

# print("\n..Opioids_per_practice..\n", opioids_per_practice.head())

relative_opioids_per_practice = opioids_per_practice - scripts['opioids'].mean()
# print("\n relative_opioids_per_practice: ", relative_opioids_per_practice.head())


standard_error_per_practice = np.sqrt(scripts['opioids'].var()/scripts['practice'].value_counts())
opioid_scores = relative_opioids_per_practice / standard_error_per_practice

opioid_scores.head()

unique_practices = (practices
    .sort_values(['code', 'name'])
    .drop_duplicates(subset='code', keep='first'))

unique_practices = unique_practices[['code', 'name']]


results = unique_practices.merge(opioid_scores.rename('score'),
                                left_on='code',
                                right_index = True)

results = results.merge(scripts['practice'].value_counts().rename('count'),
                       left_on = 'code',
                       right_index = True)

results.sort_values(by='score', ascending = False, inplace = True)
results.drop('code', axis=1, inplace = True)

# Frequently opioid prescribing practice
print("\n4. Anomalies: Frequently Opioid prescribing practice......")
print(results.head())

# (5) Growth Rate of Prescription
scripts16 = pd.read_csv('./dw-data/201606scripts_sample.csv.gz')

pct_growth = (scripts.bnf_name.value_counts() - scripts16.bnf_name.value_counts())/scripts16.bnf_name.value_counts()

pct_growth = (scripts.bnf_name.value_counts() - scripts16.bnf_name.value_counts())/scripts16.bnf_name.value_counts()
# pct_growth.head()

script_growth_df = pd.concat([pct_growth, scripts16.bnf_name.value_counts()], axis=1, sort=True)

script_growth_df.columns = ['pct_growth', 'count16']
script_growth_df.dropna(inplace=True)

mask = script_growth_df['count16'] >= 50
script_growth_df = script_growth_df[mask]
# script_growth_df.shape

script_growth_df.sort_values('pct_growth', ascending=False, inplace=True)

script_growth_df = pd.concat([script_growth_df.head(50),
                              script_growth_df.tail(50)])
# script_growth_df.head()
script_growth = list(script_growth_df.itertuples(name=None))

print("\n5. Script Rrowth........ \n", script_growth[:5])



#(6) Does a practice's prescription costs originate from routine care or from reliance on rarely prescribed treatments? Commonplace treatments can carry lower costs than rare treatments because of efficiencies in large-scale production. While some specialist practices can't help but avoid prescribing rare medicines because there are no alternatives, some practices may be prescribing a unnecessary amount of brand-name products when generics are available. Let's identify practices whose costs disproportionately originate from rarely prescribed items.
# First we have to identify which 'bnf_code' are rare. To do this,
# find the probability  𝑝  of a prescription having a particular 'bnf_code'
# We will call a 'bnf_code' rare if it is prescribed at a rate less than  0.1𝑝 .

p = 1 / scripts['bnf_code'].nunique()
# print("probability:", p)

rates = scripts['bnf_code'].value_counts() / len(scripts)
# rates.head()

mask = rates < .1 * p
rare_codes = rates[mask].index.unique()

scripts['rare'] = scripts['bnf_code'].isin(rare_codes)

rare_cost_prop = (scripts[scripts['rare']].groupby('practice')['act_cost'].sum()/scripts.groupby('practice')['act_cost'].sum()).fillna(0)

# rare_cost_prop.head(10)
# Now for each practice, calculate the proportion of costs that originate from prescription of rare treatments (i.e. rare `'bnf_code'`). Use the `'act_cost'` field for this calculation.

relative_rare_cost_prop = (rare_cost_prop
                           - scripts[scripts['rare']]['act_cost'].sum()
                          / scripts['act_cost'].sum())
# relative_rare_cost_prop.head()
standard_error = relative_rare_cost_prop.std()

# unique_practices.head()

unique_practices = (practices
                     .sort_values('name')
                     .groupby('code')
                     .first()
                     .reset_index())[['code', 'name']]

unique_practices.set_index('code', inplace=True)
# unique_practices.head()

rare_scores = (relative_rare_cost_prop / standard_error)
# rare_scores.head()


# Now we will calculate a z-score for each practice based on this proportion.

# rare_scores.head()
# unique_practices.head()
rare_scores = pd.concat([unique_practices, rare_scores], axis = 1, sort=True).sort_values('act_cost', ascending = False).head(100)

rare_scripts = list(rare_scores.itertuples(name=None))
print("\n 6. Rarely Prescribed Scripts : \n", rare_scripts[:5])

print("\n--------------------------END of ANALYSIS--------------------------")
