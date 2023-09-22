
#importing packages and data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(color_codes=True)
pd.set_option('display.max_columns',None)


for i in range(0, num_rows):
    if num_rows == 1:
        tax_loss = tax_rows
        rate = tax_row['Single Rate'].iloc[i]
        bracket = tax_row['Single Bracket'].iloc[i]
        income = salary_federal - tax_loss
        break

    elif i == num_rows:
        test = 0
    else:
        test = 0

for i in range(0, num_rows):
        if tax_row['Single Rate'].iloc[i] == 0:
            tax_loss = 1
            rate = tax_row['Single Rate'].iloc[i]
            bracket = tax_row['Single Bracket'].iloc[i]
            income = salary_federal - tax_loss
            break
        elif tax_row['Single Rate'].iloc[i] != 0 and num_rows == 1:
            tax_loss = (salary* tax_row['Single Rate'].iloc[i])
            rate = tax_row['Single Rate'].iloc[i]
            bracket = tax_row['Single Bracket'].iloc[i]
            income = salary_federal - tax_loss
            break

        else:
            if (salary - tax_row['Single Bracket'].iloc[i]) > 0 and (salary - tax_row['Single Bracket'].shift(-1).iloc[i]) > 0 and i != num_rows:
                tax_loss = tax_loss + (tax_row['Single Bracket'].shift(-1).iloc[i]* tax_row['Single Rate'].iloc[i])
                rate = tax_row['Single Rate'].iloc[i]
                bracket = tax_row['Single Bracket'].iloc[i]
                income = salary_federal - tax_loss
            
            elif (salary - tax_row['Single Bracket'].iloc[i]) > 0 and (salary - tax_row['Single Bracket'].shift(-1).iloc[i]) < 0 and i != num_rows:
                tax_loss = tax_loss + ((salary - tax_row['Single Bracket'].shift(+1).iloc[i]) * tax_row['Single Rate'].iloc[i])
                bracket = tax_row['Single Bracket'].iloc[i]
                rate = tax_row['Single Rate'].iloc[i]
                income = salary_federal - tax_loss
                break
            
            elif (salary - tax_row['Single Bracket'].iloc[i]) < 0 and num_rows != 1:
                tax_loss = tax_loss + ((salary - tax_row['Single Bracket'].shift(+1).iloc[i]) * tax_row['Single Rate'].iloc[i])
                rate = tax_row['Single Rate'].iloc[i]
                bracket = tax_row['Single Bracket'].iloc[i]
                income = salary_federal - tax_loss
                break
            
            elif (salary - tax_row['Single Bracket'].iloc[i]) > 0 and i == num_rows:
                tax_loss = tax_loss + (tax_row['Single Bracket'].shift(-1).iloc[i]* tax_row['Single Rate'].iloc[i])
                rate = tax_row['Single Rate'].iloc[i]
                bracket = tax_row['Single Bracket'].iloc[i]
                income = salary_federal - tax_loss
                break
