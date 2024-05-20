import wrds 
import pandas as pd


# 连接 WRDS 数据库（请确保 `.pgpass` 文件中或环境变量中已有凭证）
db = wrds.Connection(wrds_username='wanglei19970922', wrds_password='Wanglei19970922@')

# 设置查询的起始和结束日期
start_date = '1970-06-01'
end_date = '2023-12-31'

# 查询数据，从 IBES中选择相关字段
query = f"""
    SELECT anndats,ticker,cusip, cname, amaskcd,estimid, alysnam, horizon, value , estcur, curr
    FROM ibes.ptgdet
    WHERE anndats BETWEEN '{start_date}' AND '{end_date}'
"""
# 执行 SQL 查询
data_raw_IBES_ptgdetu = db.raw_sql(query)

# 查看前几行数据
print(data_raw_IBES_ptgdetu.head())

# 关闭连接
db.close()
#Data cleaning - only recored USD
data_raw_IBES_ptgdetu_clean = data_raw_IBES_ptgdetu[(data_raw_IBES_ptgdetu['estcur'] == 'USD') & 
                                   (data_raw_IBES_ptgdetu['curr'] == 'USD')]
#Drop non relavant coulumns 
columns_to_drop = ['estcur', 'curr', 'amaskcd']
data_raw_IBES_ptgdetu_clean = data_raw_IBES_ptgdetu_clean.drop(columns=columns_to_drop)

#Filtering horizon=12 in data_raw_IBES_ptgdetu_clean 

data_raw_IBES_ptgdetu_clean['horizon'] = pd.to_numeric(data_raw_IBES_ptgdetu_clean['horizon'], errors='coerce')
IBES_ptgdetu_clean = data_raw_IBES_ptgdetu_clean[data_raw_IBES_ptgdetu_clean['horizon'] == 12]

#Drop All NAN
IBES_ptgdetu_clean = IBES_ptgdetu_clean.dropna()
#SAVE
IBES_ptgdetu_clean.to_csv('IBES_ptgdetu_clean.csv', index=False)

#read clean_IBES_CRSP_linktable_beta_df
clean_IBES_CRSP_linktable_beta_df = pd.read_csv('clean_IBES_CRSP_linktable_beta_df.csv')

#Merging IBES_ptgdetu_clean and clean_IBES_CRSP_linktable_beta_df

IBES_ptgdetu_clean.rename(columns={'ticker': 'IBES_TICKER'}, inplace=True)
clean_IBES_CRSP_linktable_beta_df.rename(columns={'TICKER': 'IBES_TICKER'}, inplace=True)


# 假设 filtered_df 是左侧数据框，IBES_CRSP_linktable_beta_df_clean 是右侧 Linking Table 数据框
merged_IBES_Linktable = pd.merge(
    IBES_ptgdetu_clean,
    clean_IBES_CRSP_linktable_beta_df,
    how='inner',
    left_on=[ 'cusip', 'IBES_TICKER'],  # filtered_df 中的列
    right_on=[ 'NCUSIP', 'IBES_TICKER'] , # IBES Linking Table 中的列
    suffixes=('_IBES', '_linktable')  # 自定义后缀
)
# Drop NCUSIP
merged_IBES_Linktable.drop(['NCUSIP'], axis=1, inplace=True)
# Save merged_IBES_Linktable
merged_IBES_Linktable.to_csv('merged_IBES_Linktable.csv', index=False).to_csv('merged_IBES_Linktable.csv', index=False)



#filled missing value 


# Read CSV
merged_IBES_Linktable = pd.read_csv('merged_IBES_Linktable')  # Replace with the actual CSV file path
merged_IBES_Linktable.columns = merged_IBES_Linktable.columns.str.lower()

# Convert 'anndats' to datetime and create 'month_end'
merged_IBES_Linktable['anndats'] = pd.to_datetime(merged_IBES_Linktable['anndats'])
merged_IBES_Linktable['month_end'] = merged_IBES_Linktable['anndats'].dt.to_period('M').dt.to_timestamp('M')

def generate_full_date_range(subgroup):
    # Generate full month end period
    full_date_range = pd.date_range(subgroup['month_end'].min(), subgroup['month_end'].max(), freq='M').to_period('M').to_timestamp('M')
    expanded = pd.DataFrame({'month_end': full_date_range})
    for col in ['cusip', 'alysnam', 'estimid', 'permno', 'cname', 'horizon', 'ibes_ticker']:
        expanded[col] = subgroup[col].iloc[0]
    return expanded

def process_batch(group):
    # Compute the latest value of each month in terms of each analyst
    group = group.sort_values(by=['anndats'], ascending=False)
    monthly_forecasts = group.groupby(['cusip', 'alysnam', 'estimid', 'month_end', 'permno', 'cname', 'horizon', 'ibes_ticker']).first().reset_index()

    # Generate the full date range
    full_date_ranges = monthly_forecasts.groupby(['cusip', 'alysnam', 'estimid', 'permno', 'cname', 'horizon', 'ibes_ticker'], as_index=False, group_keys=False).apply(generate_full_date_range).reset_index(drop=True)

    # Merge the latest monthly values into the full date range DataFrame
    full_data = pd.merge(full_date_ranges, monthly_forecasts, on=['cusip', 'alysnam', 'estimid', 'month_end', 'permno', 'cname', 'horizon', 'ibes_ticker'], how='left')

    # Ensure the data is sorted by specific columns for correct forward filling
    full_data.sort_values(by=['cusip', 'alysnam', 'estimid', 'month_end', 'permno', 'cname', 'horizon', 'ibes_ticker'], inplace=True)

    # Apply forward fill to the 'value' column to fill missing values
    full_data['value'] = full_data.groupby(['cusip', 'alysnam', 'estimid', 'permno', 'cname', 'horizon', 'ibes_ticker'])['value'].ffill()

    return full_data[['cusip', 'alysnam', 'estimid', 'month_end', 'permno', 'cname', 'horizon', 'ibes_ticker', 'value']]

# Use unique() function to get all unique combination keys
unique_keys = merged_IBES_Linktable[['cusip', 'ibes_ticker', 'permno']].drop_duplicates()

processed_batches = []

for _, key in unique_keys.iterrows():
    cusip = key['cusip']
    ibes_ticker = key['ibes_ticker']
    permno = key['permno']
    batch = merged_IBES_Linktable[(merged_IBES_Linktable['cusip'] == cusip) &
                                  (merged_IBES_Linktable['ibes_ticker'] == ibes_ticker) &
                                  (merged_IBES_Linktable['permno'] == permno)]
    processed_batch = process_batch(batch)
    processed_batches.append(processed_batch)

# Merge all processed batches into a single DataFrame
final_result = pd.concat(processed_batches, ignore_index=True)

# Save the final result to a CSV file
final_result.to_csv('filled-merged-IBES-linktable.csv', index=False)

