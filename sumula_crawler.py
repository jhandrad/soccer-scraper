import os
from pathlib import Path

import requests


# relacao de-para entre codigo e a divisao do campeonato
de_para_cod_serie = {1: 'Série A',
                     2: 'Série B',
                     3: 'Série C',
                     5: 'Série D'}


# funcao que faz um get nas sumulas e salva no diretorio adequado
def get_sumula(ano, serie, num_jogo):
    # cria a pasta do ano em questao caso ainda nao exista
    create_dir = not os.path.isdir(f'Súmulas/{ano}')
    if create_dir:
        os.mkdir(f'Súmulas/{ano}')
    # cria a pasta da divisao dentro da pasta do ano caso ainda nao exista
    create_dir = not os.path.isdir(
        f'Súmulas/{ano}/{de_para_cod_serie.get(serie)}')
    if create_dir:
        os.mkdir(f'Súmulas/{ano}/{de_para_cod_serie.get(serie)}')
    # necessario por conta da diferenca da url antes e depois de 2012
    if ano == 2012:
        # faz o get no pdf e salva no diretório
        url_igual_2012 = f'https://conteudo.cbf.com.br/sumulas/2012/{serie}42{num_jogo}s.pdf'
        sumula_pdf = requests.get(url_igual_2012)
        path = f'Súmulas/{ano}/{de_para_cod_serie.get(serie)}'
        with open(f'{path}/sumula_{ano}{serie}{num_jogo}.pdf', 'wb') as f:
            cont = 0
            sz = 0
            while(sz <= 10 and cont < 5):
                f.write(sumula_pdf.content)
                sz = Path(
                    f'{path}/sumula_{ano}{serie}{num_jogo}.pdf').stat().st_size
                cont += 1
                if cont == 5:
                    print('Última tentativa.')
                    print('Verifique a disponibilidade da rede ou do arquivo:' +
                          f'ano:{ano} serie:{serie} n.jogo:{num_jogo}')

    else:
        # faz o get no pdf e salva no diretório
        url_maior_2012 = f'https://conteudo.cbf.com.br/sumulas/{ano}/{serie}42{num_jogo}se.pdf'
        sumula_pdf = requests.get(url_maior_2012)
        path = f'Súmulas/{ano}/{de_para_cod_serie.get(serie)}'
        with open(f'{path}/sumula_{ano}{serie}{num_jogo}.pdf', 'wb') as f:
            cont = 0
            sz = 0
            while(sz <= 10 and cont < 5):
                f.write(sumula_pdf.content)
                sz = Path(
                    f'{path}/sumula_{ano}{serie}{num_jogo}.pdf').stat().st_size
                cont += 1
                if cont == 5:
                    print('Última tentativa.')
                    print('Verifique a disponibilidade da rede ou do arquivo:' +
                          f'ano:{ano} serie:{serie} n.jogo:{num_jogo}')


for i in range(2012, 2022):
    for j in [1, 2, 3, 5]:
        for k in range(1, 381):
            get_sumula(i, j, k)
