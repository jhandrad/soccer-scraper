import pymongo
import enchant
from bson.objectid import ObjectId
 

def match_nome(nome1:str, nome2:str) -> bool:
    if nome1 == nome2:
        return True
    elif (nome1.split('/'))[0].strip() == (nome1.split('/'))[0]:
        return True
    else:
        False


def sem_nome(nome1:str, nome2:str) -> int:
    return enchant.utils.levenshtein(nome1, nome2)


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["pibic"]
collection = db["matches"]
match = collection.find_one({'_id':ObjectId('62b49c018f6cacbb0aa54f80')})

print(match)

# for match in matches:
#     home = match['teams']['home']
#     away = match['teams']['away']

#     if home.split('/') == away.split('/'):
#         print(f'jogo id = {match["_id"]} com problema no nome dos times')

#     n_sub = 0
#     try:
#         for sub in match['subs']:
#             n_sub += 1
#             n_in = sub['in']
#             n_out = sub['out']
#             name_team = sub['team']
#             team = ''

#             if match_nome(home, name_team):
#                 team = 'home'
#             elif match_nome(away, name_team):
#                 team = 'away'
#             else:
#                 if sem_nome(home, name_team) < sem_nome(away, name_team):
#                     team = 'home'
#                 elif sem_nome(home, name_team) > sem_nome(away, name_team):
#                     team = 'away'
            
#             player_in = False
#             player_out = False
#             for player in match['players'][team]:
#                 number = player['number']
#                 try:
#                     if number == int(n_in):
#                         player_in = True
#                     elif number == int(n_out):
#                         player_out = True
#                 except:
#                     pass

#             if not(player_in) or not(player_out):
#                 print(f'sub nº {n_sub} do jogo id = {match["_id"]} com problema')
#     except:
#         print(f'jogo id = {match["_id"]} não tem chave "subs"')




 
