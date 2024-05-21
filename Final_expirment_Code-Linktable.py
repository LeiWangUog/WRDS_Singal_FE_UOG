import pandas as pd
import numpy as np
import wrds 
#linktable-IBES-CRSP-BETA
# coonect WRDS 数据库
db = wrds.Connection(wrds_username='yourusername', wrds_password='youruserpassword@')
# SQL
query = f"""
    SELECT permno,ticker,ncusip,sdate, edate, score
    FROM wrdsapps.ibcrsphist
    
"""

IBES_CRSP_linktable_beta_df = db.raw_sql(query)


db.close()
#cleaning the NAN
clean_IBES_CRSP_linktable_beta_df =IBES_CRSP_linktable_beta_df.dropna()
clean_IBES_CRSP_linktable_beta_df.drop(['sdate', 'edate', 'SCORE'], axis=1, inplace=True)
#save 
clean_IBES_CRSP_linktable_beta_df = pd.read_csv('clean_IBES_CRSP_linktable_beta_df.csv')
