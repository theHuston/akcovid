#!/usr/bin/env python
from modules import DHSS_AK_Monitor, AKCovid, Location
from apscheduler.schedulers.blocking import BlockingScheduler

print("""Inky pHAT AKCovid Display""")
DHSS_AK_Monitor.connect('http://dhss.alaska.gov/dph/Epi/id/Pages/COVID-19/monitoring.aspx')

def update_screen():
    print("Updating Stats")
    DHSS_AK_Monitor.connect('http://dhss.alaska.gov/dph/Epi/id/Pages/COVID-19/monitoring.aspx')

scheduler = BlockingScheduler()
scheduler.add_job(update_screen, 'interval', hours=2)
scheduler.start()
