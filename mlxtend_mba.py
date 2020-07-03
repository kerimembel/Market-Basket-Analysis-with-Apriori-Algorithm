import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori,association_rules
import csv
import os

#Filename of .csv file
filename = 'data\\groceries.csv'

dataset = []
try:
    with open(filename,'r') as csvfile:
        #Read csv file
        reader = csv.reader(csvfile, delimiter=',')
        #Add each row into dataset
        for row in reader: 
            dataset.append(row)
except FileNotFoundError:
    print("\nCouldn't find the .csv file!\n")
    os._exit(1)

#Convert dataframe into transactions array
te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
dataframe = pd.DataFrame(te_ary, columns=te.columns_)
#print(dataframe)
#Run apriori algorithm 
frequent_itemsets = apriori(dataframe, min_support=0.009, use_colnames=True)

#Add length column into dataframe
frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))

#Update itemset to at least two items
updated_freqset = frequent_itemsets[ (frequent_itemsets['length'] >= 2) & (frequent_itemsets['support'] > 0.01)]

#Sort itemset by support value
updated_freqset = updated_freqset.sort_values(by=['support'], ascending=False)

try:
    os.makedirs(os.getcwd() + "//results")
except FileExistsError:
    # directory already exists
    pass

#Write frequent itemsets into a text file
with open("results\\frequent_itemset.txt","w") as file:
        file.write(updated_freqset.to_string())

#Get association rules from frequent itemsets with minimum threshold 0.1
association_rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1) 

#Add antecedent_len column to a association rules
#With this, the user who takes any two items is measured which item they are likely to take.
association_rules["antecedent_len"] = association_rules["antecedents"].apply(lambda x: len(x))

#Update rules by antecedent lenght , confidence and lift values
updated_rules = association_rules[ (association_rules['antecedent_len'] >= 2) &
                                    (association_rules['confidence'] > 0.2) &
                                    (association_rules['lift'] > 1.2) ]

updated_rules = updated_rules.sort_values(by=['support'], ascending=False)

updated_rules = updated_rules.drop(['antecedent support','consequent support'], axis=1)
#Write association rules into a text file
with open("results\\association_rules.txt","w") as file:
        file.write(updated_rules.to_string())


specific_rules = updated_rules[updated_rules['antecedents'] == {"whole milk", "root vegetables"}]

#Write association rules into a text file
with open("results\\specific_rules.txt","w") as file:
        file.write(specific_rules.to_string())

