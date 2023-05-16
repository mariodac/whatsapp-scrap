import os, datetime
import pandas as pd
from main_cli import MainCli

MESES={'January': 'JANEIRO', 'February': 'FEVEREIRO', 'March': 'MARÇO', 'April': 'ABRIL', 'May': 'MAIO', 'June': 'JUNHO', 'July': 'JULHO', 'August': 'AGOSTO', 'September': 'SETEMBRO', 'October': 'OUTUBRO', 'November': 'NOVEMBRO', 'December': 'DEZEMBRO'}

class Relatorios():
    
    def __init__(self):
        self.mainCli = MainCli()
        self.path_prints = self.mainCli.escolher_diretorio()
        
    def relatorio_terminais_conversas_diario(self):
        now = datetime.datetime.now().date()
        year = now.year
        month = MESES[now.strftime('%B')]
        date = now.strftime("%d-%m-%Y")
        path_day = os.path.join(self.path_prints, str(year), month, date)
        # lista itens da pasta de backups
        itens = os.listdir(path_day)
        dic_conversas = {date:itens}
        dic_terminais = {date:[]}
        for item in itens:
            dic_terminais.get(date).extend([x.replace('.txt','') for x in os.listdir(os.path.join(path_day,item)) if x.endswith('.txt')])
            
        dic_terminais[date] = list(set(dic_terminais.get(date)))

        # escrita da planilha com todas as conversas e terminais que fizeram o backup
        path_out = self.mainCli.escolher_diretorio("relatorio")
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
                
    def relatorio_terminais_conversas_mensal(self):
        # caminho da pasta raiz de backups do whatsapp
        now = datetime.datetime.now().date()
        # now = datetime.datetime.strptime('01/01/2023', '%d/%m/%Y').date()
        yesterday=now - datetime.timedelta(1)
        year = yesterday.year
        month = MESES[yesterday.strftime('%B')]
        path_month = os.path.join(self.path_prints, str(year), month)
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
        path_out = self.mainCli.escolher_diretorio("relatorio")
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
                
    def relatorio_terminais_conversas_tudo(self):
        # caminho da pasta raiz de backups do whatsapp
        # lista itens da pasta de backups
        itens = os.listdir(self.path_prints)
        # obtendo lista das pastas dos anos
        years = [x for x in os.listdir(self.path_prints)]
        # montando dicionario dos ANO:MESES {'2023':['JANEIRO', 'FEVEREIRO', ...]}
        months = {x:os.listdir(os.path.join(self.path_prints, x)) for x in years}
        dic_year_month ={}
        # montando dicionario com chave do ANO-MES do backup e valor com lista das pastas que contem o dia que foi feito o backup
        # {'2022-AGOSTO':['09-08-2022', '11-08-2022', '12-08-2022', ...]}
        for year_month, y in months.items():
            for z in y:
                dic_year_month.update({'{}-{}'.format(year_month,z):os.listdir(os.path.join(self.path_prints, year_month, z))})
        # montando dicionarios como {'2022-AGOSTO':[]}
        dic_conversas = {x:[] for x in dic_year_month.keys()}
        # montando dicionarios como {'2022-AGOSTO':{}}
        dic_terminais = {x:{} for x in dic_year_month.keys()}
        terminais = []
        for year_month,y in dic_year_month.items():
            for z in y:
                # obtendo diretorios das conversas de cada dia
                # SERÁ PREENCHIDO COMO {'2022-AGOSTO':['+55 77 9177-2665', '+55 77 8401-8935', ...]}
                conversas = [i for i in os.listdir(os.path.join(self.path_prints, year_month.split('-')[0], year_month.split('-')[1], z)) if os.path.isdir(os.path.join(self.path_prints, year_month.split('-')[0], year_month.split('-')[1], z,i))]
                # adicionando as conversas do mês
                dic_conversas.get(year_month).extend(conversas)
                for conversa in conversas:
                    # arquivos dentro da pasta de conversa
                    conversas_files = os.listdir(os.path.join(self.path_prints, year_month.split('-')[0], year_month.split('-')[1], z, conversa))
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
        path_out = self.mainCli.escolher_diretorio("relatorio")
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
    
    def print_itens(self, itens:list):
        for index, item in enumerate(itens):
            print('{} : {}'.format(index,item))
    
    def relatorio_terminais(self):
        path_backup = self.mainCli.escolher_diretorio('prints')
        path_out = self.mainCli.escolher_diretorio('relatorio')
        # escolha do ano
        # lista itens da pasta de backups
        itens = os.listdir(path_backup)
        print('Escolha o ano')
        # exibe as pastas dos anos
        self.print_itens(itens)
        # continua lendo enquanto não informa um inteiro
        op = self.mainCli.apenas_inteiro("Digite a opção > ")
        # monta caminho do ano
        year = itens[op]
        path_year = os.path.join(path_backup, itens[op])
        # lista itens da pasta do ano
        itens = os.listdir(path_year)
        # exibe as pastas dos meses
        print('Escolha o mês')
        self.print_itens(itens)
        # continua lendo enquanto não informa um inteiro
        op = self.mainCli.apenas_inteiroread_while_type_is_different(int, "Digite a opção > ")
        # monta caminho do mes
        month = itens[op]
        path_month = os.path.join(path_year, itens[op])
        print('Escolha o dia')
        # lista itens da pasta do dia
        itens = os.listdir(path_month)
        # exibe as pastas dos dias
        self.print_itens(itens)
        # continua lendo enquanto não informa um inteiro
        op = self.mainCli.apenas_inteiroread_while_type_is_different(int, "Digite a opção > ")
        # monta caminho do dia
        date = itens[op]
        path_day = os.path.join(path_month, itens[op])
        itens = os.listdir(path_day)
        conversas = {date:itens}
        conversas_path = [os.path.join(path_day, x) for x in itens]
        terminais = []
        for item in conversas_path:
            terminais.extend([x.replace('.txt', '') for x in os.listdir(item) if x.endswith('.txt')])
        terminais = [x for x in terminais if x]
        terminais = list(set(terminais))
        dic = {date: terminais}
        # path_out = r'/PATH/TO/RELATORIO'
        path_year = os.path.join(path_out, str(year))
        if not os.path.isdir(path_year):
            os.mkdir(path_year)
        path_month = os.path.join(path_year, month)
        if not os.path.isdir(path_month):
            os.mkdir(path_month)
        path_date = os.path.join(path_month, date)
        if not os.path.isdir(path_date):
            os.mkdir(path_date)
        df = pd.DataFrame.from_dict(dic)
        df.to_excel(os.path.join(path_date, 'relatorio-terminais_{}.xlsx'.format(date)))
        df = pd.DataFrame.from_dict(conversas)
        df.to_excel(os.path.join(path_date, 'relatorio-conversas_{}.xlsx'.format(date)))
