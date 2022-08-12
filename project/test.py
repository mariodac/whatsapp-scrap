#Desenvolvido por Mario Cabral em 23/07/2022
#Atualização: 29/07/2022.
#Abre whatsapp web e salva print das conversas pesquisadas pelo usuario

from scraper_wa import *

# diretorio para salvar imagens
path_out = r"D:\Imagens\TESTE-WA"

# read_input = input('Nome -> ')
# locate_chat_ignore_case(read_input)
# locate_all_chat_by_name(path_out)
# locate_chat_today(path_out)
locate_all_chat(path_out)