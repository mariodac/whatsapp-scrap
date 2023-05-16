#Desenvolvido por Mario Cabral em 23/07/2022
#Atualização: 26/12/2022.
#Abre whatsapp web e salva print das conversas

import re, time, os, socket, logging, datetime, requests, calendar, sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType 
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

MESES = {"01":"JANEIRO", "02":"FEVEREIRO", "03":"MARÇO", "04":"ABRIL", "05":"MAIO", "06":"JUNHO","07":"JULHO","08":"AGOSTO","09":"SETEMBRO","10":"OUTUBRO","11":"NOVEMBRO","12":"DEZEMBRO"}
DIA_DA_SEMANA = {'Sunday': 'domingo', 'Monday': 'segunda-feira', 'Tuesday': 'terça-feira', 'Wednesday': 'quarta-feira', 'Thursday': 'quinta-feira', 'Friday': 'sexta-feira', 'Saturday': 'sábado'}

class ScraperWhatsapp():
    def __init__(self):
        # dicionario para criar a pasta do diretorio do mês
        self.loggers = {}
        # hostname da máquina que executa o script
        self.hostname = socket.gethostname()
        self.name_log = 'scraper_wa'
        # configuração inicial webbdriver
        chrome_options = Options()
        # inicia o chrome com a janela maximizada
        chrome_options.add_argument("--start-maximized")
        self.getLogger().info("BACKUP INICIADO - {}".format(self.timestamp()))
        # verifica sistema operacional
        if os.name == 'nt':
            print('Windows')
            # configuração inicial webbdriver no chromium
            service = ChromeService(executable_path=ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install())
        else:
            print('Linux')
            # configuração inicial webbdriver no chromium
            service = ChromeService(executable_path=ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
            
        #INICIA CONTAGEM DE TEMPO
        t_i = self.initCountTime()
        try:
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except:
            chrome_options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

        if self.check_internet():
            #login to WhatsApp web
            try:
                self.driver.get("https://web.whatsapp.com/")
            except Exception as err:
                n_linha = sys.exc_info()[2]
                self.getLogger().error('Na linha {} - Erro no driver{}'.format(n_linha.tb_lineno,err))
        else:
            self.getLogger().error("Erro de conexão")
            raise ConnectionError("Internet fora do ar")

        # wait para scanear QR code do celular
        wait = WebDriverWait(self.driver, 600)

        # espera para carregar interface do whatsapp
        time.sleep(30)
        self.chat_header = wait.until(EC.visibility_of_element_located((By.XPATH, "//header[@data-testid='chatlist-header']")))
        
    def timestamp (self):
        """ Retorna tempo  atual em segundos"""       
        t = time.time()
        return time.ctime(t)

    def initCountTime(self, print_time=False):
        """Inicia contagem de tempo

        Args:
            print_time (bool, optional): Imprimir tempo. Defaults to False.

        Returns:
            int: tempo em segundos
        """
        if print_time:
            print(self.timestamp())
        t_i = time.time() 
        return t_i

    def finishCountTime(self, t_i, print_time=False):
        """Encerra a contagem

        Args:
            t_i (int): tempo inicial
            print_time (bool, optional): Imprimir tempo. Defaults to False.

        Returns:
            int: tempo em segundos
        """
        if print_time:
            print(self.timestamp())
        t_f = int(time.time() - t_i)
        return t_f

    def check_internet(self):
        timeout = 10
        try:
            requests.get('https://www.google.com', timeout=timeout)
            return True
        except ConnectionError:
            return False
        

    def getLogger(self):
        # verificação para não criar vários objetos e gerar linhas duplicadas no log 
        if self.loggers.get(self.name_log):
            return self.loggers.get(self.name_log)
        else:
            # configuração logger
            # formato do log
            logger = logging.getLogger(self.name_log)
            # configura nivel de log
            logger.setLevel('DEBUG')

            try:
                # verifica sistema operacional
                if os.name == 'nt':
                    # print('Windows')
                    # diretorio temp do windows
                    path_log = os.environ['TEMP']
                    log_format = '%(hostname)s - %(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    # aplica formato 
                    formatter = logging.Formatter(log_format, defaults={"hostname": self.hostname})
                else:
                    # print('Linux')
                    # caminho do log
                    path_log = os.path.join(os.environ['HOME'], '.scraper_wa')
                    # formato do log
                    log_format = '{} - %(asctime)s - %(name)s - %(levelname)s - %(message)s'.format(hostname)
                    formatter = logging.Formatter(log_format)
            except Exception as err:
                n_linha = sys.exc_info()[2]

            path_hostname = os.path.join(path_log, "scraper_wa-{}".format(self.hostname))
            # nome do arquivo de log
            file_handler = logging.FileHandler("{}.log".format(path_hostname))
            # configura formato do log
            file_handler.setFormatter(formatter)
            # adiciona arquivo ao manipulador de arquivo de log
            logger.addHandler(file_handler)
            self.loggers[self.name_log] = logger
            return logger

    def normalizeName(self, name):
        """Remove caracteres especiais do nome informado

        Args:
            name (_type_): palavra a ser removida caracteres

        Returns:
            str: palavra sem caracteres especiais
        """
        try:
            name = name.replace(':', '-')
            name = name.replace('’', '\'')
            name = re.sub(r'[\\\/\:\*\?\"\<\>\|]+', '', name)
            name = re.sub(r'[.]{2,}', '', name)
            name = ' '.join(re.findall('[\w\sà-ú\(\)\[\]\{\}\-\+\=!@#$%ªº´`¨&_§¬¢£~^\°;,.]*', name))
            name = name.strip()
            return name
        except Exception as err:
            n_linha = sys.exc_info()[2]
            self.getLogger().error('Na linha {} -{}'.format(n_linha.tb_lineno,err))

    def locate_chat(self, name:str):
        """Localiza conversa com determinado nome e clica nela

        Args:
            name (string): nome da conversa

        Returns:
            bool: True para elemento encontrado, False para  elemento não encontrado
            string: nome da conversa
        """
        try:
            if self.chat_header:
                # wait para carregar o chat 
                wait = WebDriverWait(self.driver, 10)
                try: 
                    # tag que possui o nome da conversa
                    x_arg = '//span[contains(@title, \'{}\')]'.format(name)
                    # print(x_arg)
                    # busca a tag com o nome da pessoa
                    person_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
                    # print(person_title)
                    person_title.click()
                    # espera para carregar o chat 
                    time.sleep(5)
                    name = person_title.text
                    name = self.normalizeName(name)
                    # caso não encontre o elemento retorna verdadeiro e nome do chat
                    return True, person_title.text
                except:
                    # print("Elemento não encontrado")
                    # caso não encontre o elemento retorna false e nulo
                    return False, None
        except Exception as err:
            self.driver.quit()
            n_linha = sys.exc_info()[2]
            self.getLogger().error('Na linha {} -{}'.format(n_linha.tb_lineno,err))

    def locate_chat_ignore_case(self, name:str, path_out):
        """Localiza conversa ignorando maiscula e minuscula

        Args:
            name (str): Nome da conversa
            path_out (str): caminho de saida dos prints
        """
        try:
            wait = WebDriverWait(self.driver, 10)
            # busca botão de pesquisa
            search_chat = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="chat-list-search"]')))
            # clica no botão de pesquisa
            search_chat.click()
            time.sleep(1)
            # envia o nome informado para o campo de pesquisa
            search_chat.send_keys(name)
            time.sleep(1)
            # enviando enter seleciona o primeira conversa dos resultados
            search_chat.send_keys(Keys.ENTER)
            # obtem o nome da conversa
            name = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="conversation-info-header"]')))
            name = name.text.split("\n")[0]
            # sobe no topo 
            self.scroll_to_top()
            self.save_print(path_out, name)
            # pegar o nome e salvar screenshot
            # chat_list = driver.find_element(By.ID, 'pane-side')
            # chats = chat_list.find_elements(By.XPATH, '//div[@aria-colindex="2"]')
            # primeiro resultado da lista
            # print(chats[-2].text)
        except Exception as err:
            self.driver.quit()
            n_linha = sys.exc_info()[2]
            self.getLogger().error('Na linha {} -{}'.format(n_linha.tb_lineno,err))

    def locate_chat_today(self, path_out):
        """Localiza todos os chats do dia atual e realiza prints

        Args:
            path_out (str): caminho de saida para os prints
        """
        try:
            if self.chat_header:
                # lista de chats encontrados
                chats = []
                SCROLL_PAUSE_TIME = 1
                # Pega tamanho do scroll
                scroll_height = self.driver.execute_script("return document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
                # # Rola ate o fim da pagina
                # driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, {});".format(scroll_height))
                # # Rola até o inicio da pagina
                self.driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, 0);")
                # Define o tamanho de rolagem
                scroll_roll = 1000
                while True:
                    # todos os chats visiveis na página
                    elements = self.driver.find_elements(By.XPATH, '//div[@role="gridcell"]')
                    for element in elements:
                        # verifica hora da ultima mensagem apenas do dia atual
                        if re.search('(2[0-3]|[01]?[0-9]):([0-5]?[0-9])', element.text):
                            # clica na conversa
                            element.click()
                            # abre menu de contexto da conversa
                            ActionChains(self.driver).context_click(element).perform()
                            time.sleep(5)
                            try:
                                element_context = self.driver.find_element(By.XPATH, '//div[@role="application"]')
                            except:
                                element_context = None
                            # marca conversa como não lida
                            if element_context:
                                # não marca como não lida mensagens arquivadas
                                if 'Desarquivar conversa' in element_context.text:
                                    pass
                                # verifica se whatsapp é business
                                elif 'Editar etiqueta' in element_context.text:
                                    ActionChains(self.driver).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
                                else:
                                    ActionChains(self.driver).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
                            # obtem nome da conversa
                            name = element.text.split("\n")[0]
                            name = self.normalizeName(name)
                            # data da conversa
                            date = element.text.split("\n")[1]
                            date_datetime = datetime.datetime.strptime(date,'%d/%m/%Y').date()
                            weekday = calendar.day_name[date_datetime.weekday()]
                            # verifica nome na lista de chats encontrados
                            if name not in chats:
                                # sobe no topo da conversa
                                self.scroll_to_top()
                                # salva os prints das conversas
                                self.save_print(path_out, name)
                                # adiciona nome na lista
                                chats.append(name)
                            else:
                                continue
                    # verifica se chegou no fim da lista de chat
                    if scroll_roll >= scroll_height:
                        break
                    # Rola no tamanho definido
                    self.driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, {});".format(scroll_roll))
                    # Define novo tamanho de rolagem
                    scroll_roll += 1000
                    # Espera página carregar
                    time.sleep(SCROLL_PAUSE_TIME)
        except Exception as err:
            self.driver.quit()
            n_linha = sys.exc_info()[2]
            self.getLogger().error('Na linha {} -{}'.format(n_linha.tb_lineno,err))

    def locate_archived_chats(self):
        """Localiza botão de arquivados e clique nele

        Args:
            path_out (str): caminho de saida para os prints
        
        Returns:
            bool: True para elemento encontrado, False para  elemento não encontrado
        """
        try:
            if self.chat_header:
                self.driver.refresh()
                time.sleep(5)
                # busca o botão de mensagens arquivadas
                # //span[@data-testid="archived"]
                # //div[@role="group"]
                try:
                    element = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@role="group"]')))
                except:
                    element = None
                if element:
                    element.click()
                    return True
                else:
                    return False
        except Exception as err:
            self.driver.quit()
            n_linha = sys.exc_info()[2]
            self.getLogger().error('Na linha {} -{}'.format(n_linha.tb_lineno,err))
            
    def locate_chat_ndays(self, path_out, ndays=3):
        """Localiza todos os chats de n dias antes e realiza prints

        Args:
            path_out (str): caminho de saida para os prints
            ndays (int, optional): Numero de dias. Defaults to 3.
        """
        try:
            if self.chat_header:
                # lista de chats encontrados
                chats = []
                SCROLL_PAUSE_TIME = 1
                # Pega tamanho do scroll
                scroll_height = self.driver.execute_script("return document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
                # # Rola ate o fim da pagina
                # driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, {});".format(scroll_height))
                # # Rola até o inicio da pagina
                self.driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, 0);")
                # Define o tamanho de rolagem
                scroll_roll = 1000
                while True:
                    # todos os chats visiveis na página
                    time.sleep(5)
                    elements = self.driver.find_elements(By.XPATH, '//div[@role="gridcell"]')
                    for element in elements:
                        time.sleep(5)
                        if element.text:
                            # obtem nome da conversa
                            name = element.text.split("\n")[0]
                            name = self.normalizeName(name)
                            now = datetime.datetime.now().date()
                            last_ndays = now - datetime.timedelta(ndays)
                            today = now.day
                            """
                            today_date = now.strftime("%d-%m-%Y") - "27-01-2023"
                            today = 27
                            last_ndays = 20
                            '{}/{}'.format(x, now.strftime("%m/%Y")) - "20-01-2023"
                            now.strftime("%m/%Y") = "01/2023"
                            datetime.datetime.strptime('{}/{}'.format(x, now.strftime("%m/%Y")), '%d/%m/%Y').date() objeto do datetime.date
                            weekday() retorna uma numero da semana {segunda=0,terça=1,quarta=2,quinta=3,sexta=4,sábado=5,domingo=6}
                            datetime.datetime.strptime('{}/{}'.format(20, now.strftime("%m/%Y")), '%d/%m/%Y').date().weekday() = 4
                            range(last_ndays.day,today+1) [20,21,22,23,24,25,26,27]
                            """
                            last_days = {'{}/{}'.format(x, now.strftime("%m/%Y")): DIA_DA_SEMANA[calendar.day_name[datetime.datetime.strptime('{}/{}'.format(x, now.strftime("%m/%Y")), '%d/%m/%Y').date().weekday()]] for x in range(last_ndays.day,today+1)}
                            if len(element.text.split('\n')) > 1:
                                date = element.text.split('\n')[1]
                                weekday = date in last_days.values()
                                date_week = date in last_days.keys()
                                yesterday = date == 'Ontem'
                                hour = re.search('(2[0-3]|[01]?[0-9]):([0-5]?[0-9])', date)
                            else:
                                weekday = element.text in last_days.values()
                                date_week = element.text in last_days.keys()
                                yesterday = element.text == 'Ontem'
                                hour = re.search('(2[0-3]|[01]?[0-9]):([0-5]?[0-9])', element.text)
                            # re.search('(2[0-3]|[01]?[0-9]):([0-5]?[0-9])', date)
                            if hour or yesterday or date_week or weekday:
                                # clica na conversa
                                try:
                                    element.click()
                                except:
                                    continue
                                # abre menu de contexto da conversa
                                ActionChains(self.driver).context_click(element).perform()
                                time.sleep(5)
                                try:
                                    element_context = self.driver.find_element(By.XPATH, '//div[@role="application"]')
                                except:
                                    element_context = None
                                # marca conversa como não lida
                                if element_context:
                                    # não marca como não lida mensagens arquivadas
                                    if 'Desarquivar conversa' in element_context.text:
                                        self.getLogger().info("Conversa arquivada {}".format(name))
                                    # verifica se whatsapp é business
                                    elif 'Editar etiqueta' in element_context.text:
                                        ActionChains(self.driver).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
                                    else:
                                        ActionChains(self.driver).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
                                # verifica nome na lista de chats encontrados
                                if name not in chats:
                                    # sobe no topo da conversa
                                    # scroll_to_top()
                                    # salva os prints das conversas
                                    self.save_print(path_out, name)
                                    # adiciona nome na lista
                                    chats.append(name)
                                else:
                                    continue
                    # verifica se chegou no fim da lista de chat
                    if scroll_roll >= scroll_height:
                        break
                    # Rola no tamanho definido
                    self.driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, {});".format(scroll_roll))
                    # Define novo tamanho de rolagem
                    scroll_roll += 1000
                    # Espera página carregar
                    time.sleep(SCROLL_PAUSE_TIME)
        except Exception as err:
            self.driver.quit()
            n_linha = sys.exc_info()[2]
            self.getLogger().error('Na linha {} -{}'.format(n_linha.tb_lineno,err))

    def locate_all_chat(self, path_out):
        """Localiza todos os chats e realiza prints

        Args:
            path_out (str): caminho de saida para os prints

        """
        try:
            if self.chat_header:
                # lista de chats encontrados
                chats = []
                SCROLL_PAUSE_TIME = 1
                # Pega tamanho do scroll
                scroll_height = self.driver.execute_script("return document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
                # # Rola ate o fim da pagina
                # driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, {});".format(scroll_height))
                # # Rola até o inicio da pagina
                self.driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, 0);")
                # Define o tamanho de rolagem
                scroll_roll = 1000
                while True:
                    # todos os chats visiveis na página
                    elements = self.driver.find_elements(By.XPATH, '//div[@role="gridcell"]')
                    for element in elements:
                        # clica na conversa
                        element.click()
                        # abre menu de contexto da conversa
                        ActionChains(self.driver).context_click(element).perform()
                        time.sleep(5)
                        try:
                            element_context = self.driver.find_element(By.XPATH, '//div[@role="application"]')
                        except:
                            element_context = None
                        # marca conversa como não lida
                        # if element_context:
                        #     if 'Editar etiqueta' in element_context.text:
                        #         ActionChains(driver).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
                        #     else:
                        #         ActionChains(driver).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
                        # obtem nome da conversa
                        name = element.text.split("\n")[0]
                        name = self.normalizeName(name)
                        # verifica nome na lista de chats encontrados
                        if name not in chats:
                            # sobe até o topo do chat
                            self.scroll_to_top()
                            # salva os prints
                            self.save_print(path_out, name)
                            # adiciona nome na lista
                            chats.append(name)
                        else:
                            continue
                    # verifica se chegou no fim da lista de chat
                    if scroll_roll >= scroll_height:
                        break
                    # Rola no tamanho definido
                    self.driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, {});".format(scroll_roll))
                    # Define novo tamanho de rolagem
                    scroll_roll += 1000
                    # Espera página carregar
                    time.sleep(SCROLL_PAUSE_TIME)
        except Exception as err:
            self.driver.quit()
            n_linha = sys.exc_info()[2]
            self.getLogger().error('Na linha {} -{}'.format(n_linha.tb_lineno,err))

    def locate_all_chat_by_name(self, path_out):
        """Percorre toda lista de chat procurando pelo nome digitado

        Args:
            path_out (string): caminho para salvar print
        """
        try:
            while True:
                print("Digite o nome exatamente como está salvo no contato")
                read_input = input("Digite o nome da conversa ou 0 para encerrar: ")
                if read_input == "0":
                    break
                SCROLL_PAUSE_TIME = 0.5
                # Pega tamanho do scroll
                scroll_height = self.driver.execute_script("return document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
                # # Rola ate o fim da pagina
                # driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, {});".format(scroll_height))
                # # Rola até o inicio da pagina
                self.driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, 0);")
                # Define o tamanho de rolagem
                scroll_roll = 1000
                while True:
                    # try:
                    #     find = driver.execute_script("document.evaluate('//span[contains(@title, 'Mateus Nunes')]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue" )
                    # except:
                    #     find = None
                    # localiza o nome digitado na posição atual
                    check, name_chat = self.locate_chat(read_input)
                    name_chat = self.normalizeName(name_chat)
                    # Rola no tamanho definido
                    self.driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, {});".format(scroll_roll))
                    # Define novo tamanho de rolagem
                    scroll_roll += 1000
                    # Espera página carregar
                    time.sleep(SCROLL_PAUSE_TIME)
                    # Verifica se chegou no fim ou encontrou a conversa
                    if check:
                        self.getLogger().info("Conversa com {} encontrada".format(read_input))
                        break
                    elif scroll_roll >= scroll_height:
                        break
                if check:
                    # sobe ate o topo 
                    self.scroll_to_top()
                    # salva prints
                    self.save_print(path_out, name_chat)
                else:
                    self.getLogger().warning("Conversa com {} não encontrada".format(read_input))
        except Exception as err:
            self.driver.quit()
            n_linha = sys.exc_info()[2]
            self.getLogger().error('Na linha {} -{}'.format(n_linha.tb_lineno,err))
            
    def save_print(self, path_out, name:str):
        """Salva print de conversa

        Args:
            path_out (string): caminho da pasta onde será salvo a imagem
            name (string): nome do arquivo
        """
        try:
            # retira caracteres especiais do nome
            name = self.normalizeName(name)
            # obtem data atual
            now = datetime.datetime.now()
            # obtem ano
            year = now.year
            init_backup = now.strftime("%m/%d/%Y, %H:%M:%S")
            now = now.strftime("%d-%m-%Y")
            # monta o caminho da pasta do mês - exemplo: administrativo-geral/ADMINISTRATIVO-GERAL/02 DPTO TI.GTI/10 - CONTROLE FERRAMENTAS/WHATSAPP/2023
            path_year = os.path.join(path_out, str(year))
            # verifica se pasta do ano não existe e cria a pasta
            if not os.path.isdir(path_year):
                os.mkdir(path_year)
            # monta o caminho da pasta do mês - exemplo: administrativo-geral/ADMINISTRATIVO-GERAL/02 DPTO TI.GTI/10 - CONTROLE FERRAMENTAS/WHATSAPP/NOVEMBRO
            path_month = os.path.join(path_year, MESES[now.split('-')[1]])
            # verifica se pasta do mes não existe e cria a pasta
            if not os.path.isdir(path_month):
                os.mkdir(path_month)
            # monta o caminho da pasta do mês - exemplo: administrativo-geral/ADMINISTRATIVO-GERAL/02 DPTO TI.GTI/10 - CONTROLE FERRAMENTAS/WHATSAPP/NOVEMBRO/01-11-2022
            path_today = os.path.join(path_month, now)
            # verifica se pasta do dia não existe e cria a pasta
            if not os.path.isdir(path_today):
                os.mkdir(path_today)
            # monta o caminho da pasta da conversa - exemplo: administrativo-geral/ADMINISTRATIVO-GERAL/02 DPTO TI.GTI/10 - CONTROLE FERRAMENTAS/WHATSAPP/NOVEMBRO/01-11-2022/nome_da_conversa
            path_chat = os.path.join(path_today, name)
            # verifica se pasta da conversa não existe e cria a pasta
            if not os.path.isdir(path_chat):
                os.mkdir(path_chat)
            # abre arquivo com o nome do terminal
            file_host = open('{}/{}.txt'.format(path_chat, self.hostname), 'a', encoding='utf-8')
            # registra hora que iniciou backup no arquivo
            file_host.write('BACKUP INICIADO {}\n'.format(init_backup))
            time.sleep(5)
            i = 1
            scroll_roll = 500
            # Pega tamanho total do scroll
            scroll_height = self.driver.execute_script("return document.evaluate('//div[@data-testid=\"conversation-panel-messages\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
            try:
                element_name = self.driver.find_element(By.XPATH, '//span[@data-testid="conversation-info-header-chat-title"]')
            except:
                element_name = None
            file_host.write("Nome que será colocado nos arquivos do print: {}\n".format(name))
            if element_name:
                # print(element_name.text)
                file_host.write("Nome encontrado na conversa aberta no navegador: {}\n".format(element_name.text))
            while True:
                # pega conversa
                element = self.driver.find_element(By.ID, 'main')
                # monta caminho do arquivo da imagem - exemplo: administrativo-geral/ADMINISTRATIVO-GERAL/02 DPTO TI.GTI/10 - CONTROLE FERRAMENTAS/WHATSAPP/NOVEMBRO/01-11-2022/nome_numeroprint
                print_chat = os.path.join(path_chat, '{}_{}.png'.format(name, i))
                # salva print da conversa
                # element.screenshot(print_chat)
                self.getLogger().info("Print salvo em {}".format(print_chat))
                # rola para próxima página da conversa
                self.driver.execute_script("return document.evaluate('//div[@data-testid=\"conversation-panel-messages\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, {})".format(scroll_roll))
                # compara posição atual com o tamanho total para verificar se chegou no final
                if scroll_roll >= scroll_height:
                    break
                i += 1
                scroll_roll += 500
            # atualiza tempo
            now = datetime.datetime.now()
            finish_backup = now.strftime("%m/%d/%Y, %H:%M:%S")
            # registra hora que finalizou backup no arquivo
            file_host.write('BACKUP finalizado {}\n'.format(finish_backup))
            # fecha arquivo
            file_host.close()
        except Exception as err:
            self.driver.quit()
            n_linha = sys.exc_info()[2]
            self.getLogger().error('Na linha {} -{}'.format(n_linha.tb_lineno,err))

    def scroll_to_top(self):
        """Rola até o topo da conversa selecionada
        """
        try:
            if self.chat_header:
                SCROLL_PAUSE_TIME = 10
                #document.evaluate('//div[@data-testid='conversation-panel-messages']', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight
                # x = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='conversation-panel-messages']")))
                
                # pega tamanho total do scroll
                last_height = self.driver.execute_script("return document.evaluate('//div[@data-testid=\"conversation-panel-messages\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")

                while True:
                    # executa rolagem na página
                    self.driver.execute_script("document.evaluate('//div[@data-testid=\"conversation-panel-messages\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, 0);")

                    # espera pagina carregar
                    time.sleep(SCROLL_PAUSE_TIME)

                    # calcula nova posição e compara com a ultima posição
                    new_height = self.driver.execute_script("return document.evaluate('//div[@data-testid=\"conversation-panel-messages\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
        except Exception as err:
            self.driver.quit()
            n_linha = sys.exc_info()[2]
            self.getLogger().error('Na linha {} -{}'.format(n_linha.tb_lineno,err))

    def scroll_to_bottom_chat_list(self):
        """Rola até o final da lista de chat
        """
        try:
            if self.chat_header:
                SCROLL_PAUSE_TIME = 0.5
                # Pega tamanho do scroll
                scroll_height = self.driver.execute_script("return document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
                # Rola ate o fim da pagina
                self.driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, {});".format(scroll_height))
                # Rola até o inicio da pagina
                self.driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, 0);")
                # Define o tamanho de rolagem
                scroll_roll = 1000
                while True:
                    # Rola no tamanho definido
                    self.driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, {});".format(scroll_roll))
                    # Define novo tamanho de rolagem
                    scroll_roll += 1000
                    # Espera página carregar
                    time.sleep(SCROLL_PAUSE_TIME)
                    # Verifica se chegou no fim
                    if scroll_roll >= scroll_height:
                        break
        except Exception as err:
            self.driver.quit()
            n_linha = sys.exc_info()[2]
            self.getLogger().error('Na linha {} -{}'.format(n_linha.tb_lineno,err))

