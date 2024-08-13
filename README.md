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
-  Adjust Forecasts Error Portfilio Performance![AFE-cum return-FF6 ](https://github.com/user-attachments/assets/fde8e1da-8c08-4c32-b327-68ddfd7ecc72)
-  ![Res-FF6-AFE-Cumlative-Return](https://github.com/user-attachments/assets/8ae80f21-4de0-4bbe-856f-a77017576e74)
-  ![5yrsSharpRatio](https://github.com/user-attachments/assets/62a1be97-29fc-487e-8bff-1ce57826bf22)

-  Scaled-disagreement Portfolio Performance

![Res-FF6-SDS-Cumlative-Return](https://github.com/user-attachments/assets/d2e80555-b6c7-49fc-bd08-dcaa87afca50)

![SDS-EW156VW156-5yrSharpRatio](https://github.com/user-attachments/assets/85b21ddc-ad00-4e10-90a6-7ad870a1c1b2)
-  VDS Portfolio Performance
  ![image](https://github.com/user-attachments/assets/f4edacce-27fc-491a-918f-6ab6a3a343f1)
![image](https://github.com/user-attachments/assets/e9d79294-4c74-49ab-a625-a7a4b6cbbb92)
-  Portfolio market cap
![image](https://github.com/user-attachments/assets/f17eb0d4-044b-46b7-9774-e3c40c5fe731)
![image](https://github.com/user-attachments/assets/17b3fa34-b841-4fd2-836b-e572aaf5b662)

  
# Acknowledgments

Special thanks to Dr. Miguel Colburn Herculano for his guidance and support in this project.

# Reference

http://assayinganomalies.com.
Authors: Mihail Velikov velikov@psu.edu & Robert Novy-Marx robert.novy-marx@simon.rochester.edu.
