#importing packages and data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import seaborn as sns
sns.set_theme(color_codes=True)
pd.set_option('display.max_columns',None)

#file path currently has issues so to fix this issue we use \\. it is also posible to put a r as in df = pd.read_csv(r'C...')
dfindex = pd.read_csv('C:\\Users\\natha\\OneDrive\\Documents\\Working Files\\Classes, review, and information\\Python\\Projects\\Cost of living index\\cost-of-living-index-by-state-[updated-june-2023].csv')
dftaxes = pd.read_csv('C:\\Users\\natha\\OneDrive\\Documents\\Working Files\\Classes, review, and information\\Python\\Projects\\Cost of living index\\State-Individual-Income-Tax-Rates-and-Brackets-2015-2023-fv.csv')
dfwage = pd.read_csv('C:\\Users\\natha\\OneDrive\\Documents\\Working Files\\Classes, review, and information\\Python\\Projects\\Cost of living index\\Average-Wage-Per-State.csv')
dfincome = pd.DataFrame(columns=['State','State Rate','Bracket','Income'])

print(dftaxes)

#Edit data file to clean the data
#Edit taxes data for Bracket
dftaxes['Bracket'] = dftaxes['Bracket'].str.replace('$', '')
dftaxes['Bracket'] = dftaxes['Bracket'].str.replace(',', '').str.replace('%','')
dftaxes['Bracket'] = pd.to_numeric(dftaxes['Bracket'])
#Edit taxes data for Rate
dftaxes['Rate'] = dftaxes['Rate'].str.replace('%', '')
dftaxes['Rate'] = pd.to_numeric(dftaxes['Rate'])
dftaxes['Rate'] = dftaxes['Rate']/100
#Edit taxes date to remove states sections filled with nan 
dftaxes = dftaxes.dropna(subset=['State'])

#Edit wage data to remove variables
dfwage['Annual Average Wage'] = dfwage['Annual Average Wage'].str.replace('$', '')
dfwage['Annual Average Wage'] = dfwage['Annual Average Wage'].str.replace(',', '').str.replace('"','')
dfwage['Annual Average Wage'] = pd.to_numeric(dfwage['Annual Average Wage'])

#estimate the overall cost for someone from a ship and remove federal taxes
ship_cost = 12000000000
people = 552830 + (552830*.2)
salary = ship_cost / people
#print('your salary is', salary)
fica = .0765
federal_tax = .0284
salary_federal = salary - (salary * fica) - (salary * federal_tax)

#Calculating state specific income
#create a list of all the states
state_list = dftaxes['State'].unique().tolist() #this will review the column names state and find all the unique values. then using tolist it will create a list name state_list

# iterate over each state in the list
for state in state_list:
    # find the corresponding row in dftaxes for the current state
    tax_row = dftaxes[dftaxes['State'] == state]
    tax_row['Bracket'] = pd.to_numeric(tax_row['Bracket'])
    tax_row['Rate'] = pd.to_numeric(tax_row['Rate'])
    num_rows = tax_row.shape[0]
    tax_loss = 0
    rate = 0
    bracket = 0
    income = 0
    for i in range(0, num_rows):
        if num_rows == 1 and tax_row['Rate'].iloc[i] != 0:
            tax_loss = salary*tax_row['Rate'].iloc[i]
            rate = tax_row['Rate'].iloc[i]
            bracket = tax_row['Bracket'].iloc[i]
            income = salary_federal - tax_loss
            break
            
        elif num_rows == 1 and tax_row['Rate'].iloc[i] == 0:
            #no need for tex_loss equation just make iincome = salary_federal
            rate = tax_row['Rate'].iloc[i]
            bracket = tax_row['Bracket'].iloc[i]
            income = salary_federal
            break

        elif i == num_rows:
            if tax_row['Bracket'].iloc[i] < salary:
                tax_loss = tax_loss + (tax_row['Bracket'].iloc[i]* tax_row['Rate'].iloc[i])
                rate = tax_row['Rate'].iloc[i]
                bracket = tax_row['Bracket'].iloc[i]
                income = salary_federal - tax_loss
                break
            else: 
                tax_loss = tax_loss + ((salary-tax_row['Bracket'].shift(+1).iloc[i])* tax_row['Rate'].iloc[i])
                rate = tax_row['Rate'].iloc[i]
                bracket = tax_row['Bracket'].iloc[i]
                income = salary_federal - tax_loss
                break

        else:
            if tax_row['Bracket'].iloc[i] < salary and tax_row['Bracket'].shift(-1).iloc[i] < salary:
                tax_loss = tax_loss + (tax_row['Bracket'].shift(-1).iloc[i]* tax_row['Rate'].iloc[i])
                rate = tax_row['Rate'].iloc[i]
                bracket = tax_row['Bracket'].iloc[i]

            elif tax_row['Bracket'].iloc[i] < salary and tax_row['Bracket'].shift(-1).iloc[i] > salary:
                tax_loss = tax_loss + ((salary - tax_row['Bracket'].iloc[i])* tax_row['Rate'].iloc[i])
                rate = tax_row['Rate'].iloc[i]
                bracket = tax_row['Bracket'].iloc[i]
                income = salary_federal - tax_loss
                break
            
            else:
                tax_loss = salary*tax_row['Rate'].iloc[i]
                rate = tax_row['Rate'].iloc[i]
                bracket = tax_row['Bracket'].iloc[i]
                income = salary_federal - tax_loss
                break
    #input found variables into the dfincome data frame
    dfincome = dfincome._append({'State': state,'State Rate': rate ,'Bracket': bracket, 'Income': income}, ignore_index=True)
