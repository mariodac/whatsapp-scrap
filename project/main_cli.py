#Desenvolvido por Mario Cabral em 23/07/2022
#Atualização: 29/07/2022.
#Abre whatsapp web e salva print das conversas pesquisadas pelo usuario

from scraper_wa import ScraperWhatsapp
import wx, os, datetime

class MainCli:
    def escolher_diretorio(self,nome:str="saida"):    
        # cria instancia da tela que não tera um pai (janela principal)
        app = wx.App(None)
        # cria um objeto de dialog de diretório sem um pai
        dialog = wx.DirDialog (None, "Escolha um diretório", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        #verifica se o usuário clicou em ok
        if dialog.ShowModal() == wx.ID_OK: 
            # diretorio selecionado para criar diretório onde salvar imagens
            path_escolhido = dialog.GetPath()
        else: # caso não clique em OK
            # diretorio para criar diretório onde salvar imagens
            path_escolhido = os.path.dirname(os.path.abspath(__file__))
            # lista itens do diretorio path_saida
            diretorio = os.listdir(path_escolhido)
            # monta caminho para salvar prints
            path_saida = os.path.join(path_escolhido, nome)
            # verifica se não existe nenhum item com esse nome no diretorio
            if "prints" not in diretorio:
                # verificar se não há nenhum diretorio com esse mesmo nome
                if not os.path.isdir(path_saida):
                    # cria diretorio
                    os.mkdir(path_saida)

        # destroi os objetos para liberar a memória
        dialog.Destroy()
        app.Destroy()

        return path_saida

    def apenas_inteiro(self):
        # realiza a leitura apenas de inteiro
        try:
            # lê a entrada do teclado
            opcao = int(input(">> "))
        except Exception:
            # loop enquando não for informado um inteiro
            while type(opcao) != int:
                print('Opção invalida')
                opcao = input(">> ")
                try:
                    opcao = int(opcao)
                except ValueError:
                    continue
        return opcao
if __name__ == '__main__':
    mainCli = MainCli()
    while True:
        data_atual = datetime.datetime.today()
        data_atual = data_atual.strftime('%d/%m/%Y')
        print("0 - para encerrar\n1 - para localizar conversa pelo nome\n2 - para localizar as conversas do dia de hoje {}\n3 - para localizar conversas com certa quantidade de dias\n4 - para localizar todas as conversas".format(data_atual))
        opcao = mainCli.apenas_inteiro()
        if opcao == 0:
            break
        if opcao in range(1,5):
            scrapperWAPP = ScraperWhatsapp()
            path_saida = mainCli.escolher_diretorio()
        if opcao == 1:
            nome = input("Digite o nome >> ")
            scrapperWAPP.locate_chat_ignore_case(nome, path_saida)
        if opcao == 2:
            scrapperWAPP.locate_chat_today(path_saida)
        if opcao == 3:
            n_dias = input("Digite a quantidade de dias (padrão=3 | aperte ENTER)")
            if n_dias == "":
                ScraperWhatsapp.locate_chat_ndays(path_saida)
            else:
                n_dias = mainCli.apenas_inteiro()
                ScraperWhatsapp.locate_chat_ndays(path_saida, n_dias)
        if opcao == 4:
            ScraperWhatsapp.locate_all_chat(path_saida)
        else:
            print("Opção inválida")