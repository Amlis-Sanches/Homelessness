#importing packages and data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import seaborn as sns
import tax_and_salary as tas
sns.set_theme(color_codes=True)
pd.set_option('display.max_columns',None)

#importing the data gathered from different websites and goverment documents. I also create an empty data frame
#file path currently has issues so to fix this issue we use \\. it is also posible to put a r as in df = pd.read_csv(r'C...')
dfindex = pd.read_csv('C:\\Users\\natha\\Documents\\Coding\\Homelessness blog post\\BlogPostPHA\\cost-of-living-index-by-state-[updated-june-2023].csv')
dftaxes = pd.read_csv('C:\\Users\\natha\\Documents\\Coding\\Homelessness blog post\\BlogPostPHA\\State-Individual-Income-Tax-Rates-and-Brackets-2015-2023-fv.csv')
dfwage = pd.read_csv('C:\\Users\\natha\\Documents\\Coding\\Homelessness blog post\\BlogPostPHA\Average-Wage-Per-State.csv')
dfincome = pd.DataFrame(columns=['State','State Rate','Bracket','Income'])


#--------------------------Edit data file to clean the data
#--Edit the Tax data for states
#Remove the unneeded characters from the data set in the tax information. 
charlist = ['$', '%', ',', '"'] #char to remove
rowlist = ['Single Bracket', 'Single Rate'] #rows to remove from
dftaxes = tas.df_remove_chars(dftaxes, rowlist, charlist) #created function to modify and replace dftaxes

dftaxes['Single Bracket'] = pd.to_numeric(dftaxes['Single Bracket'])
#Edit the Single rate to remove string items and make it a numerical value
dftaxes['Single Rate'] = pd.to_numeric(dftaxes['Single Rate'])
dftaxes['Single Rate'] = dftaxes['Single Rate']/100
#Additional eddit
dftaxes = dftaxes.dropna(subset=['State'])

#------------------------------Edit wage data
#Remove string items and make a numerical value
dfwage = tas.df_remove_chars(dfwage, ['Annual Average Wage'], charlist) #second item needs to be a list
dfwage['Annual Average Wage'] = pd.to_numeric(dfwage['Annual Average Wage'])

#estimate the overall cost for someone from a ship and remove federal taxes
ship_cost = 12000000000 #Estimated ship cost from goverment
people = 582462
salary = ship_cost/people
fica = .0765
federal_tax = .1886
salary_federal = salary - (salary * fica) - (salary * federal_tax)

#-------------------------------------------Calculating state specific income
#create a list of all the states
state_list = dftaxes['State'].unique().tolist() #this will review the column names state and find all the unique values. then using tolist it will create a list name state_list

# iterate over each state in the list. Due to complexity of the taxes, mutiple tests needed to be conducted. 
for state in state_list:
    # find the corresponding row in dftaxes for the current state
    tax_row = dftaxes[dftaxes['State'] == state]
    tax_row['Single Bracket'] = pd.to_numeric(tax_row['Single Bracket'])
    tax_row['Single Rate'] = pd.to_numeric(tax_row['Single Rate'])
    
    stateTax, rate, bracket = tas.taxes(tax_row, 'Single Rate', 'Single Bracket', salary_federal)
    income = salary_federal - stateTax
    #input found variables into the dfincome data frame
    dfincome = dfincome._append({'State': state,'State Rate': rate ,'Bracket': bracket, 'Income': income}, ignore_index=True)
dfincome = dfincome.sort_values('Income')
print(dfincome)
#----------------------------------------------calculate the income index for each state compaired to the national average. 
#after reviewing this section i will keep this for further information in the future but it is irrelevent
#dfincome = dfincome[dfincome['State'] != 'District Of Columbia']
#dfindex = dfindex[dfindex['State'] != 'District of Columbia']
dfindex = dfindex.sort_values(by='State')
dfincome = dfincome.sort_values(by='State')
dfwageindex = dfincome[['State', 'Income']]
dfwageindex['wage'] = dfwage['Annual Average Wage']
dfwageindex['Income Index I'] = dfwageindex['Income']/(31133) #average individual income of the united states
dfwageindex['Income Index H'] = dfwageindex['Income']/(61334) #average household incme within the usited states


# Reorganize the data by income from largest to smallest
dfincome.sort_values(by='Income', ascending=False, inplace=True)

#---------------------------- Create a list of states with the max income--------------------------------------------------------#
## Determine the states with the best income after taxes
max_income = dfincome['Income'].max()
max_income_rows = dfincome[dfincome['Income'] == max_income]
states_with_max_income = max_income_rows['State'].tolist()

# Grab the rows in dfindex for each state
df_State_Options = pd.DataFrame()  # Empty DataFrame to store the options

for state in states_with_max_income:
    # Find the rows in dfindex that match the current state
    state_options = dfindex[dfindex['State'] == state]

    # Append the state options to the DataFrame
    df_State_Options = pd.concat([df_State_Options, state_options])
