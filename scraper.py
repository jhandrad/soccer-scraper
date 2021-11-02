from datetime import datetime
import os
import time

from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import requests

import db
from my_exceptions import InsertIntoDBError


class Scraper():

    def __init__(self) -> None:
        create_db = not os.path.isfile('matches.db')
        if create_db:
            db.create_db()
        self.error_count = 0

    def __log_exceptions(self, code: int, url: str) -> None:
        self.error_count += 1
        now = datetime.now().strftime('%d/%m/%Y %H:%M')
        scraper_log = open('scraper_log.txt', 'a')
        if code == 1:
            scraper_log.write('%s\n' % (str(self.error_count)+' - '+now +
                                        ': The page does not exist or is not responding\n' +
                                        'match odds on url: '+url +
                                        ', were not entered in database\n'))
        elif code == 2:
            scraper_log.write('%s\n' % (str(self.error_count)+' - '+now +
                                        ': The match does not have odds avaliable' +
                                        ' or they arent in expected format or the page doesnt load on' +
                                        ' the expected time.' +
                                        '\nmatch odds on url: '+url +
                                        ', were not entered in database\n'))
        elif code == 3:
            scraper_log.write('%s\n' % (str(self.error_count)+' - '+now +
                                        ': Page results-soccer can not be reacheble' +
                                        ' or the url is wrong' +
                                        '\nmatchs on url: '+url +
                                        ', were not entered in database\n'))
        elif code == 4:
            scraper_log.write('%s\n' % (str(self.error_count)+' - '+now +
                                        ': Error for insert data on db' +
                                        '\nmatchs on url: '+url +
                                        ', were not entered in database\n'))
        scraper_log.close()

    def __get_page_odds(self, url: str) -> None:
        # loads the js in details page of each match and return the html of match odds
        firefox_options = Options()
        firefox_options.headless = True
        driver = webdriver.Firefox(
            executable_path=r'C:\Programas\geckodriver.exe', options=firefox_options)
        try:
            driver.get(url)
        except WebDriverException:
            self.__log_exceptions(1, url)
            raise WebDriverException
        else:
            time.sleep(5)
            html = driver.page_source
            bs = BeautifulSoup(html, 'html.parser')
            trs = (bs.find('table', id='sortable-1')).tbody.find_all('tr')
            return trs
        finally:
            driver.close()

    def __get_page_results(self, url: str) -> None:
        try:
            html = requests.get(url)
            bs = BeautifulSoup(html.content, 'html.parser')
            table = bs.find(
                'table', class_='table-main js-tablebanner-t js-tablebanner-ntb')
            spans = bs.find('h1').find_all('span')
            championship = spans[1].get_text()
            season = (spans[0].get_text()).split(' ')[-1]
            trs = table.find_all('tr')
        except:
            self.__log_exceptions(3, url)
            raise ValueError
        else:
            return trs, championship, season

    def __scraping_page_odds(self, url: str) -> None:
        dic = {}
        try:
            trs = self.__get_page_odds(url)
        except:
            raise WebDriverException
        else:
            for i in range(len(trs)):
                tds = trs[i].find_all('td')
                for j in range(len(tds)):
                    att = tds[j].attrs
                    if ('data-odd' in att.keys()):
                        dic[tds[0].a.get_text()] = [tds[j]['data-odd'], tds[j+1]
                                                    ['data-odd'], tds[j+2]['data-odd']]
                        break
            return dic

    def do_scraping(self, url: str, num_seasons: int) -> None:
        if num_seasons == 0:
            return None
        try:
            trs, championship, season = self.__get_page_results(url)
        except:
            print('Erro. Talvez o link esteja incorreto')
        else:
            for i in range(len(trs)):
                if len(trs[i].find_all('td')) > 0:
                    td1 = trs[i].find('td', class_='h-text-left')
                    td2 = trs[i].find('td', class_='h-text-center')
                    spans = td1.a.find_all('span')
                    teams = [spans[x].get_text() for x in range(2)]
                    score = td2.a.get_text()
                    try:
                        odds = self.__scraping_page_odds(
                            'https://www.betexplorer.com'+td1.a['href'])
                        db.add_match_db(
                            [championship, season, teams[0], teams[1], score], odds
                        )
                    except InsertIntoDBError:
                        self.__log_exceptions(
                            4, 'https://www.betexplorer.com'+td1.a['href'])
                    except:
                        self.__log_exceptions(
                            2, 'https://www.betexplorer.com'+td1.a['href'])
            num_seasons -= 1
            year1 = int(season.split('/')[0])
            return self.do_scraping('https://www.betexplorer.com/soccer/' +
                                    f'england/premier-league-{str(year1-1)}-{str(year1)}'+
                                    '/results/', num_seasons)


scraper = Scraper()
scraper.do_scraping(
    'https://www.betexplorer.com/soccer/england/premier-league-2020-2021/results/', 1)

