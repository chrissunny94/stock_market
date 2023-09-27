# import pandas as pd
# import os, requests
# from datetime import datetime, date

# #URL from where file can be downloaded.
# nse_symbol_path = 'https://www1.nseindia.com/content/equities/symbolchange.csv'

# r = requests.get(nse_symbol_path) #getting the file.

# r.status_code #to check if the request was successful.

# importing nse from nse tools
from nsetools import Nse

# creating a Nse object
nse = Nse()

# printing Nse object
print(nse)


 
# getting quote of the sbin
quote = nse.get_index_list()

print(quote)