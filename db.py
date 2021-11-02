from contextlib import closing
import sqlite3

from my_exceptions import InsertIntoDBError


def create_db() -> None:
    with sqlite3.connect('matches.db') as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('PRAGMA foreign_keys = ON;')
            cursor.execute('''
                        CREATE TABLE matches(
                            id_match INTEGER primary key AUTOINCREMENT,
                            championship VARCHAR(40) NOT NULL,
                            season VARCHAR(10) NOT NULL,
                            home VARCHAR(30) NOT NULL,
                            visitor VARCHAR(30) NOT NULL,
                            game_score VARCHAR(6) NOT NULL
                            )'''
                           )

            cursor.execute('''
                        CREATE TABLE odds(
                            id_odd INTEGER primary key AUTOINCREMENT,
                            bookmaker VARCHAR(20) NOT NULL,
                            odd_home VARCHAR(6) NOT NULL,
                            odd_draw VARCHAR(6) NOT NULL,
                            odd_visitor VARCHAR(6) NOT NULL,
                            fk_id_match INTEGER NOT NULL,
                            FOREIGN KEY(fk_id_match) REFERENCES matches (id_match)
                            )'''
                           )
            conn.commit()


def add_match_db(match: list, odds: dict) -> None:
    with sqlite3.connect('matches.db') as conn:
        with closing(conn.cursor()) as cursor:
            try:
                cursor.execute('PRAGMA foreign_keys = ON;')
                cursor.execute('''
                                    INSERT INTO matches (championship, season, home,
                                    visitor, game_score) VALUES(?,?,?,?,?)
                            ''', (match[0], match[1], match[2], match[3], match[4]))
                cursor.execute(
                                '''SELECT id_match FROM matches WHERE id_match=
                                   (SELECT MAX(id_match) FROM matches)''')
                fk_id_match = int(cursor.fetchone()[0])
                for i in odds:
                    cursor.execute('''
                                        INSERT INTO odds (bookmaker, odd_home, odd_draw,
                                        odd_visitor, fk_id_match) VALUES(?,?,?,?,?)
                                ''', (i, odds[i][0], odds[i][1], odds[i][2], fk_id_match))
                conn.commit()
            except:
                raise InsertIntoDBError()


def get_db() -> None:
    with sqlite3.connect('matches.db') as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('PRAGMA foreign_keys = ON;')  
            cursor.execute('SELECT * FROM matches')
            matches = open('matches.txt', 'w')
            matches.write('{0:^10} | {0:^40} | {0:^10} | {1:^30} | {2:^30} | {3:^10}\n'.format
                        ('id', 'championship', 'season','home', 'visitor', 'score'))

            for i in (cursor.fetchall()):
                matches.write('{0:^10} | {0:^40} | {0:^10} | {1:^30} | {2:^30} | {3:^10}\n'.format
                        (i[0],i[1],i[2],i[3],i[4],i[5]))

            cursor.execute('SELECT * FROM odds')
            odds = open('odds.txt', 'w')
            odds.write('{0:^20} | {1:^20} | {2:^20} | {3:^20} | {4:^20}\n'.format
                        ('bookmaker', 'odd_home', 'odd_draw', 'odd_visitor', 'fk_id_match'))

            for i in (cursor.fetchall()):
                odds.write('{0:^20} | {1:^20} | {2:^20} | {3:^20} | {4:^20}\n'.format
                        (i[1],i[2],i[3],i[4],i[5]))

            matches.close()
            odds.close()