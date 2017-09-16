#!/usr/bin/env python

"""sunviewer.py: Draws a basic chart based on sunfinder.py"""


__author__ = "Steven Campbell AKA Scalextrix"
__copyright__ = "Copyright 2017, Steven Campbell"
__license__ = "The Unlicense"
__version__ = "1.0"


import datetime as dt
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import time
import sqlite3
import sys

userselector = raw_input('Enter a UserID or blank for all users ')
xaxischooser = raw_input('Plot energy against "date" or "blocks"? ')

conn = sqlite3.connect('solardetails.db')
c = conn.cursor()
if userselector == '':
	energyplot = c.execute('select totalmwh FROM SOLARDETAILS').fetchall()
	incenergyplot = c.execute('select incrementmwh FROM SOLARDETAILS').fetchall()
	blocknumber = c.execute('select block FROM SOLARDETAILS').fetchall()
	datetime = c.execute('select period FROM SOLARDETAILS').fetchall()
	longitudes = c.execute('select DISTINCT lon FROM SOLARDETAILS').fetchall()
	latitudes = c.execute('select DISTINCT lat FROM SOLARDETAILS').fetchall()
	conn.close()
else:
	energyplot = c.execute('select totalmwh FROM SOLARDETAILS where dataloggerid="{}"'.format(userselector)).fetchall()
	incenergyplot = c.execute('select incrementmwh FROM SOLARDETAILS where dataloggerid="{}"'.format(userselector)).fetchall()
	blocknumber = c.execute('select block FROM SOLARDETAILS where dataloggerid="{}"'.format(userselector)).fetchall()
	datetime = c.execute('select period FROM SOLARDETAILS where dataloggerid="{}"'.format(userselector)).fetchall()
	longitudes = c.execute('select DISTINCT lon FROM SOLARDETAILS where dataloggerid="{}"'.format(userselector)).fetchall()
	latitudes = c.execute('select DISTINCT lat FROM SOLARDETAILS where dataloggerid="{}"'.format(userselector)).fetchall()
	conn.close()

energyplot = [float(f[0]) for f in energyplot]
incenergyplot = [float(f[0]) for f in incenergyplot]
blocknumber = [int(f[0]) for f in blocknumber]
longitudes = [float(f[0][:-1]) for f in longitudes]
latitudes = [float(f[0][:-1]) for f in latitudes]

if xaxischooser == 'date':
	dates = [a[0][a[0].rfind(';')+1:] for a in datetime]
	date = [dt.datetime.strptime(d,'%Y-%m-%d %H:%M:%S') for d in dates]
	plt.figure(num=1, figsize=(16, 12))
	plt.subplots_adjust(left=0.06, bottom=0.13, right=0.98, top=0.9, wspace=.2, hspace=.6)
	plt.subplot(211)
	plt.title('TOTAL Energy data from ElectriCChain')
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
	plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
	plt.plot(date, energyplot, 'go')
	plt.ylabel('Energy MWh')
	plt.xlabel('Date & Time (UTC)')
	plt.xticks(rotation=45)
	plt.subplot(212)
	plt.title('INCREMENTAL Energy data from ElectriCChain')
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
	plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
	plt.plot(date, incenergyplot, 'ro')
	plt.ylabel('Energy MWh')
	plt.xlabel('Date & Time (UTC)')
	plt.xticks(rotation=45)

elif xaxischooser == 'blocks':
	plt.figure(num=1, figsize=(16, 12))
	plt.subplots_adjust(left=0.06, bottom=0.13, right=0.98, top=0.9, wspace=.2, hspace=.6)
	plt.subplot(211)
	plt.title('TOTAL Energy data from ElectriCChain')
	plt.plot(blocknumber, energyplot, 'go')
	plt.ylabel('Energy MWh')
	plt.xlabel('SolarCoin Blocks')
	plt.xticks(rotation=45)
	plt.subplot(212)
	plt.title('INCREMENTAL Energy data from ElectriCChain')
	plt.bar(blocknumber, incenergyplot, width=10.0, align='center', color='r')
	plt.ylabel('Energy MWh')
	plt.xlabel('SolarCoin Blocks')
	plt.xticks(rotation=45)
else:
	print 'You must either choose "date" or "blocks", exit in 10 seconds'
	time.sleep(10)
	sys.exit()

plt.figure(num=2, figsize=(10, 8))
earth = Basemap(projection='mill')
earth.drawcoastlines(color='0.50', linewidth=0.25)
earth.fillcontinents(color='0.95')
x,y = earth(longitudes, latitudes)
earth.plot(x,y, 'b*', markersize=3)
plt.show()