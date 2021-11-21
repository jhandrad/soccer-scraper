from contextlib import closing
import sqlite3
import time

from bs4.element import ResultSet

from my_exceptions import InsertIntoDBError


def create_db() -> None:
    with sqlite3.connect('matches.db') as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('PRAGMA foreign_keys = ON;')

            cursor.execute('''
                        CREATE TABLE Teams(
                            id_team INTEGER primary key AUTOINCREMENT,
                            name VARCHAR(45) NOT NULL
                            )'''
                           )
            
            cursor.execute('''
                        CREATE TABLE Leagues(
                            id_league INTEGER primary key AUTOINCREMENT,
                            name VARCHAR(45) NOT NULL
                            )'''
                           )

            cursor.execute('''
                        CREATE TABLE Matches(
                            id_match INTEGER primary key AUTOINCREMENT,
                            date VARCHAR(10) NOT NULL,
                            instant VARCHAR(5) NOT NULL,
                            fk_id_home_team INTEGER NOT NULL,
                            fk_id_visiting_team INTEGER NOT NULL,
                            goal_home_team INTEGER NOT NULL,
                            goal_visiting_team INTEGER NOT NULL,
                            fk_id_league INTEGER NOT NULL,
                            round INTEGER NOT NULL,
                            season VARCHAR(10) NOT NULL,
                            FOREIGN KEY(fk_id_home_team) REFERENCES Teams (id_team),
                            FOREIGN KEY(fk_id_visiting_team) REFERENCES Teams (id_team),
                            FOREIGN KEY(fk_id_league) REFERENCES Leagues (id_league)
                            )'''
                           )
            
            cursor.execute('''
                        CREATE TABLE Bookmakers(
                            id_bookmaker INTEGER primary key AUTOINCREMENT,
                            name VARCHAR(45) NOT NULL
                            )'''
                           )

            cursor.execute('''
                        CREATE TABLE Odds_1x2(
                            id_odd INTEGER primary key AUTOINCREMENT,
                            fk_id_bookmaker INTEGER NOT NULL,
                            odd_home REAL NOT NULL,
                            odd_draw REAL NOT NULL,
                            odd_visitor REAL NOT NULL,
                            fk_id_match INTEGER NOT NULL,
                            FOREIGN KEY(fk_id_bookmaker) REFERENCES Bookmakers (id_bookmaker),
                            FOREIGN KEY(fk_id_match) REFERENCES Matches (id_match)
                            )'''
                           )
            
            cursor.execute('''
                        CREATE TABLE Odds_ou(
                            id_odd INTEGER primary key AUTOINCREMENT,
                            fk_id_bookmaker INTEGER NOT NULL,
                            total REAL NOT NULL,
                            odd_over REAL NOT NULL,
                            odd_under REAL NOT NULL,
                            fk_id_match INTEGER NOT NULL,
                            FOREIGN KEY(fk_id_bookmaker) REFERENCES Bookmakers (id_bookmaker),
                            FOREIGN KEY(fk_id_match) REFERENCES Matches (id_match)
                            )'''
                           )

            conn.commit()


def add_team(team: str) -> int:
    with sqlite3.connect('matches.db') as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('PRAGMA foreign_keys = ON;')
            cursor.execute('''SELECT id_team FROM Teams WHERE name = ?''',
                            (team,))
            result = cursor.fetchone()
            if result == None:
                
                cursor.execute('''INSERT INTO Teams (name) 
                                VALUES(?)''', (team,))
                
                cursor.execute('''SELECT id_team FROM Teams WHERE name = ?''',
                            (team,))
                result = cursor.fetchone()
                conn.commit()
                return result[0]
            else:
                conn.commit()
                return result[0]
            

def add_league(league: str) -> int:                          
    with sqlite3.connect('matches.db') as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('PRAGMA foreign_keys = ON;')
            cursor.execute('''SELECT id_league FROM Leagues WHERE name = ?''',
                            (league,))
            result = cursor.fetchone()
            if result == None:
               
                cursor.execute('''INSERT INTO Leagues (name) 
                                VALUES(?)''', (league,))
                
                cursor.execute('''SELECT id_league FROM Leagues WHERE name = ?''',
                            (league,))
                result = cursor.fetchone()
                conn.commit()
                return result[0]
            else:
                conn.commit()
                return result[0]


