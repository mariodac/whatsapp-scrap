import re, time, os, socket, logging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

# configuração inicial webbdriver
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# configuração logger
# hostname da máquina que executa o script
hostname = socket.gethostname()
# formato do log
log_format = '%(hostname)s - %(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger('scraper_wa')
# configura nivel de log
logger.setLevel('DEBUG')
try:
	# verifica sistema operacional
    if os.name == 'nt':
        path_log = os.environ['TEMP']
    else:
        path_log = '/var/log/'
except Exception as err:
	logger.error(err)
path_hostname = os.path.join(path_log, "scraper_wa-{}".format(hostname))
# nome do arquivo de log
file_handler = logging.FileHandler("{}.log".format(path_hostname))
# aplica formato 
formatter = logging.Formatter(log_format, defaults={"hostname": hostname})
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

#login to WhatsApp web
driver.get("https://web.whatsapp.com/")

# wait para scanear QR code do celular
wait = WebDriverWait(driver, 600)

# espera para carregar interface do whatsapp
chat_header = wait.until(EC.visibility_of_element_located((By.XPATH, "//header[@data-testid='chatlist-header']")))

def locate_chat(name:str):
    """Localiza conversa com determinado nome e clica nela

    Args:
        name (string): nome da conversa

    Returns:
        bool: True para elemento encontrado, False para  elemento não encontrado
        string: nome da conversa
    """
    try:
        if chat_header:
            # wait para carregar o chat 
            wait = WebDriverWait(driver, 10)
            try: 
                x_arg = '//span[contains(@title, \'{}\')]'.format(name)
                # print(x_arg)
                person_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
                # print(person_title)
                person_title.click()
                # para carregar o chat 
                time.sleep(5)
                # caso não encontre o elemento retorna verdadeiro e nome do chat
                return True, person_title.text
            except:
                # print("Elemento não encontrado")
                # caso não encontre o elemento retorna false e nulo
                return False, None
    except Exception as err:
        logger.error(err)

def locate_chat_ignore_case(name:str):
    try:
        wait = WebDriverWait(driver, 10)
        search_chat = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="chat-list-search"]')))
        search_chat.click()
        time.sleep(1)
        search_chat.send_keys(name)
        print()
    except Exception as err:
        logger.error(err)

def locate_chat_today(path_out):
    try:
        if chat_header:
            # lista de chats encontrados
            chats = []
            SCROLL_PAUSE_TIME = 1
            # Pega tamanho do scroll
            scroll_height = driver.execute_script("return document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
            # # Rola ate o fim da pagina
            # driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, {});".format(scroll_height))
            # # Rola até o inicio da pagina
            driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, 0);")
            # Define o tamanho de rolagem
            scroll_roll = 1000
            while True:
                # todos os chats visiveis na página
                elements = driver.find_elements(By.XPATH, '//div[@role="gridcell"]')
                for element in elements:
                    # verifica hora da ultima mensagem apenas do dia atual
                    if re.search('(2[0-3]|[01]?[0-9]):([0-5]?[0-9])', element.text):
                        element.click()
                        # obtem nome da conversa
                        name = element.text.split("\n")[0]
                        # verifica nome na lista de chats encontrados
                        if name not in chats:
                            scroll_to_top()
                            save_print(path_out, name)
                            chats.append(name)
                        else:
                            continue
                # verifica se chegou no fim da lista de chat
                if scroll_roll >= scroll_height:
                    break
                # Rola no tamanho definido
                driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, {});".format(scroll_roll))
                # Define novo tamanho de rolagem
                scroll_roll += 1000
                # Espera página carregar
                time.sleep(SCROLL_PAUSE_TIME)
    except Exception as err:
        logger.error(err)

