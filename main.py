from datetime import datetime
import argparse

from scraper import Scraper
import db

parser = argparse.ArgumentParser(
    description='Get match data by league and season')
parser.add_argument('mode', type=int,
                    help='''App modes:
                            1 - Add new data
                            2 - Generates a txt of the current data in db''')
args = parser.parse_args()


def add_new_data():
    options = {
        '1': ['england', 'premier-league'],
        '2': ['italy', 'serie-a'],
        '3': ['germany', 'bundesliga'],
        '4': ['spain', 'laliga'],
        '5': ['france', 'ligue-1'],
    }
    print('''
            Options
        1 - Premier League
        2 - Serie A (Italy)
        3 - Bundesliga
        4 - LaLiga
        5 - Ligue 1''')
    option = input('\nChoose the league: ')
    league = options.get(option, 'null')
    number_of_seasons = int(input('Type the number of previous seasons: '))
    s = Scraper()
    start = datetime.now()
    s.do_scraping(league, number_of_seasons)
    time_elapsed = datetime.now() - start
    print(f'Time elapsed: {time_elapsed}')


def generate_txt():
    db.get_db()


def invalid_mode():
    print('Modes:' +
          '\n1 - Add new data' +
          '\n2 - Generates a txt of the current data in db')


if __name__ == '__main__':
    switch = {
        1: add_new_data,
        2: generate_txt
    }
    case = switch.get(args.mode, invalid_mode)
    case()
