import pandas as pd
import bs4 as bs
from unidecode import unidecode
from itertools import combinations
from tqdm import tqdm
import csv
from subprocess import check_output
import os

source = ''
with open('source.txt' , 'r', encoding="UTF8") as file:
    source = file.read()

soup = bs.BeautifulSoup(source, 'lxml')

def hour_code_to_index(code):
    weekday = int(code[0]) - 2
    period = code[1]
    number = int(code[2]) - 1
    offset = 0
    if period == 'T':
        offset = 6
    elif period == 'N':
        offset = 12
    index = (18 * weekday) + offset + number
    return index

trs = soup.find_all('tr')
data = {'codigo':[], 'materia':[], 'horarios':[]}
counter = -1
for tr in trs:
    td = tr.find('td', {'class':'t'})
    if td != None:
        txt = td.get_text()
        split = txt.split(' - ')
        data['codigo'].append(split[0].strip())
        split = ''.join(split[1:]).split('(')
        data['materia'].append(unidecode(split[0].strip()))
        data['horarios'].append({})
        counter += 1
    else:
        tds = tr.find_all('td', {'class':'sl'})
        if len(tds) > 0:
            turma = tds[0].get_text()
            horario = tds[2].get_text()
            if horario == '\xa0':
                continue
            horario_ls = horario.split(' - ')
            horario_ls = [h[:h.index('(')] for h in horario_ls]
            horario_ls = list(map(hour_code_to_index, horario_ls))
            if turma not in data['horarios'][counter]:
                data['horarios'][counter][turma] = []
            data['horarios'][counter][turma] = horario_ls

df = pd.DataFrame(data=data)

materias = ['Análise De Algorítmos',
            'Comunicação Oral E Escrita',
            'Sistemas De Controle',
            'Transmissão De Dados',
            'Compiladores',
            'Engenharia De Software',
            'Sistemas Operacionais',
            'Sistemas Microcontrolados',
            'Ciências Do Ambiente',
            'Eletrônica Geral 2',
            'Oficina De Integração'
            ]


materias = list(map(lambda item: unidecode(item), materias))

data = {'materia':[], 'horarios':[], 'codes': []}
for materia in materias:
    res = df[df['materia'] == materia]
    if len(res) > 0:
        h = {}
        codes = []
        for index, row in res.iterrows():
            h.update(row['horarios'])
            for key in row['horarios'].keys():
                codes.append(row['codigo'] + '-' + key)
            #codes += [row['codigo']] * len(row['horarios'])
        data['materia'].append(materia)
        data['horarios'].append(h)
        data['codes'].append(codes)

result = pd.DataFrame(data=data)

with open("horarios.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    for index, row in result.iterrows():
        for h in row['horarios'].values():
            writer.writerow([index] + h)

out = str(check_output(['./calc.exe']))
out = out.split(" \\r\\n")

h = []


for code in out:
    os.system('cls')
    h = [['']*18 for i in range(5)]
    for index, val in enumerate(code.strip("b'").split(" ")):
        val = int(str(val))
        if val != 0:
            selected = list(result.iloc[index]['horarios'].values())[val - 1]
            code = result.iloc[index]['codes'][val - 1]
            for horario_index in selected:
                weekday = horario_index // 18
                hour = horario_index % 18
                h[weekday][hour] = code
    weekdays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    data = dict(zip(weekdays, h))
    horario_df = pd.DataFrame(data=data)
    print(horario_df)
    
    opt = str(input())
    if opt == 'save' or opt == 's':
        horario_df.to_excel('horario.xlsx')
        exit(0)
    elif opt == 'quit' or opt == 'q':
        exit(0)