import os
import pandas as pd

# caminho da pasta raiz de backups do whatsapp
path_backup = r'PATH\TO\BACKUP\WHATSAPP'
# lista itens da pasta de backups
itens = os.listdir(path_backup)
years = [x for x in os.listdir(path_backup)]
months = {x:os.listdir(os.path.join(path_backup, x)) for x in years}
dic_year_month ={}
for x, y in months.items():
    for z in y:
        dic_year_month.update({'{}-{}'.format(x,z):os.listdir(os.path.join(path_backup, x, z))})
dic_conversas = {x:[] for x in dic_year_month.keys()}
dic_terminais = {x:{} for x in dic_year_month.keys()}
# setembro-2022 21283
# janeiro-2023 19652
for x,y in dic_year_month.items():
    for z in y:
        conversas = os.listdir(os.path.join(path_backup, x.split('-')[0], x.split('-')[1], z))
        dic_conversas.get(x).extend(conversas)
        for conversa in conversas:
            # arquivos dentro da pasta de conversa
            conversas_files = os.listdir(os.path.join(path_backup, x.split('-')[0], x.split('-')[1], z, conversa))
            dic_terminais.get(x).update({z:[i for i in conversas_files if i.endswith('.txt')]})
with pd.ExcelWriter('relatorio-conversas.xlsx') as writer:  
    for x,y in dic_conversas.items():
        df = pd.DataFrame.from_dict({x:y})
        df.to_excel(writer, sheet_name=x)
with pd.ExcelWriter('relatorio-terminais.xlsx') as writer:  
    for x,y in dic_terminais.items():
        df = pd.DataFrame.from_dict({x:y})
        df.to_excel(writer, sheet_name=x)
        
