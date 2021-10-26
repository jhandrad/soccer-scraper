from datetime import datetime
import os
import time

from types import NoneType
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import requests

import db
from my_exceptions import InsertIontoDBError

class Scraper():

    def __init__(self) -> None:
        create_db = not os.path.isfile('matches.db')
        if create_db:
            db.create_db()
        self.error_count = 0

    def log_exceptions(self, code: int, url: str) -> None:
        self.error_count += 1 
        now = datetime.now().strftime('%d/%m/%Y %H:%M')
        scraper_log = open('scraper_log.txt', 'a')
        if code == 1:
            scraper_log.write('%s\n' %(str(self.error_count)+' - '+now+
                                       ': The page does not exist or is not responding\n'+
                                       'match odds on url: '+url+
                                       ', were not entered in database\n'))
        elif code == 2:
            scraper_log.write('%s\n' %(str(self.error_count)+' - '+now+
                                       ': The match does not have odds avaliable'+
                                       ' or they arent in expected format or the page doesnt load on'+
                                       ' the expected time.'+
                                       '\nmatch odds on url: '+url+
                                       ', were not entered in database\n'))
        elif code == 3:
            scraper_log.write('%s\n' %(str(self.error_count)+' - '+now+
                                       ': Page results-soccer can not be reacheble'+
                                       ' or the url is wrong'+
                                       '\nmatchs on url: '+url+
                                       ', were not entered in database\n'))
        elif code == 4:
            scraper_log.write('%s\n' %(str(self.error_count)+' - '+now+
                                       ': Error for insert data on db'+
                                       '\nmatchs on url: '+url+
                                       ', were not entered in database\n'))
        scraper_log.close()

    def get_teams(self, match: str) -> tuple[str, str]:
        #get the names teams in a only one string and return each one individually
        teams = match.split('-')
        return teams[0].strip(), teams[1].strip()

    def get_page_odds(self, url: str):
        #loads the js in details page of each match and return the html of match odds
        firefox_options = Options()
        firefox_options.headless = True
        driver = webdriver.Firefox(
            executable_path=r'C:\Programas\geckodriver.exe', options=firefox_options)
        try:
            driver.get(url)
        except WebDriverException:
            self.log_exceptions(1, url)
            raise WebDriverException
        else:
            time.sleep(5)
            html = driver.page_source
            bs = BeautifulSoup(html, 'html.parser')
            trs = (bs.find('table', id='sortable-1')).tbody.find_all('tr')
            return trs
        finally:
            driver.close()

    def get_page_results(self, url: str):
        try:
            html = requests.get(url)
            bs = BeautifulSoup(html.content, 'html.parser')
            table = bs.find_all('table', class_='table-main js-nrbanner-t')
            tbodies = table[0].find_all('tbody')
        except:
            self.log_exceptions(3, url)
            raise ValueError
        else:
             return tbodies

    def scraping_page_odds(self, url: str):
        dic = {}
        try:
            trs = self.get_page_odds(url)
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

    def do_scraping(self, url: str, num_test: int) -> None:
        cont = 0
        try:
            tbodies = self.get_page_results(url)
        except:
            print('Erro. Talvez o link esteja incorreto')
        else:
            for i in range(len(tbodies)):
                trs = tbodies[i].find_all('tr')
                for j in range(len(trs)):
                    atributos = trs[j].attrs
                    if not('class' in atributos.keys()):
                        tds = trs[j].find_all('td')
                        teams = self.get_teams(tds[0].a.get_text())
                        if (type(tds[2].a) != NoneType and tds[2].a.get_text() not in ['bet365', 'POSTP.']):
                            score = tds[2].a.get_text()
                            try:
                                odds = self.scraping_page_odds(
                                    'https://www.betexplorer.com'+tds[0].a['href'])
                                db.add_match_bd([teams[0], teams[1], score], odds)
                            except InsertIontoDBError:
                                self.log_exceptions(4, 'https://www.betexplorer.com'+tds[0].a['href'])
                            except:
                                self.log_exceptions(2, 'https://www.betexplorer.com'+tds[0].a['href'])
                            finally:
                                cont += 1
                                if (cont == num_test):
                                    raise ValueError
                                continue

    
s1 = Scraper()
s1.do_scraping('https://www.betexplorer.com/results/soccer/', 30)
db.get_bd()
