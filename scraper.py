from datetime import datetime
import os
import time

from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import requests

from my_exceptions import InsertIntoDBError
import db


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
                                        ': The page doesnt load on' +
                                        " the expected time, or the game doesn't have odds_1x2." +
                                        "Verify your internet connection." +
                                        '\nmatch odds_1x2 on url: '+url +
                                        ', were not entered in database\n'))
        elif code == 2:
            scraper_log.write('%s\n' % (str(self.error_count)+' - '+now +
                                        ': Page results-soccer can not be reacheble' +
                                        ' or the url is wrong' +
                                        '\nmatchs on url: '+url +
                                        ', were not entered in database\n'))
        elif code == 3:
            scraper_log.write('%s\n' % (str(self.error_count)+' - '+now +
                                        ': Error for insert data on db' +
                                        '\nmatchs on url: '+url +
                                        ', were not entered in database\n'))
        scraper_log.close()

    def __get_page_details(self, url: str, attempts: int, mode: int, delay: float):
        if attempts == 0:
            raise AttributeError

        firefox_options = Options()
        firefox_options.headless = True
        driver = webdriver.Firefox(
            executable_path='C:\Programas\geckodriver.exe', options=firefox_options,
            timeout=1
        )
        try:
            driver.get(url)
            html = driver.page_source
            bs = BeautifulSoup(html, 'html.parser')
            trs = (bs.find('table', id='sortable-1')).tbody.find_all('tr')
            divs = (bs.find_all('div', id='odds-content')
                    )[0].find_all('div', class_='box-overflow')
            date_instant = self.__format_date_instant(
                bs.find('p', id='match-date').get_text())
        except:
            attempts -= 1
            driver.close()
            print(f'\nYour network might be down. retrying in {delay:.2f}s...')
            time.sleep(delay)
            delay *= 2
            return self.__get_page_details(url, attempts, mode, delay)
        else:
            driver.close()
            if mode == 1:
                return trs, date_instant
            elif mode == 2:
                return divs

    def __get_page_results(self, url: str):
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
            self.__log_exceptions(2, url)
            raise ValueError
        else:
            return trs, championship, season

    def __get_odds_1x2(self, url: str) -> dict:
        dic = {}
        trs, date_instant = self.__get_page_details(
                            url, 10, 1, 0.1)
        for i in range(len(trs)):
            tds = trs[i].find_all('td')
            try:
                dic[tds[0].a.get_text()] = [float(tds[3]['data-odd']), float(tds[4]
                                            ['data-odd']), float(tds[5]['data-odd'])]
            except:
                pass
        return dic, date_instant

    def __get_odds_ou(self, url: str) -> dict:
        dic = {}
        divs = self.__get_page_details(
                            f'{url}#ou', 10, 2, 0.1)
        for i in range(len(divs)):
            trs = (divs[i].table.tbody.find_all('tr'))
            for j in range(len(trs)):
                tds = trs[j].find_all('td')
                try:
                    if tds[0].a.get_text() in dic.keys():
                        dic[tds[0].a.get_text()].append([float(tds[3].get_text()),
                                                        float(
                                                            tds[4]['data-odd']),
                                                        float(tds[5]['data-odd'])])
                    else:
                        dic[tds[0].a.get_text()] = [[float(tds[3].get_text()),
                                                    float(tds[4]['data-odd']),
                                                    float(tds[5]['data-odd'])]]
                except:
                    pass
        return dic

    def __format_round(self, round: str) -> str:
        return int(round.split('.')[0])

    def __format_score(self, score: str) -> tuple:
        s = score.split(':')
        if len(s) > 1:
            if len(s[1].split(' ')) > 1:
                s[1] = s[1].split(' ')[0]
            return (int(s[0]), int(s[1]))
        else:
            return(-1,-1)

    def __format_date_instant(self, dt_instant: str) -> tuple:
        dt = dt_instant.split('-')
        return (dt[0].strip(), dt[1].strip())

    def __aux_url(self, season: str) -> str:
        years = season.split('-')
        if len(years) == 2:
            year_2 = int(years[0])
            year_1 = year_2-1
            return f'{year_1}-{year_2}'
        elif len(years) == 1:
            return f'{int(years[0])-1}'

    def __format_league(self, attrs: tuple) -> str:
        if attrs[0] == 'Serie A':
            return f'{attrs[0]} ({attrs[1].title()})'
        else:
            return attrs[0]

    def match_on_demand(self) -> None:
        team1 = input('team1: ')
        team2 = input('team2: ')
        score1 = int(input('score1: '))
        score2 = int(input('score2: '))
        league = input('league: ')
        season = input('season (ex 2020/2021): ')
        round = int(input('round: '))
        url = input('url: ')
        odds_1x2, date_instant = self.__get_odds_1x2(url)
        odds_ou = self.__get_odds_ou(url)
        db.add_match_db(
            [team1, team2, league, date_instant[0],
            date_instant[1], score1, score2, round, season],
            odds_1x2, odds_ou
        )

    def do_scraping(self, op: list, num_seasons: int, s: str) -> None:
        url = f'https://www.betexplorer.com/soccer/{op[0]}/{op[1]}-{s}/results/'
        if num_seasons <= 0:
            return None
        try:
            trs, championship, season = self.__get_page_results(url)
            round = 0
        except ValueError:
            print(url)
            print('Error. The url might be incorrect')
        else:
            for i in range(len(trs)):
                if len(trs[i].find_all('td')) > 0: 
                    td1 = trs[i].find('td', class_='h-text-left')
                    td2 = trs[i].find('td', class_='h-text-center')
                    spans = td1.a.find_all('span')
                    teams = [spans[x].get_text() for x in range(2)]
                    score = self.__format_score(td2.a.get_text())
                    link = 'https://www.betexplorer.com'+td1.a['href']
                    championship = self.__format_league((championship, op[0]))
                    try:
                        odds_1x2, date_instant = self.__get_odds_1x2(link)
                        odds_ou = self.__get_odds_ou(link)
                        db.add_match_db(
                            [teams[0], teams[1], championship, date_instant[0],
                            date_instant[1], score[0], score[1], round, season],
                            odds_1x2, odds_ou
                        )
                    except InsertIntoDBError:
                        self.__log_exceptions(3, link)
                    except AttributeError:
                        self.__log_exceptions(1, link)
                else:
                    ths = trs[i].find_all('th')
                    round = self.__format_round(ths[0].get_text())

            num_seasons -= 1
            s = self.__aux_url(s)
            return self.do_scraping(op, num_seasons, s)
