import pandas as pd
import PyPDF2 as p2
import sqlite3

# os dicionarios servem para simular a estrutura de cada tabela
matches_ = {
    'id_match': [],
    'id_championship': [],
    'id_h_team': [],
    'id_a_team': [],
    'stadium': [],
    'date': [],
    'round': [],
    'season': []}
championships_ = {
    'id_championship': [],
    'name': []}
teams_ = {
    'id_team': [],
    'name': [],
    'uf': []}
athletes_ = {
    'id_athlete': [],
    'nickname': [],
    'name': []}
athletes_matches_ = {
    'id_a_m': [],
    'id_fk_athlete': [],
    'id_fk_match': [],
    't/r': [],
    'p/a': [],
    'num': []}


def popula_matches_(texto_pdf: str, estrutura_tabela: dict):
    flag1 = False
    flag2 = False
    championship = (texto_pdf[4].split('/')[0]).split(' ')
    championship = (' '.join(championship[1:])).strip()
    for i, j in enumerate(championships_['name']):
        if j == championship:
            id_championship = championships_['id_championship'][i]
            estrutura_tabela['id_championship'].append(id_championship)
    teams = texto_pdf[8].split('X')
    team1 = (teams[0].split('/'))[0].strip()
    team2 = (teams[1].split('/'))[0].strip()
    for i, j in enumerate(teams_['name']):
        if j == team1:
            id_team = teams_['id_team'][i]
            estrutura_tabela['id_h_team'].append(id_team)
            flag1 = True
        elif j == team2:
            id_team = teams_['id_team'][i]
            estrutura_tabela['id_a_team'].append(id_team)
            flag2 = True
    if not(flag1):
        estrutura_tabela['id_h_team'].append('na')
    if not(flag2):
        estrutura_tabela['id_a_team'].append('na')
    stadium = (texto_pdf[14].split('/')[0]).strip()
    estrutura_tabela['stadium'].append(stadium)
    date = texto_pdf[10].strip()
    t = texto_pdf[12].strip()
    date_t = f'{date} {t}'
    estrutura_tabela['date'].append(date_t)
    round_ = texto_pdf[6].strip()
    estrutura_tabela['round'].append(round_)
    season = date.split('/')[-1]
    estrutura_tabela['season'].append(season)
    estrutura_tabela['id_match'].append(len(estrutura_tabela['id_match'])+1)


def popula_championships_(texto_pdf: str, estrutura_tabela: dict):
    championship = (texto_pdf[4].split('/')[0]).split(' ')
    championship = (' '.join(championship[1:])).strip()
    if not(championship in estrutura_tabela['name']):
        estrutura_tabela['id_championship'].append(
            len(estrutura_tabela['id_championship'])+1)
        estrutura_tabela['name'].append(championship)


def popula_teams(texto_pdf: str, estrutura_tabela: dict):
    teams_ = texto_pdf[8].split('X')
    team1 = (teams_[0].split('/'))[0].strip()
    team2 = (teams_[1].split('/'))[0].strip()
    uf1 = (teams_[0].split('/'))[1].strip()
    uf2 = (teams_[1].split('/'))[1].strip()
    if not(team1 in estrutura_tabela['name']):
        estrutura_tabela['id_team'].append(len(estrutura_tabela['id_team'])+1)
        estrutura_tabela['name'].append(team1)
        estrutura_tabela['uf'].append(uf1)
    if not(team2 in estrutura_tabela['name']):
        estrutura_tabela['id_team'].append(len(estrutura_tabela['id_team'])+1)
        estrutura_tabela['name'].append(team2)
        estrutura_tabela['uf'].append(uf2)


