import wrds
import pandas as pd

# Connect to WRDS database 
db = wrds.Connection(wrds_username='your_username', wrds_password='your_password')

# Set the start and end dates for the query
start_date = '1970-06-01'
end_date = '2023-12-31'

# Query data from CRSP, selecting relevant fields
query_msf = f"""
    SELECT permno, cusip, prc, date, cfacpr, cfacshr, ret, shrout, altprc, spread, altprcdt, retx
    FROM crsp.msf
    WHERE date BETWEEN '{start_date}' AND '{end_date}'
"""
# Execute the SQL query
msf = db.raw_sql(query_msf)

# Get stocknames data to find share code
query_stocknames = """
    SELECT permno, shrcd
    FROM crsp.stocknames
"""
stocknames = db.raw_sql(query_stocknames)

# Merge tables on permno column
merged_data = msf.merge(stocknames[['permno', 'shrcd']], on='permno', how='left')

# Filter common stocks (shrcd of 10 or 11)
df_CRSP_msf_1970 = merged_data[merged_data['shrcd'].isin([10, 11])]

# Close the connection
db.close()



# Drop unnecessary columns
df_CRSP_msf_1970.drop(columns=['altprc', 'altprcdt', 'retx','ret','cfacshr','spread','shrout'], inplace=True)

# Filter again to ensure only common stocks remain
filtered_df_CRSP_msf_1970 = df_CRSP_msf_1970[df_CRSP_msf_1970['shrcd'].isin([10, 11])]

# Use .loc to set the values of the PRC column to absolute values
filtered_df_CRSP_msf_1970.loc[:, 'prc'] = filtered_df_CRSP_msf_1970['prc'].abs()

# Drop all rows containing NaN values
filtered_df_CRSP_msf_1970 = filtered_df_CRSP_msf_1970.dropna()

# Add a new column as PRC / CFACPR, and name it adjusted_PRC
filtered_df_CRSP_msf_1970['adjusted_prc'] = filtered_df_CRSP_msf_1970['prc'] / filtered_df_CRSP_msf_1970['cfacpr']
#save 
filtered_df_CRSP_msf_1970.to_csv('TEST_PY_filtered_df_CRSP_msf_1970.csv', index=False)
# Alternative Download CRSP-MSF table directly from WRDS because the Sharecode variable its not exist if using pyhton wrds liabirary 
# My expirment using alternative way 