def locate_all_chat_by_name(path_out):
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
            scroll_height = driver.execute_script("return document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
            # # Rola ate o fim da pagina
            # driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, {});".format(scroll_height))
            # # Rola até o inicio da pagina
            driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, 0);")
            # Define o tamanho de rolagem
            scroll_roll = 1000
            while True:
                # try:
                #     find = driver.execute_script("document.evaluate('//span[contains(@title, 'Mateus Nunes')]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue" )
                # except:
                #     find = None
                # localiza o nome digitado na posição atual
                check, name_chat = locate_chat(read_input)
                # Rola no tamanho definido
                driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, {});".format(scroll_roll))
                # Define novo tamanho de rolagem
                scroll_roll += 1000
                # Espera página carregar
                time.sleep(SCROLL_PAUSE_TIME)
                # Verifica se chegou no fim ou encontrou a conversa
                if check:
                    logger.info("Conversa com {} encontrada".format(read_input))
                    break
                elif scroll_roll >= scroll_height:
                    break
            if check:
                scroll_to_top()
                save_print(path_out, name_chat)
            else:
                logger.warning("Conversa com {} não encontrada".format(read_input))
    except Exception as err:
        logger.error(err)

def save_print(path_out, name):
    """Salva print de conversa

    Args:
        path_out (string): caminho da pasta onde será salvo a imagem
        name (string): nome do arquivo
    """
    time.sleep(5)
    i = 1
    scroll_roll = 500
    # Pega tamanho total do scroll
    scroll_height = driver.execute_script("return document.evaluate('//div[@data-testid=\"conversation-panel-messages\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
    while True:
        # pega conversa
        element = driver.find_element(By.ID, 'main')
        print_chat = os.path.join(path_out, '{}_{}.png'.format(name, i))
        # salva print da conversa
        element.screenshot(print_chat)
        logger.info("Print salvo em {}".format(print_chat))
        # rola para próxima página
        driver.execute_script("return document.evaluate('//div[@data-testid=\"conversation-panel-messages\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, {})".format(scroll_roll))
        # compara posição atual com o tamanho total
        if scroll_roll >= scroll_height:
            break
        i += 1
        scroll_roll += 500

def scroll_to_top():
    """Rola até o topo da conversa selecionada
    """
    if chat_header:
        SCROLL_PAUSE_TIME = 5
        #document.evaluate('//div[@data-testid='conversation-panel-messages']', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight
        # x = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='conversation-panel-messages']")))
        
        # pega tamanho total do scroll
        last_height = driver.execute_script("return document.evaluate('//div[@data-testid=\"conversation-panel-messages\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")

        while True:
            driver.execute_script("document.evaluate('//div[@data-testid=\"conversation-panel-messages\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, 0);")

            # espera pagina carregar
            time.sleep(SCROLL_PAUSE_TIME)

            # calcula nova posição e compara com a ultima posição
            new_height = driver.execute_script("return document.evaluate('//div[@data-testid=\"conversation-panel-messages\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

def scroll_to_bottom_chat_list():
    """Rola até o final da lista de chat
    """
    if chat_header:
        SCROLL_PAUSE_TIME = 0.5
        # Pega tamanho do scroll
        scroll_height = driver.execute_script("return document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
        # Rola ate o fim da pagina
        driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, {});".format(scroll_height))
        # Rola até o inicio da pagina
        driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, 0);")
        # Define o tamanho de rolagem
        scroll_roll = 1000
        while True:
            # Rola no tamanho definido
            driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, {});".format(scroll_roll))
            # Define novo tamanho de rolagem
            scroll_roll += 1000
            # Espera página carregar
            time.sleep(SCROLL_PAUSE_TIME)
            # Verifica se chegou no fim
            if scroll_roll >= scroll_height:
                break

def locate_chat2(name):
    """Find the chat with a given name in WhatsApp web and
    click on that chat
    """
    if chat_header:
        x_arg = '//span[(@title, '+ '"' +name + '"'+ ')]'
        print(x_arg)
        person_title = wait.until(EC.presence_of_element_located((
            By.XPATH, x_arg)))
        print(person_title)
        person_title.click()
        elements = driver.find_elements(By.XPATH, "//div[@role='gridcell']")
        # elements = driver.find_elements(By.XPATH, "//*[matches(@text,'^(([0]?[1-9]|1[0-2])(:)([0-5][0-9]))$')]")
        find_elements = []
        for element in elements:
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            if re.search('^(([0]?[1-9]|1[0-2])(:)([0-5][0-9]))$', element.text):
                find_elements.append(element)