def popula_athletes_(texto_pdf: str, estrutura_tabela: dict):
    indices = []
    cont = 0
    for i, j in enumerate(texto_pdf):
        if j == 'CBF':
            indices.append(i)
    for i in range((indices[0]+1), len(texto_pdf), 6):
        if (texto_pdf[i] == ' ') or (i+5 >= len(texto_pdf)):
            break
        nick = texto_pdf[i+1]
        name = texto_pdf[i+2]
        cod = texto_pdf[i+5]
        if not(cod in estrutura_tabela['id_athlete']):
            estrutura_tabela['id_athlete'].append(cod)
            estrutura_tabela['nickname'].append(nick)
            estrutura_tabela['name'].append(name)
    for i in range((indices[1]+1), len(texto_pdf), 6):
        if (texto_pdf[i] == ' ') or (i+5 >= len(texto_pdf)):
            break
        nick = texto_pdf[i+1]
        name = texto_pdf[i+2]
        cod = texto_pdf[i+5]
        if not(cod in estrutura_tabela['id_athlete']):
            estrutura_tabela['id_athlete'].append(cod)
            estrutura_tabela['nickname'].append(nick)
            estrutura_tabela['name'].append(name)


def popula_athletes_matches_(texto_pdf: str, estrutura_tabela: dict):
    indices = []
    athlts = []
    for i, j in enumerate(texto_pdf):
        if j == 'CBF':
            indices.append(i)
    for i in range((indices[0]+1), len(texto_pdf), 6):
        if (texto_pdf[i] == ' ') or (i+5 >= len(texto_pdf)):
            break
        num = texto_pdf[i]
        tr = texto_pdf[i+3]
        pa = texto_pdf[i+4]
        cod = texto_pdf[i+5]
        athlts.append((cod, num, tr, pa))
    for i in range((indices[1]+1), len(texto_pdf), 6):
        if (texto_pdf[i] == ' ') or (i+5 >= len(texto_pdf)):
            break
        num = texto_pdf[i]
        tr = texto_pdf[i+3]
        pa = texto_pdf[i+4]
        cod = texto_pdf[i+5]
        athlts.append((cod, num, tr, pa))

    for i in athlts:
        estrutura_tabela['id_fk_athlete'].append(i[0])
        estrutura_tabela['id_fk_match'].append(matches_['id_match'][-1])
        estrutura_tabela['num'].append(i[1])
        estrutura_tabela['t/r'].append(i[2])
        estrutura_tabela['p/a'].append(i[3])
        estrutura_tabela['id_a_m'].append(i[0] + str(matches_['id_match'][-1]))


serie = {1: 'Série A',
         2: 'Série B',
         3: 'Série C',
         5: 'Série D'}


try:
    for i in range(1, 3):
        for j in range(1, 381):
            path = f'Súmulas/2013/{serie.get(i)}/sumula_2013{i}{j}.pdf'
            pdf = p2.PdfFileReader(path)
            conteudo = pdf.getPage(0).extractText()
            texto_pdf = conteudo.split('\n')
            popula_championships_(texto_pdf, championships_)
            popula_teams(texto_pdf, teams_)
            popula_athletes_(texto_pdf, athletes_)
            popula_matches_(texto_pdf, matches_)
            popula_athletes_matches_(texto_pdf, athletes_matches_)
except:
    print(path)


cnx = sqlite3.connect('sumulas.db')

pd.DataFrame(data=matches_).to_csv('Matches.csv')
pd.DataFrame(data=championships_).to_csv('Championship.csv')
pd.DataFrame(data=teams_).to_csv('Teams.csv')
pd.DataFrame(data=athletes_).to_csv('Athletes.csv')
pd.DataFrame(data=athletes_matches_).to_csv('Athletes_matches.csv')

# pd.DataFrame(data=matches_).to_sql(name='Matches', con=cnx, index=False)
# pd.DataFrame(data=championships_).to_sql(name='Championship', con=cnx,index=False)
# pd.DataFrame(data=teams_).to_sql(name='Teams', con=cnx,index=False)
# pd.DataFrame(data=athletes_).to_sql(name='Athletes', con=cnx,index=False)
# pd.DataFrame(data=athletes_matches_).to_sql(name='Athletes_matches', con=cnx,index=False)


# pdf = p2.PdfFileReader('Súmulas/2013/Série A/sumula_2013192.pdf')
# conteudo = pdf.getPage(0).extractText()
# texto_pdf = conteudo.split('\n')

# for i in range(len(texto_pdf)):
#     print(f'{i} - ' + texto_pdf[i])
