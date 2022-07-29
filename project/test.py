#Desenvolvido por Mario Cabral em 23/07/2022
#Atualização: 29/07/2022.
#Abre whatsapp web e salva print das conversas pesquisadas pelo usuario

from scraper_wa import *

# scroll_to_bottom_chat_list()
# height = driver.execute_script("return document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
# element = driver.find_element(By.XPATH, "//div[@data-testid='chat-list']")
# elements = [element for element in driver.find_elements(By.XPATH, "//div[@data-testid='cell-frame-container']")]

# find_elements = []
# for element in elements:
#     driver.execute_script("arguments[0].scrollIntoView();", element)
#     element.click()
#     if re.search('^(([0]?[1-9]|1[0-2])(:)([0-5][0-9]))$', element.text):
#         find_elements.append(element)
path_out = r"D:\Imagens"

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
        try:
            find = driver.execute_script("document.evaluate('//span[contains(@title, 'Mateus Nunes')]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue" )
        except:
            pass
        check, name_chat = locate_chat(read_input)
        # Rola no tamanho definido
        driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, {});".format(scroll_roll))
        # Define novo tamanho de rolagem
        scroll_roll += 1000
        # Espera página carregar
        time.sleep(SCROLL_PAUSE_TIME)
        # Verifica se chegou no fim
        if check:
            break
    scroll_to_top()
    # //*[@data-testid="down"]
    save_print(path_out, name_chat)