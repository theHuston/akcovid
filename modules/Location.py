# import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Define location class
class Location:
    def __init__(self, row):

        cols=list()
        for col in row.findAll("td"):
            cols.append(col)


        #print(cols[1].text.strip())
        #print(cols[2].text.strip())
        #print(cols[3].text.strip())
        #print(cols[4].text.strip())
        #print(cols[-1].text.strip())


        name = cols[0].text.strip() [0:15]
        travel = int(cols[1].text.strip().encode('ascii', 'ignore'))
        local = int(cols[2].text.strip().encode('ascii', 'ignore'))
        contact = int(cols[3].text.strip().encode('ascii', 'ignore'))
        pending = int(cols[4].text.strip().encode('ascii', 'ignore'))
        total = int(cols[-1].text.strip().encode('ascii', 'ignore'))

        #print(travel)
        #print(local)
        #print(contact)
        #print(pending)
        #print(total)

        self.name = name
        self.travel = travel
        self.local = local
        self.contact = contact
        self.pending = pending
        self.confirmed = int(travel)+int(local)+int(contact)
        self.total = total


    def getInfo(self):
        print(self.name + " has " + self.travel + " travel related cases.")
        print(self.name + " has " + self.local + " local related cases.")
