from contextlib import closing
import sqlite3

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
                            odd_visiting REAL NOT NULL,
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


def add_team_lg_bkmkr(id_name: str, table: str, var: str) -> int:
    with sqlite3.connect('matches.db') as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('PRAGMA foreign_keys = ON;')
            cursor.execute(f'SELECT {id_name} FROM {table} WHERE name = ?',
                           (var,))
            result = cursor.fetchone()
            if result == None:
                try:
                    cursor.execute(f'INSERT INTO {table} (name) VALUES(?)',
                                   (var,))

                    cursor.execute(f'SELECT {id_name} FROM {table} WHERE name = ?',
                                   (var,))
                    result = cursor.fetchone()
                except:
                    raise InsertIntoDBError
                else:
                    conn.commit()
                    return result[0]
            else:
                conn.commit()
                return result[0]


def exists(attrs: list) -> bool:
    with sqlite3.connect('matches.db') as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('PRAGMA foreign_keys = ON;')
            cursor.execute('''SELECT id_match FROM Matches WHERE (date,instant,
                            fk_id_home_team,fk_id_visiting_team) = (?,?,?,?)''',
                           (attrs[0], attrs[1], attrs[2], attrs[3]))
            result = cursor.fetchone()
            if result == None:
                return False
            else:
                return True


def add_match_db(match: list, odds_1x2: dict, odds_ou: dict) -> None:
    with sqlite3.connect('matches.db') as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('PRAGMA foreign_keys = ON;')
            fk_id_home_team = add_team_lg_bkmkr('id_team', 'Teams', match[0])
            fk_id_visiting_team = add_team_lg_bkmkr(
                'id_team', 'Teams', match[1])
            fk_id_league = add_team_lg_bkmkr('id_league', 'Leagues', match[2])
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
            fk_id_match = int(cursor.fetchone()[0])
            conn.commit()
            add_odds_db(fk_id_match, odds_1x2, odds_ou)


def add_odds_db(fk_id_match: int, odds_1x2: dict, odds_ou: dict) -> None:
    for i in odds_1x2:
        with sqlite3.connect('matches.db') as conn:
            with closing(conn.cursor()) as cursor:
                fk_id_bookmaker = add_team_lg_bkmkr(
                    'id_bookmaker', 'Bookmakers', i)
                cursor.execute('''
                                    INSERT INTO Odds_1x2 (fk_id_bookmaker, odd_home, odd_draw,
                                    odd_visiting, fk_id_match) VALUES(?,?,?,?,?)
                            ''', (fk_id_bookmaker, odds_1x2[i][0], odds_1x2[i][1],
                                  odds_1x2[i][2], fk_id_match))
    for i in odds_ou:
        with sqlite3.connect('matches.db') as conn:
            with closing(conn.cursor()) as cursor:
                fk_id_bookmaker = add_team_lg_bkmkr(
                    'id_bookmaker', 'Bookmakers', i)
                for j in range(len(odds_ou[i])):
                    cursor.execute('''
                                    INSERT INTO Odds_ou (fk_id_bookmaker, total, odd_over,
                                    odd_under, fk_id_match) VALUES(?,?,?,?,?)
                            ''', (fk_id_bookmaker, odds_ou[i][j][0], odds_ou[i][j][1],
                                  odds_ou[i][j][2], fk_id_match))
            conn.commit()
