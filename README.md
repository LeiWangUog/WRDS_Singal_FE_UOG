# Singal of Forcast error from 1970-2023
This repository contains the Python code used for connecting to the WRDS database and generating a signal matrix of forecast errors from the IBES and CRSP datasets. The project aims to analyze analyst forecast value, clean it, and produce a long-short factor matrix for asset pricing tests.
# Project Structure
The project is organized into the following folders and scripts:

Final_expirment_Code-CRSP.py: Connects to the WRDS database and retrieves CRSP data.

Final_expirment_Code-IBES.py: Connects to the WRDS database and retrieves IBES data.

Final_expirment_Code-Linktable.py: Handles the linking of CRSP and IBES data using a link table.

Final_expirment_Code-Merging IBES-CRSP.py: Merges the cleaned IBES and CRSP data to produce the final signal matrix.

#Setup
Install Library:
pip install wrds
pip install pandas
pip install numpy
Set up WRDS credentials: Ensure you have access to WRDS. Create a .env file in the root directory of the project with the following content:

WRDS_USERNAME=your_wrds_username

WRDS_PASSWORD=your_wrds_password

# Usage
1.Running the Scripts:

CRSP Data Retrieval:

python Final_expirment_Code-CRSP.py

IBES Data Retrieval:

python Final_expirment_Code-IBES.py

Linking Data:

python Final_expirment_Code-Linktable.py

Merging Data & Analyze signal:

python Final_expirment_Code-Merging\ IBES-CRSP.py

2.Data Cleaning and Analysis:

The scripts are designed to clean the data by handling missing values, removing outliers, and standardizing formats. The final merged dataset will be saved in the project directory.
# Result 
![image](https://github.com/LeiWangUog/WRDS_Singal_FE_UOG/assets/158491057/b6640ac8-d3c5-4426-88fc-863f6d8e0950)

![image](https://github.com/LeiWangUog/WRDS_Singal_FE_UOG/assets/158491057/c6079a0f-42e1-43a2-aaf1-acac395156fc)

# Portfilio Performance
-  Adjust Forecasts Error Portfilio Performance
- [res_10percentile_FE4_equalweight_adjFE(+).fig](res_10percentile_FE4_equalweight_adjFE(+).fig) - MATLAB Fig
- ![image](https://github.com/LeiWangUog/WRDS_Singal_FE_UOG/assets/158491057/f83e2e63-5319-4c10-b03d-d037e80655f5)

-  Scaled-disagreement Portfolio Performance
- ![image](https://github.com/LeiWangUog/WRDS_Singal_FE_UOG/assets/158491057/f70326b8-9a80-4a0d-9ba3-a3de217b9eb9)
- ![image](https://github.com/LeiWangUog/WRDS_Singal_FE_UOG/assets/158491057/dc3f8879-515d-4954-b530-d9c7fba11893)



# Acknowledgments

Special thanks to Dr. Miguel Colburn Herculano for his guidance and support in this project.

# Reference

http://assayinganomalies.com.
Authors: Mihail Velikov velikov@psu.edu & Robert Novy-Marx robert.novy-marx@simon.rochester.edu.
