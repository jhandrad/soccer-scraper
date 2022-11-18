import pymongo
import enchant
 

def match_nome(nome1:str, nome2:str) -> bool:
    if nome1 == nome2:
        return True
    elif (nome1.split('/'))[0].strip() == (nome2.split('/'))[0].strip():
        return True
    else:
        False


def levenshtein(nome1:str, nome2:str) -> int:
    return enchant.utils.levenshtein(nome1, nome2)


def match_nome_2(nome1:str, nome2:str) -> bool:
    if (nome1.split('/')[1].strip()) == (nome2.split('/')[1].strip()):
        return True
    return False 


def save_results(l:list,name:str,desc:str,mode:int) -> None:
    with open (f'{name}.txt','w',encoding='utf-8') as f:
        f.write(f'{desc}{len(l)}\n')
        for i in l: 
            if mode == 1:            
                f.write(f'\t_id = {i}\n')
            elif mode == 2:
                f.write(f'\t_id = {i[0]} nº sub: {i[1]}\n')


problem_name_teams = []
problem_subs = []
problem_number_sub = []
wo = []

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["pibic"]
collection = db["matches"]
matches = collection.find()


for match in matches:
    home = match['teams']['home']
    away = match['teams']['away']

    # fluxo para o caso que os nomes sao iguais mudando apenas o estado
    if home.split('/')[0].strip() == away.split('/')[0].strip():
        n_sub = 0
        for sub in match['subs']:
            n_sub += 1
            n_in = sub['in']
            n_out = sub['out']
            name_team = sub['team']
            team = ''

            # casos que não há como distinguir os times
            if name_team == home.split('/')[0].strip():
                problem_name_teams.append(match['_id'])
                break
            if home.split('/')[1] == '' or away.split('/')[1] == '':
                problem_name_teams.append(match['_id'])
                break
            
            # compara os nomes para definir se eh home ou away
            elif match_nome_2(home, name_team):
                team = 'home' 
            elif match_nome_2(away, name_team):
                team = 'away'
            elif levenshtein(home, name_team) < levenshtein(away, name_team):
                team = 'home'
            elif levenshtein(home, name_team) > levenshtein(away, name_team):
                team = 'away'

            # para o caso das funcoes de verificacao de nomes nao funcionar
            if team == '':
                raise ValueError(f'O nome não foi identificado como "home" ou como "away". _id = {match["_id"]}')

            # busca na lista de jogadores do time (home ou away) o numero dos jogadores na substituicao
            player_in = True
            player_out = True
            for player in match['players'][team]:
                number = player['number']
                try:
                    if number == int(n_in):
                        player_in = False
                    elif number == int(n_out):
                        player_out = False
                except ValueError:
                    problem_number_sub.append((match['_id'], n_sub))
                
            if (player_in) or (player_out):
                problem_subs.append((match['_id'], n_sub))

    # fluxo para os demais casos
    else:
        if 'subs' in match.keys():
            n_sub = 0
            for sub in match['subs']:
                n_sub += 1
                n_in = sub['in']
                n_out = sub['out']
                name_team = sub['team']
                team = ''

                # compara os nomes para definir se eh home ou away
                if match_nome(home, name_team):
                    team = 'home' 
                elif match_nome(away, name_team):
                    team = 'away'
                elif levenshtein(home, name_team) < levenshtein(away, name_team):
                    team = 'home'
                elif levenshtein(home, name_team) > levenshtein(away, name_team):
                    team = 'away'

                # para o caso das funcoes de verificacao de nomes nao funcionar
                if team == '':
                    problem_name_teams.append(match['_id'])
                    break
                
                # busca na lista de jogadores do time (home ou away) o numero dos jogadores na substituicao
                player_in = True
                player_out = True
                flag = True
                for player in match['players'][team]:
                    number = player['number']
                    try:
                        if number == int(n_in):
                            player_in = False
                        elif number == int(n_out):
                            player_out = False
                    except ValueError:
                        problem_number_sub.append((match['_id'], n_sub))
                        flag = False
                        break
                    
                if (player_in or player_out) and (flag):
                    problem_subs.append((match['_id'], n_sub))
            
        else:
            wo.append((match['_id']))
            


save_results(wo,'jogos wo','Jogos que foram W.O.: ',1)
save_results(problem_name_teams,'problema nomes','Jogos com problema no nome dos times (impossibilidade para distinguir nomes): ',1)
save_results(problem_subs,
            'problema substituição','Jogos com problema em substituições (jogador não consta na lista de jogadores do time): ',2)
save_results(problem_number_sub,
            'problema numero','Jogos com problema em substituições (numero do jogador no formato: "Nº - nome"): ',2)
