import re, time, os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

#initial setup
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

#login to WhatsApp web
driver.get("https://web.whatsapp.com/")

# wait para scanear QR code do celular
wait = WebDriverWait(driver, 600)

# 
chat_header = wait.until(EC.visibility_of_element_located((By.XPATH, "//header[@data-testid='chatlist-header']")))

def locate_chat(name):
    """Find the chat with a given name in WhatsApp web and
    click on that chat
    """
    wait = WebDriverWait(driver, 10)
    try: 
        x_arg = '//span[contains(@title, \'{}\')]'.format(name)
        # print(x_arg)
        person_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
        # person_title = wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, name)))
        print(person_title)
        person_title.click()
        time.sleep(5)
        return True, person_title.text
    except Exception as err:
        # print(err)
        print("Elemento não encontrado")
        return False, None

def locate_all_chat_by_name(path_out):
    pass

def save_print(path_out, name):
    time.sleep(5)
    i = 1
    scroll_roll = 500
    # Pega tamanho do scroll
    scroll_height = driver.execute_script("return document.evaluate('//div[@data-testid=\"conversation-panel-messages\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
    while True:
        element = driver.find_element(By.ID, 'main')
        element.screenshot(os.path.join(path_out, '{}_{}.png'.format(name, i)))
        driver.execute_script("return document.evaluate('//div[@data-testid=\"conversation-panel-messages\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, {})".format(scroll_roll))
        if scroll_roll >= scroll_height:
            break
        i += 1
        scroll_roll += 500

def scroll_to_top():
    """Scrolls to the top of the chat currently open in the WhatsApp Web
    interface
    """
    if chat_header:
        SCROLL_PAUSE_TIME = 5
        "{}"
        #document.evaluate('//div[@data-testid='conversation-panel-messages']', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight
        x = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='conversation-panel-messages']")))
        
        # Get scroll height
        last_height = driver.execute_script("return document.evaluate('//div[@data-testid=\"conversation-panel-messages\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")

        while True:
            driver.execute_script("document.evaluate('//div[@data-testid=\"conversation-panel-messages\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, 0);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.evaluate('//div[@data-testid=\"conversation-panel-messages\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

def scroll_to_bottom_chat_list():
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