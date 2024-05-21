# Singal of Forcast error from 1970-2023
This repository contains the Python code used for connecting to the WRDS database and generating a signal matrix of forecast errors from the IBES and CRSP datasets. The project aims to analyze analyst forecast value, clean it, and produce a long-short factor matrix for asset pricing tests.
# Project Structure
The project is organized into the following folders and scripts:

Final_expirment_Code-CRSP.py: Connects to the WRDS database and retrieves CRSP data.
Final_expirment_Code-IBES.py: Connects to the WRDS database and retrieves IBES data.
Final_expirment_Code-Linktable.py: Handles the linking of CRSP and IBES data using a link table.
Final_expirment_Code-Merging IBES-CRSP.py: Merges the cleaned IBES and CRSP data to produce the final signal matrix.
