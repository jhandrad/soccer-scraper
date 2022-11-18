import pymongo
import enchant
from bson.objectid import ObjectId
 

def match_nome(nome1:str, nome2:str) -> bool:
    if nome1 == nome2:
        return True
    elif (nome1.split('/'))[0].strip() == (nome2.split('/'))[0]:
        return True
    else:
        False


def levenshtein(nome1:str, nome2:str) -> int:
    return enchant.utils.levenshtein(nome1, nome2)


def match_nome_2(nome1:str, nome2:str) -> bool:
    if (nome1.split('/')[1].strip()) == (nome2.split('/')[1].strip()):
        return True
    return False 


def trata_numero_sub(texto:str) -> int:
    return int(texto.split('-')[0].strip())


problema_nome_times = []
problema_subs = []
problema_numero_sub = []
jogos_wo = []

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["pibic"]
collection = db["matches"]

match = collection.find_one({'_id':ObjectId('62b49c018f6cacbb0aa54f80')})

home = match['teams']['home']
away = match['teams']['away']

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
            problema_nome_times.append(match['_id'])
            break
        
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
                problema_numero_sub.append((match['_id'], n_sub))
                break
            
        if (player_in) or (player_out):
            problema_subs.append((match['_id'], n_sub))
    
else:
    jogos_wo.append((match['_id']))