def add_bookmaker(bookmaker: str) -> int:
    with sqlite3.connect('matches.db') as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('PRAGMA foreign_keys = ON;')
            cursor.execute('PRAGMA busy_timeout = 1000;')
            cursor.execute('''SELECT id_bookmaker FROM Bookmakers WHERE name = ?''',
                            (bookmaker,))
            result = cursor.fetchone()
            if result == None:
               
                cursor.execute('''INSERT INTO Bookmakers (name) 
                                VALUES(?)''', (bookmaker,))
               
                cursor.execute('''SELECT id_bookmaker FROM Bookmakers WHERE name = ?''',
                            (bookmaker,))
                result = cursor.fetchone()
                conn.commit()
                return result[0]
            else:
                conn.commit()
                return result[0]


def add_match_db(match: list, odds_1x2: dict, odds_ou: dict) -> None:
    with sqlite3.connect('matches.db') as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('PRAGMA foreign_keys = ON;')
            fk_id_home_team = add_team(match[0])
            fk_id_visiting_team = add_team(match[1])
            fk_id_league = add_league(match[2])
            cursor.execute('''
                                INSERT INTO Matches (date, instant, fk_id_home_team,
                                fk_id_visiting_team, goal_home_team, goal_visiting_team,
                                fk_id_league, round, season)
                                    VALUES(?,?,?,?,?,?,?,?,?)
                            ''', (match[3], match[4], fk_id_home_team, fk_id_visiting_team, 
                                    match[5], match[6], fk_id_league, match[7], match[8]))
            cursor.execute(
                '''SELECT id_match FROM Matches WHERE id_match=
                                (SELECT MAX(id_match) FROM Matches)''')
            # fk_id_match = int(cursor.fetchone()[0])
            # for i in odds_1x2:
            #     fk_id_bookmaker = add_bookmaker(i)
            #     cursor.execute('''
            #                         INSERT INTO Odds_1x2 (fk_id_bookmaker, odd_home, odd_draw,
            #                         odd_visiting, fk_id_match) VALUES(?,?,?,?,?)
            #                 ''', (fk_id_bookmaker, odds_1x2[i][0], odds_1x2[i][1],
            #                         odds_1x2[i][2], fk_id_match))
            # for i in odds_ou:
            #     fk_id_bookmaker = add_bookmaker(i)
            #     for j in range(len(odds_ou[i])):
            #         cursor.execute('''
            #                         INSERT INTO Odds_ou (fk_id_bookmaker, total, odd_over,
            #                         odd_under, fk_id_match) VALUES(?,?,?,?,?)
            #                 ''', (fk_id_bookmaker, odds_1x2[i][j][0], odds_1x2[i][j][1],
            #                         odds_1x2[i][j][2], fk_id_match))
            conn.commit()
            

# def get_db() -> None:
#     with sqlite3.connect('matches.db') as conn:
#         with closing(conn.cursor()) as cursor:
#             cursor.execute('PRAGMA foreign_keys = ON;')
#             matches = open('matches.txt', 'w')
#             matches.write('{0:^10} | {1:^20} | {2:^10} | {3:^30} | {4:^30} | {5:^10}\n'.format
#                           ('id', 'league', 'season', 'home', 'visitor', 'score'))

#             cursor.execute('SELECT * FROM matches')
#             for i in (cursor.fetchall()):
#                 matches.write(f'{i[0]:^10} | {i[1]:^20} | {i[2]:^10} | ' +
#                               f'{i[3]:^30} | {i[4]:^30} | {i[5]:^10}\n')

#             cursor.execute('SELECT * FROM odds')
#             odds = open('odds.txt', 'w')
#             odds.write('{0:^20} | {1:^20} | {2:^20} | {3:^20} | {4:^20}\n'.format
#                        ('bookmaker', 'odd_home', 'odd_draw', 'odd_visitor', 'fk_id_match'))

#             for i in (cursor.fetchall()):
#                 odds.write(
#                     f'{i[1]:^20} | {i[2]:^20} | {i[3]:^20} | {i[4]:^20} | {i[5]:^20}\n')

#             matches.close()
#             odds.close()
