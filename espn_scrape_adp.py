from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import bs4
import csv

browser = webdriver.Firefox()
browser.get('https://fantasy.espn.com/basketball/livedraftresults')
sleep(3)
page_count = int(bs4.BeautifulSoup(browser.page_source, "lxml").select('a.PaginationNav__list__item__link.flex.justify-center.items-center')[-1].text)

more_pages = True
with open('espn_adp.csv', mode='w') as csv_file:
	csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	for page_ct in range(0, page_count):
		#try:
		sleep(5)
		html_source = bs4.BeautifulSoup(browser.page_source, "lxml")
		html_source = html_source.select('table.Table2__table-scroller.Table2__table')[0].find('tbody')
		player_rows = html_source.select('tr.Table2__tr.Table2__tr--sm.Table2__odd')

		sleep(5)
		for player in player_rows:
			name = player.select('a.link.clr-link.pointer')[0].text
			positions = player.select('span.playerinfo__playerpos.ttu')[0].text
			positions = [x.strip() for x in positions.split(',')]
			team = player.select('span.playerinfo__playerteam')[0].text
			adp = player.select('div.jsx-2810852873.table--cell.sortedAscending.adp.tar.sortable')[0].text
			adp_trend = player.select('div.jsx-2810852873.table--cell.sortedAscending.pcadp.tar.sortable')[0].select('span')[0].text
			player_row = [name, team, adp, adp_trend]
			for position in positions:
				player_row.append(position)
			csv_writer.writerow(player_row)
			print(name, team, positions, adp)

		print("Next page!")
		browser.find_element_by_xpath('//*[@id="espn-analytics"]/div/div[5]/div[2]/div[1]/div/div/div/div[3]/div/button[2]').click()

		#except:
		#	more_pages = False
