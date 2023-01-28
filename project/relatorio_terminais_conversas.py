import os, datetime
import pandas as pd

# caminho da pasta raiz de backups do whatsapp
path_backup = r'PATH\TO\BACKUP\WHATSAPP'
# lista itens da pasta de backups
itens = os.listdir(path_backup)
# obtendo lista das pastas dos anos
years = [x for x in os.listdir(path_backup)]
# montando dicionario dos ANO:MESES {'2023':['JANEIRO', 'FEVEREIRO', ...]}
months = {x:os.listdir(os.path.join(path_backup, x)) for x in years}
dic_year_month ={}
# montando dicionario com chave do ANO-MES do backup e valor com lista das pastas que contem o dia que foi feito o backup
# {'2022-AGOSTO':['09-08-2022', '11-08-2022', '12-08-2022', ...]}
for year_month, y in months.items():
    for z in y:
        dic_year_month.update({'{}-{}'.format(year_month,z):os.listdir(os.path.join(path_backup, year_month, z))})
# montando dicionarios como {'2022-AGOSTO':[]}
dic_conversas = {x:[] for x in dic_year_month.keys()}
# montando dicionarios como {'2022-AGOSTO':{}}
dic_terminais = {x:{} for x in dic_year_month.keys()}
terminais = []
for year_month,y in dic_year_month.items():
    for z in y:
        # obtendo diretorios das conversas de cada dia
        # SERÁ PREENCHIDO COMO {'2022-AGOSTO':['+55 77 9177-2665', '+55 77 8401-8935', ...]}
        conversas = [i for i in os.listdir(os.path.join(path_backup, year_month.split('-')[0], year_month.split('-')[1], z)) if os.path.isdir(os.path.join(path_backup, year_month.split('-')[0], year_month.split('-')[1], z,i))]
        # adicionando as conversas do mês
        dic_conversas.get(year_month).extend(conversas)
        for conversa in conversas:
            # arquivos dentro da pasta de conversa
            conversas_files = os.listdir(os.path.join(path_backup, year_month.split('-')[0], year_month.split('-')[1], z, conversa))
            # adicionando no dia qual terminal foi feito o backup
            # SERÁ PREENCHIDO DA SEGUINTE MANEIRA {'16-12-2022': ['T2194.txt'], ...}
            terminais.extend([i.replace('.txt', '') for i in conversas_files if i.endswith('.txt')])
            # terminais = list(set(terminais))
            # substituir duplicatas por vazio
            # seen = set()
            # for i, e in enumerate(terminais):
            #     if e in seen:
            #         terminais[i] = ''
            #     else:
            #         seen.add(e)
            # terminais.sort(reverse=True)
            dic_terminais.get(year_month).update({z:terminais})
# escrita da planilha com todas as conversas de todo o mes, cada aba contendo um ano-mes
path_out = 'PATH\TO\RELATORIO'
now = datetime.datetime.now().date()
year = now.year
month = now.strftime("%B")
date = now.strftime('%d-%m-%Y')
path_year = os.path.join(path_out, str(year))
if not os.path.isdir(path_year):
    os.mkdir(path_year)
path_month = os.path.join(path_year, month)
if not os.path.isdir(path_month):
    os.mkdir(path_month)
path_date = os.path.join(path_month, date)
if not os.path.isdir(path_date):
    os.mkdir(path_date)
with pd.ExcelWriter('relatorio-conversas-all.xlsx') as writer:  
    for year_month,chats in dic_conversas.items():
        df = pd.DataFrame.from_dict({year_month:chats})
        df.to_excel(writer, sheet_name=year_month)
with pd.ExcelWriter('relatorio-terminais-all.xlsx') as writer:  
    for year_month,days in dic_terminais.items():
        df = pd.DataFrame.from_dict(days)
        # for day, terminais in days.items():
        #     df = pd.DataFrame.from_dict({day:list(set(terminais))})
        df.to_excel(writer, sheet_name=year_month)
        
