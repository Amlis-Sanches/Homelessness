import pandas as pd
import numpy as np

# Create a DataFrame with your data
data = {
    'Month': [0, 1, 2, 3, 4, 5, 6, 7],
    'Wyoming': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 1.0, 2.0],
    'Florida': [13451.088382, 10710.942568, 7970.796755, 5230.650942, 2490.505128,
                -249.640685, 13170.577765, 10149.921335],
    'New Hampshire': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    'Nevada': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
}

df = pd.DataFrame(data)

# Forward fill NaN values with previous non-null values
df.ffill(inplace=True)

# Remove rows with NaN values
df.dropna(inplace=True)

# Reset the index
df.reset_index(drop=True, inplace=True)

print(df)