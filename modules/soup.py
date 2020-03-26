# import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup

# specify the url
quote_page = 'http://dhss.alaska.gov/dph/Epi/id/Pages/COVID-19/monitoring.aspx'

# query the website and return the html to the variable ‘page’
page = urlopen(quote_page)

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')

# Take out the <div> of name and get its value
table = soup.find('table')

rows=list()
for row in table.findAll("tr"):
   rows.append(row)

cols=list()
for col in rows[-1].findAll("td"):
   cols.append(col)


travel = cols[0].text.strip() # strip() is used to remove starting and trailing
local = cols[1].text.strip()
total = cols[-1].text.strip()

print ('Travel: '+travel+' | Local: '+local+' | TOTAL: '+total)

