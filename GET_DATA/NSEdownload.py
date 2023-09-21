from NSEDownload import stocks

# Gets data without adjustment for events
df = stocks.get_data(stock_symbol="RELIANCE", start_date='20-9-2023', end_date='21-9-2023')
print(df)