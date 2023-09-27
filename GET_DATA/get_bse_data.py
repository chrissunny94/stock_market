from bsedata.bse import BSE
import pprint
pp = pprint.PrettyPrinter(width=20, compact=True)

b = BSE(update_codes = True)


    

list_of_all_companies =(b.getScripCodes())
print(len(list_of_all_companies))
for company in list_of_all_companies:
    print(company)
    comapany_quote = b.getQuote(company)
    print(comapany_quote['companyName'])
    print(comapany_quote['marketCapFull'])
    print(comapany_quote['pChange'])
