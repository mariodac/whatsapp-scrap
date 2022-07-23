import re, time
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

#scan QR code from phone
wait = WebDriverWait(driver, 60)

chat_header = wait.until(EC.visibility_of_element_located((By.XPATH, "//header[@data-testid='chatlist-header']")))

def scroll_to_top():
    """Scrolls to the top of the chat currently open in the WhatsApp Web
    interface
    """
    if chat_header:
        SCROLL_PAUSE_TIME = 1
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

        # Get scroll height
        last_height = driver.execute_script("return document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scroll(0, {});".format(last_height))

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height =  driver.execute_script("return document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

def locate_chat(name):
    """Find the chat with a given name in WhatsApp web and
    click on that chat
    """
    if chat_header:
        x_arg = '//span[contains(@title, '+ '"' +name + '"'+ ')]'
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