import os, datetime
import pandas as pd

#crontab 0 20    * * *   root   python3 /home/real/relatorios-whatsapp/relatorio_terminais_conversas_diario.py
# caminho da pasta raiz de backups do whatsapp
path_backup = r'PATH\TO\BACKUP\WHATSAPP'
MESES={'January': 'JANEIRO', 'February': 'FEVEREIRO', 'March': 'MARÇO', 'April': 'ABRIL', 'May': 'MAIO', 'June': 'JUNHO', 'July': 'JULHO', 'August': 'AGOSTO', 'September': 'SETEMBRO', 'October': 'OUTUBRO', 'November': 'NOVEMBRO', 'December': 'DEZEMBRO'}
now = datetime.datetime.now().date()
year = now.year
month = MESES[now.strftime('%B')]
date = now.strftime("%d-%m-%Y")
path_day = os.path.join(path_backup, str(year), month, date)
# lista itens da pasta de backups
itens = os.listdir(path_day)
dic_conversas = {date:itens}
dic_terminais = {date:[]}
for item in itens:
    dic_terminais.get(date).extend([x.replace('.txt','') for x in os.listdir(os.path.join(path_day,item)) if x.endswith('.txt')])
    
dic_terminais[date] = list(set(dic_terminais.get(date)))

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
    for year_month,chats in dic_conversas.items():
        df = pd.DataFrame.from_dict({year_month:chats})
        df.to_excel(writer, sheet_name=year_month)
with pd.ExcelWriter(os.path.join(path_date, 'relatorio-terminais_{}.xlsx'.format(date))) as writer:  
    for year_month,days in dic_terminais.items():
        df = pd.DataFrame.from_dict(dic_terminais)
        # for day, terminais in days.items():
        #     df = pd.DataFrame.from_dict({day:list(set(terminais))})
        df.to_excel(writer, sheet_name=year_month)
        
