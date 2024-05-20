import wrds
import pandas as pd

# Connect to WRDS database (ensure you have the correct credentials)
conn = wrds.Connection(wrds_username='your_username', wrds_password='your_password')

# Set the start and end dates for the query
start_date = '1970-06-01'
end_date = '2023-12-31'

# Query data from CRSP, selecting relevant fields
query_msf = f"""
    SELECT permno, cusip, prc, date, cfacpr, cfacshr, ret, vol, bid, ask, shrout, altprc, spread, altprcdt, retx
    FROM crsp.msf
    WHERE date BETWEEN '{start_date}' AND '{end_date}'
"""
# Execute the SQL query
msf = conn.raw_sql(query_msf)

# Get stocknames data to find share code
query_stocknames = """
    SELECT permno, shrcd
    FROM crsp.stocknames
"""
stocknames = conn.raw_sql(query_stocknames)

# Merge tables on permno column
merged_data = msf.merge(stocknames[['permno', 'shrcd']], on='permno', how='left')

# Filter common stocks (shrcd of 10 or 11)
df_CRSP_msf_1970 = merged_data[merged_data['shrcd'].isin([10, 11])]

# Close the connection
conn.close()

# Drop unnecessary columns
df_CRSP_msf_1970.drop(columns=['COMNAM', 'NCUSIP', 'TICKER'], inplace=True)

# Filter again to ensure only common stocks remain
filtered_df_CRSP_msf_1970 = df_CRSP_msf_1970[df_CRSP_msf_1970['shrcd'].isin([10, 11])]

# Use .loc to set the values of the PRC column to absolute values
filtered_df_CRSP_msf_1970.loc[:, 'prc'] = filtered_df_CRSP_msf_1970['prc'].abs()

# Drop all rows containing NaN values
filtered_df_CRSP_msf_1970 = filtered_df_CRSP_msf_1970.dropna()

# Add a new column as PRC / CFACPR, and name it adjusted_PRC
filtered_df_CRSP_msf_1970['adjusted_prc'] = filtered_df_CRSP_msf_1970['prc'] / filtered_df_CRSP_msf_1970['cfacpr']

# Read the final IBES data
final_result = pd.read_csv('filled-merged-IBES-linktable.csv')

# Ensure date formats are consistent
filtered_df_CRSP_msf_1970['date'] = pd.to_datetime(filtered_df_CRSP_msf_1970['date']).dt.to_period('M')
final_result['month_end'] = pd.to_datetime(final_result['month_end']).dt.to_period('M')

# Convert PERMNO column to integers
filtered_df_CRSP_msf_1970['permno'] = filtered_df_CRSP_msf_1970['permno'].astype(int)
final_result['permno'] = final_result['permno'].astype(int)

# Merge the two DataFrames
merged_df = pd.merge(
    final_result,
    filtered_df_CRSP_msf_1970,
    how='inner',
    left_on=['permno', 'cusip', 'month_end'],
    right_on=['permno', 'cusip', 'date']
)

# Calculate Forecast_error
merged_df['Forecast_error'] = (merged_df['value'] - merged_df['adjusted_prc']) / merged_df['adjusted_prc']
merged_df.to_csv('2024_05_17_orginal_merged_df.csv', index=False)

# Read the merged data
merged_df = pd.read_csv('2024_05_17_orginal_merged_df.csv')

# Create a copy of the DataFrame for 99% confidence interval adjustment
merged_df_copy_CI99 = merged_df.copy()

# Calculate the 1% and 99% percentiles
lower_percentile = merged_df_copy_CI99['Forecast_error'].quantile(0.01)
upper_percentile = merged_df_copy_CI99['Forecast_error'].quantile(0.99)

# Calculate and create the new Adjusted_Forecast_error column
merged_df_copy_CI99['Adjusted_Forecast_error_CI'] = merged_df_copy_CI99['Forecast_error'].apply(
    lambda x: lower_percentile if x < lower_percentile else (upper_percentile if x > upper_percentile else x)
)

# Save the processed data
merged_df_copy_CI99.to_csv('2024_05_16_adjusted_merged_df.csv', index=False)


# Plot the frequency distribution of Adjusted_Forecast_error
import matplotlib.pyplot as plt

# Plot the frequency distribution
plt.figure(figsize=(10, 6))
plt.hist(merged_df_copy_CI99['Adjusted_Forecast_error_CI'], bins=50, edgecolor='k', alpha=0.7)
plt.title('Frequency Distribution of Adjusted_Forecast_error_CI')
plt.xlabel('Adjusted_Forecast_error_CI')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# Ensure date columns are converted to datetime format
merged_df_copy_CI99['month_end'] = pd.to_datetime(merged_df_copy_CI99['month_end'])

# Create a unique identifier for each company
merged_df_copy_CI99['company_id'] = merged_df_copy_CI99['cusip'] + '-' + merged_df_copy_CI99['permno'].astype(str) + '-' + merged_df_copy_CI99['ibes_ticker']

# Drop rows with NA values
merged_df_copy = merged_df_copy_CI99.dropna()

# Calculate the average FE value for each company each month
consensus_df = merged_df_copy.groupby(['company_id', 'month_end'])['Adjusted_Forecast_error_CI'].mean().reset_index()

# Create the signal matrix
signal_matrix_CI = consensus_df.pivot(index='company_id', columns='month_end', values='Adjusted_Forecast_error_CI')
signal_matrix_CI.to_csv('signal_matrix_CI.csv')

# Read the signal matrix
signal_matrix_CI = pd.read_csv('signal_matrix_CI.csv', index_col=0)

# Ensure columns are in datetime format
signal_matrix_CI.columns = pd.to_datetime(signal_matrix_CI.columns)

# Transpose the matrix so companies are columns and time is rows
transposed_signal_matrix = signal_matrix_CI.T

# Select specific companies
selected_companies = ['03783310-14593-AAPL', '02079K30-90319-GOOG', '02079K10-14542-GOOG/1', '88160R10-93436-TSLA', '00790310-61241-AMD','00036020-76868-AAON','61688010-48071-JPM']  # Ensure these values exist in your company_id

# Filter the data for selected companies
filtered_matrix = transposed_signal_matrix[selected_companies]

# Plot the time series of average FE for selected companies
plt.figure(figsize=(15, 10))

for company in filtered_matrix.columns:
    plt.plot(filtered_matrix.index, filtered_matrix[company], label=company)

# Set the x-axis format to year
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.YearLocator())

plt.title('Time Series of Average FE for Selected Companies')
plt.xlabel('Year')
plt.ylabel('Average FE')
plt.legend(title='Company')
plt.xticks(rotation=45)
plt.show()