if __name__ == '__main__':
    scrapperWAPP = ScraperWhatsapp()
    if scrapperWAPP.check_internet():
        try:
            # verifica sistema operacional
            if os.name == 'nt':
                print('Windows')
                # caminho de salvamento no windows
                path_escolhido = os.path.join(os.environ['USERPROFILE'], 'Pictures')
            else:
                print('Linux')
                # caminho de salvamento no linux
                path_escolhido = os.path.join(os.environ['HOME'], 'Imagens')
            print("!!!!!"*30+"NÃO\tFECHE\tESTA\tJANELA"+"!!!!!"*30)
            print("#"*20+"ATENÇÃO"+"#"*20)
            print("Máquina será desligada após finalizado o backup")
            scrapperWAPP.locate_chat_ndays(path_escolhido)
            if scrapperWAPP.locate_archived_chats():
                scrapperWAPP.getLogger().info("Iniciando conversas arquivadas {}".format(scrapperWAPP.timestamp()))
                scrapperWAPP.locate_chat_ndays(path_escolhido)
                scrapperWAPP.getLogger().info("Finalizando conversas arquivadas {}".format(scrapperWAPP.timestamp()))
            # locate_all_chat(path_out)
            # locate_all_chat_by_name(path_out)
            # name = input("Digite o nome -> ")
            # locate_chat_ignore_case(name, path_out)
            scrapperWAPP.driver.quit()
            # FINALIZA CONTAGEM DE TEMPO
            t_f = scrapperWAPP.finishCountTime(scrapperWAPP.t_i)
            segundos = t_f%60
            minutos = int(t_f/60)
            if minutos > 60:
                horas = int(minutos/60)
                minutos = minutos%60
            else:
                horas = 0
            scrapperWAPP.getLogger().info("BACKUP FINALIZADO - {} - Executado em {} horas {} minutos {} segundos".format(scrapperWAPP.timestamp(),horas, minutos, segundos))
        except Exception as err:
            scrapperWAPP.driver.quit()
            n_linha = sys.exc_info()[2]
            scrapperWAPP.getLogger().error('Na linha {} -{}'.format(n_linha.tb_lineno,err))
    else:
        raise ConnectionError("Internet fora do ar")