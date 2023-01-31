import os, datetime
import pandas as pd

#crontab 0 20 1 * *   root   python3 /home/real/relatorios-whatsapp/relatorio_terminais_conversas_diario.py
# caminho da pasta raiz de backups do whatsapp
path_backup = r'PATH\TO\BACKUP\WHATSAPP'
MESES={'January': 'JANEIRO', 'February': 'FEVEREIRO', 'March': 'MARÇO', 'April': 'ABRIL', 'May': 'MAIO', 'June': 'JUNHO', 'July': 'JULHO', 'August': 'AGOSTO', 'September': 'SETEMBRO', 'October': 'OUTUBRO', 'November': 'NOVEMBRO', 'December': 'DEZEMBRO'}
now = datetime.datetime.now().date()
# now = datetime.datetime.strptime('01/01/2023', '%d/%m/%Y').date()
yesterday=now - datetime.timedelta(1)
year = yesterday.year
month = MESES[yesterday.strftime('%B')]
path_month = os.path.join(path_backup, str(year), month)
date = '{}-{}'.format(year, month)
# lista itens da pasta de backups
itens = os.listdir(path_month)
dic_conversas = {}
dic_terminais = {}
for item in itens:
    dic_conversas.update({item:os.listdir(os.path.join(path_month, item))})
for day in itens:
    day_path = os.path.join(path_month, day)
    day_itens = os.listdir(day_path)
    dic_terminais.update({day:[]})
    for chat in day_itens:
        if os.path.isdir(os.path.join(day_path, chat)):
            for x in os.listdir(os.path.join(day_path, chat)):
                if x.endswith('.txt'):
                    x = x.replace('.txt', '')
                    dic_terminais[day].append(x)
                else:
                    dic_terminais[day].append('')
                dic_terminais[day] = list(set(dic_terminais[day]))
                dic_terminais[day].sort(reverse=True)
            # dic_terminais[day].extend([x.replace('.txt', '')  if x.endswith('.txt')])
    # dic_terminais.get(date).extend([x.replace('.txt','') for x in os.listdir(os.path.join(path_month,item)) if x.endswith('.txt')])
    
# dic_terminais[date] = list(set(dic_terminais.get(date)))

# escrita da planilha com todas as conversas e terminais que fizeram o backup
path_out = r'PATH\TO\RELATORIO\BACKUP\WHATSAPP'
path_year = os.path.join(path_out, str(year))
if not os.path.isdir(path_year):
    os.mkdir(path_year)
path_month = os.path.join(path_year, month)
if not os.path.isdir(path_month):
    os.mkdir(path_month)
path_date = os.path.join(path_month, date)
if not os.path.isdir(path_date):
    os.mkdir(path_date)
    
with pd.ExcelWriter(os.path.join(path_date, 'relatorio-conversas_{}.xlsx'.format(date))) as writer:  
    for day,chats in dic_conversas.items():
        df = pd.DataFrame.from_dict({day:chats})
        df.to_excel(writer, sheet_name=day)
with pd.ExcelWriter(os.path.join(path_date, 'relatorio-terminais_{}.xlsx'.format(date))) as writer:  
    for day,terminais in dic_terminais.items():
        df = pd.DataFrame.from_dict({day:terminais})
        # for day, terminais in days.items():
        #     df = pd.DataFrame.from_dict({day:list(set(terminais))})
        df.to_excel(writer, sheet_name=day)
        
