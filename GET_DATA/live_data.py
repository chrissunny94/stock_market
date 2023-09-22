from jugaad_data.nse import NSELive 
from jugaad_data.holidays import holidays

print(holidays(year=2023,month=None))



n = NSELive()
import pprint
# pp = pprint.PrettyPrinter(width=41, compact=True)
# for i in range(10):
#     q = n.stock_quote("HDFCBANK")
#     pp.pprint(q['priceInfo'])
