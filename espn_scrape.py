from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import bs4
import csv

browser = webdriver.Firefox()
browser.get('https://fantasy.espn.com/basketball/playerrater')
sleep(3)
page_count = int(bs4.BeautifulSoup(browser.page_source, "lxml").select('a.PaginationNav__list__item__link.flex.justify-center.items-center')[-1].text)

more_pages = True
with open('espn_positions.csv', mode='w') as csv_file:
	csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	for page_ct in range(0, page_count):
		try:
			sleep(5)
			html_source = bs4.BeautifulSoup(browser.page_source, "lxml")
			html_source = html_source.select('table.Table2__right-aligned.Table2__table-fixed.Table2__Table--fixed--left.Table2__table')[0].find('tbody')
			player_groups = html_source.select('div.jsx-1120675750.player-column__bio')

			sleep(5)
			for player in player_groups:
				name = player.select('a.link.clr-link.pointer')[0].text
				positions = player.select('span.playerinfo__playerpos.ttu')[0].text
				positions = [x.strip() for x in positions.split(',')]
				team = player.select('span.playerinfo__playerteam')[0].text
				player_row = [name, team]
				for position in positions:
					player_row.append(position)
				csv_writer.writerow(player_row)
				#print(name, team, positions)

			browser.find_element_by_xpath('//*[@id="espn-analytics"]/div/div[5]/div[2]/div[1]/div/div/div/div[3]/div/div/button[2]').click()

		except:
			more_pages = False