df_State_Options = df_State_Options.sort_values(by='COLindex')
# Now df_State_Options contains the rows from dfindex for the states with the best income

#---------------------------------------------------Determine which states have the lowest index (7 of them)------------------#
#choose 7 since this will match up with the dtates that have the highest income due to no taxes
low_index = dfindex.nsmallest(7, 'COLindex')
low_index_state = low_index['State'].tolist()
df_Low_State_Options = pd.DataFrame()  # Empty DataFrame to store the options
print(df_Low_State_Options)
for state in low_index_state:
    #Find the rows in dfindex that match the current state
    state_options = dfindex[dfindex['State']==state]
    #append the state option to the dataframe
    df_Low_State_Options = pd.concat([df_Low_State_Options,state_options])
df_Low_State_Options = df_Low_State_Options.sort_values(by='COLindex')

print(df_Low_State_Options)

#----------------------------------------------------calculate the decrease for each state choosen---------------------------#
#----------decrease for the list of states that you will get the highest amount of money without the taxes
#implament variables from article on https://worldpopulationreview.com/state-rankings/cost-of-living-index-by-state
anualexpenses = 61334
housingcost = 1748
averagerent = 1154/2
transportation = 9826/2
food = 609.75
utilities = 370.16/2
duelincome = 67521
individualincome = 35805

monthly_expenses = averagerent + food + utilities + (transportation / 12)

df_State_Options['Monthly Expenses'] = (df_State_Options['COLindex'] / 100) * monthly_expenses
df_State_Options['Income'] = max_income

df_budget_state = pd.DataFrame()

for state in states_with_max_income:
    expenses = df_State_Options[df_State_Options['State'] == state]
    expenses['Monthly Expenses'] = pd.to_numeric(expenses['Monthly Expenses'])

    budget = max_income
    num_of_months = 0

    while (budget > 0).any():
        num_of_months += 1
        budget -= expenses['Monthly Expenses']
        new_row = {'Month': num_of_months}
        new_row[state] = budget.item()
        print(new_row)
        df_budget_state = df_budget_state._append(new_row, ignore_index=True)

print(df_budget_state)
#----------------------------------------------------------Plotting--------------------------------------------------------------#
colors = ['black'] #setting color for charts
#----------------plot the income after taxes that are suspected to come out
# Create the plot
plt.figure(figsize=(10, 6))
with sns.axes_style("whitegrid"):
    plt.bar(dfincome['State'], dfincome['Income'])  # Use 'Income' directly as the height values
plt.xlabel('State')
plt.ylabel('Income After Taxes')

#adjust the tick markers on the y-axis
ax = plt.gca()
ax.yaxis.set_major_locator(MultipleLocator(5000))

# Rotate the x-axis labels if needed for better readability
plt.xticks(rotation=90)

# Display the plot
plt.show()

#---------------reorganize index data by the lowest cost of living index in 2023
dfindex.sort_values(by='COLindex', ascending=False, inplace=True)

#plot index data for each state
plt.figure(figsize=(10, 6))
with sns.axes_style("whitegrid"):
    sns.barplot(x='State', y='COLindex', data=dfindex, palette=colors)
plt.xlabel('State')
plt.ylabel('Cost of Living Index')

# Rotate the x-axis labels if needed for better readability
plt.xticks(rotation=90)
plt.show()

#---------------====================Finnal state choices
#---------------Display states with the highest income and there index
#plot index data
plt.figure(figsize=(10, 6))
#sns.set_style(rc = {'axes.facecolor': 'white'})
with sns.axes_style("whitegrid"):
    sns.barplot(x='State', y='COLindex', data=df_State_Options, palette=colors)
plt.xlabel('State')
plt.ylabel('Cost of Living Index')
plt.title('Cost of living index for top options')
# Rotate the x-axis labels if needed for better readability
plt.xticks(rotation=90)

plt.show()

#---------------Display lowest index value for cross analsys
#plot index data
plt.figure(figsize=(10, 6))
#sns.set_style(rc = {'axes.facecolor': 'white'})
with sns.axes_style("whitegrid"):
    sns.barplot(x='State', y='COLindex', data=df_Low_State_Options, palette=colors)
plt.xlabel('State')
plt.ylabel('Cost of Living Index')
plt.title('Cost of living index for top options')
# Rotate the x-axis labels if needed for better readability
plt.xticks(rotation=90)

plt.show()


#---------------Graphing Each budget for the highest income states
# Graphing the states budget over time onto one linechart to show how long you be able to live in that state
#A single plot with four lines, one per measurement type, is obtained with
plt.figure(figsize=(10, 6))

# Replace NaN values with 0
df_budget_state_filled = df_budget_state.copy()
df_budget_state_filled[states_with_max_income] = df_budget_state[states_with_max_income].fillna(0)

for state in states_with_max_income:
    sns.lineplot(x='Month', y=state, data=df_budget_state_filled)

plt.xlabel('Month')
plt.ylabel('Budget')
plt.title('How Long will the budget last in each state')

plt.show()