from datetime import datetime

from scraper import Scraper


def add_new_data() -> None:
    options = {
        1: ['england', 'premier-league'],
        2: ['italy', 'serie-a'],
        3: ['germany', 'bundesliga'],
        4: ['spain', 'laliga'],
        5: ['france', 'ligue-1'],
        6: ['brazil', 'serie-a']
    }
    print('''
             Options
        ==================
        1 - Premier League
        2 - Serie A (Italy)
        3 - Bundesliga
        4 - LaLiga
        5 - Ligue 1
        6 - Série A (Brazil)''')
    while True:
        try:
            option = int(input('\nChoose the league: '))
            season = str(input('Season to start, ex: 2020-2021: '))
            number_of_seasons = int(input('Number of previous seasons: '))
        except:
            print('Value invalid.')
            continue
        league = options.get(option)
        if league == None:
            print('Invalid. The league you chose is invalid.')
        else:
            break
    s = Scraper()
    print(calc_time_spent(s, [league, number_of_seasons, season]))


def calc_time_spent(s: Scraper, vars: list) -> str:
    start = datetime.now()
    s.do_scraping(vars[0], vars[1],vars[2])
    time_elapsed = str(datetime.now() - start).split(':')
    time_elapsed[-1] = round(float(time_elapsed[-1]))
    t_e = f'{time_elapsed[0]}:{time_elapsed[1]}:{time_elapsed[2]}'
    return f'Time elapsed: {t_e}'


if __name__ == '__main__':
    add_new_data()
