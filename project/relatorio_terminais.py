import os
import pandas as pd


def read_while_type_is_different(typ:type, message:str=None):
    """Continua lendo enquanto não é informado o tipo de dado especificado

    Args:
        typ (Any): tipo de dadp
        message (str, optional): Mensagem a ser exibida no input. Defaults to None.

    Returns:
        Any: dado lido
    """
    inp = None
    while type(inp) != typ:
        if message:
            inp = input(message)
        else:
            inp = input("Digite > ")
        try:
            inp = typ(inp)
        except:
            print("Informe um dado do tipo {}".format(typ))
            continue
    return inp

def print_itens(itens:list):
    for index, item in enumerate(itens):
        print('{} : {}'.format(index,item))

path_backup = r'PATH\TO\BACKUP\WHATSAPP'
# escolha do ano
# lista itens da pasta de backups
itens = os.listdir(path_backup)
print('Escolha o ano')
# exibe as pastas dos anos
print_itens(itens)
# continua lendo enquanto não informa um inteiro
op = read_while_type_is_different(int, "Digite a opção > ")
# monta caminho do ano
year = itens[op]
path_year = os.path.join(path_backup, itens[op])
# lista itens da pasta do ano
itens = os.listdir(path_year)
# exibe as pastas dos meses
print('Escolha o mês')
print_itens(itens)
# continua lendo enquanto não informa um inteiro
op = read_while_type_is_different(int, "Digite a opção > ")
# monta caminho do mes
month = itens[op]
path_month = os.path.join(path_year, itens[op])
print('Escolha o dia')
# lista itens da pasta do dia
itens = os.listdir(path_month)
# exibe as pastas dos dias
print_itens(itens)
# continua lendo enquanto não informa um inteiro
op = read_while_type_is_different(int, "Digite a opção > ")
# monta caminho do dia
date = itens[op]
path_day = os.path.join(path_month, itens[op])
itens = os.listdir(path_day)
conversas_path = [os.path.join(path_day, x) for x in itens]
terminais = []
for item in conversas_path:
    terminais.extend([x.replace('.txt', '') for x in os.listdir(item) if x.endswith('.txt')])
terminais = [x for x in terminais if x]
terminais = list(set(terminais))
dic = {date: terminais}
df = pd.DataFrame.from_dict(dic)
df.to_excel(os.path.join(os.environ['USERPROFILE'], 'Desktop', '{}.xlsx'.format(date)))

