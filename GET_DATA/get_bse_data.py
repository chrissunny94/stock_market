from bsedata.bse import BSE
import pprint
pp = pprint.PrettyPrinter(width=41, compact=True)

b = BSE()
print(b)
# Output:
# Driver Class for Bombay Stock Exchange (BSE)

# to execute "updateScripCodes" on instantiation
b = BSE(update_codes = True)
q = b.getQuote('534976')
pp.pprint(q)


b = BSE()
codelist = ["500116", "512573"]
for code in codelist:
    quote = b.getQuote(code)
    pp.pprint(quote["companyName"])
    pp.pprint(quote["currentValue"])
    pp.pprint(quote["updatedOn"])
    

his = b.getPeriodTrend('532540','6M')
q = b.getQuote('532540')
pp.pprint(q)