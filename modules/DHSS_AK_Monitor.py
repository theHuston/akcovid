# import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
from modules import Location,AKCovid

def connect(monitor_page):

    # query the website and return the html to the variable ‘page’
    page = urlopen(monitor_page)

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')

    # Take out the <div> of name and get its value
    ak_table = soup.find('table')

    locations=list()
    for row in ak_table.findAll("tr")[1:]:
        location = Location.Location(row)
        locations.append(location)


    #Set Statewide Numbers from Footer Row
    total_travel = locations[-1].travel
    total_local = locations[-1].local
    total_overall = locations[-1].total
    total_confirmed = locations[-1].confirmed
    total_pending = locations[-1].pending
    del locations[0] # Delete Header Row from Locations
    del locations[-1] # Delete Footer Row from Locations

    AKCovid.locations = locations
    AKCovid.loc_1 = 0
    AKCovid.loc_2 = 5
    AKCovid.loc_3 = 6
    AKCovid.last_update = '03/25/20'
    AKCovid.ak_total = total_overall
    AKCovid.ak_total_local = total_local
    AKCovid.ak_total_travel = total_travel
    AKCovid.ak_total_confirmed = total_confirmed
    AKCovid.ak_total_pending = total_pending
    #AKCovid.us_total = cells[-1]

    AKCovid.makeScreen()

    #print (locations[1].name+' | Total Travel: '+locations[1].travel+' | Total Local: '+locations[1].local+' | AK TOTAL: '+locations[1].total)