#summary statistics
#print(dfincome.describe())
print(dfincome)

# calculate the income index for each state
dfincome = dfincome[dfincome['State'] != 'District Of Colombia']
dfindex = dfindex[dfindex['state'] != 'District of Columbia']
dfindex = dfindex.sort_values(by='state')
dfincome = dfincome.sort_values(by='State')
dfwageindex = dfincome[['State', 'Income']]
dfwageindex['wage'] = dfwage['Annual Average Wage']
dfwageindex['Income Index I'] = dfwageindex['Income']/(31133) #average individual income of the united states
dfwageindex['Income Index H'] = dfwageindex['Income']/(61334) #average household incme within the usited states
#print(dfwageindex)

# Reorganize the data by income from largest to smallest
dfincome.sort_values(by='Income', ascending=False, inplace=True)

#---------------------------- Determine which state is the best option--------------------------------------------------------#
## Determine the states with the best income after taxes
max_income = dfincome['Income'].max()
max_income_rows = dfincome[dfincome['Income'] == max_income]
states_with_max_income = max_income_rows['State'].tolist()
#print(states_with_max_income)

# Grab the rows in dfindex for each state
df_State_Options = pd.DataFrame()  # Empty DataFrame to store the options

for state in states_with_max_income:
    print(state)
    # Find the rows in dfindex that match the current state
    state_options = dfindex[dfindex['state'] == state]

    # Append the state options to the DataFrame
    df_State_Options = pd.concat([df_State_Options, state_options])

# Now df_State_Options contains the rows from dfindex for the states with the best income
print(df_State_Options)

lowest_col_index = df_State_Options['2023'].min()
lowest_col_index_row = df_State_Options.loc[df_State_Options['2023'] == lowest_col_index]
print(lowest_col_index_row)


#----------------------------------------------------------Plotting--------------------------------------------------------------#
# Create the plot
plt.figure(figsize=(10, 6))
plt.bar(dfincome['State'], dfincome['Income'])  # Use 'Income' directly as the height values
plt.xlabel('State')
plt.ylabel('Income')
plt.title('Income After Taxes')

#adjust the tick markers on the y-axis
ax = plt.gca()
ax.yaxis.set_major_locator(MultipleLocator(5000))

# Rotate the x-axis labels if needed for better readability
plt.xticks(rotation=90)

# Display the plot
plt.show()

#reorganize index data by the lowest cost of living index in 2023
dfindex.sort_values(by='2023', ascending=False, inplace=True)

#plot index data
plt.figure(figsize=(10, 6))
sns.barplot(x='state', y='2023', data=dfindex)

plt.xlabel('sate')
plt.ylabel('Cost of Living Index')
plt.title('Cost of Living Index per State')

# Rotate the x-axis labels if needed for better readability
plt.xticks(rotation=90)

plt.show()

# Income index plot
dfwageindex = dfwageindex.sort_values(by='Income Index I')
sns.lineplot(x='State', y='Income Index I', data=dfwageindex)
#sns.lineplot(x='State', y='Income Index H', data=dfwageindex)

# Add labels and title
plt.xlabel('State')
plt.ylabel('Income Index')
plt.title('Income Compaired to Average Indipendent Income')
plt.xticks(rotation=90)
plt.legend()

# Display the plot
plt.show()
