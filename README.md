# medical_data_analysis
Medical data analysis is done on NHS Dataset
---------------------------------------------------
Here statistical Analysis based on Data Science is done on Health Care Problem
-------------------------------------------------------------- -------------------------------  
We are given medical data from the British NHS on prescription drugs. Since this is real data, it contains many ambiguities that we will need to confront in our analysis. This data set comes from Britain's National Health Service. 

The scripts variable is a list of prescriptions issued by NHS doctors. Each prescription is represented by a dictionary with various data fields: 'practice', 'bnf_code', 'bnf_name', 'quantity', 'items', 'nic', and 'act_cost'.

The practices variable is a list of member medical practices of the NHS. Each practice is represented by a dictionary containing identifying information for the medical practice. Most of the data fields are self-explanatory. Notice the values in the 'code' field of practices match the values in the 'practice' field of scripts.

The data (scripts) contains quantitative data on the number of items dispensed ('items'), the total quantity of item dispensed ('quantity'), the net cost of the ingredients ('nic'), and the actual cost to the patient ('act_cost'). Whenever working with a new data set, it can be useful to calculate summary statistics to develop a feeling for the volume and character of the data. This makes it easier to spot trends and significant features during further stages of analysis.

(1) Calculate the sum, mean, standard deviation, and quartile statistics for each of these quantities. Format your results for each quantity as a list: [sum, mean, standard deviation, 1st quartile, median, 3rd quartile]. Create a tuple with these lists for each quantity as a final result.

(2) How many items of each drug (i.e. 'bnf_name') were prescribed? That is Calculate the total items prescribed for each 'bnf_name'. What is the most commonly prescribed 'bnf_name' in our data? [Hint: Use 'bnf_name' to construct our groups]

(3) Find the total items prescribed in each postal code, representing the results as a list of tuples (post code, total items prescribed). Sort the results in ascending order of alphabetically by post code and take only results from the first 100 post codes. Only include post codes if there is at least one prescription from a practice in that post code. [Hint: Some practices have multiple postal codes associated with them. Use the alphabetically first postal code. Join scripts and practices based on the fact that 'practice' in scripts matches 'code' in practices. However, we must first deal with the repeated values of 'code' in practices. Arrange in alphabetically first postal codes.]

(4) Find the most commonly dispensed item in each postal code, representing the results as a list of tuples (post_code, bnf_name, amount dispensed as proportion of total). Sort your results in ascending order alphabetically by post code and take only results from the first 100 post codes. [Hint: continue to use the joined variable we created before, where we've chosen the alphabetically first postal code for each practice. Additionally, some postal codes have multiple 'bnf_name' with the same number of items prescribed for the maximum. In this case, take the alphabetically first 'bnf_name'.]

(5) Analysis of which drugs have opioid which are harmful

(6) Analysis of Rarely prescribed medicines
