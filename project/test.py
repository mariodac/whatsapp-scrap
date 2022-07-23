from scraper_wa import *
# scroll_to_bottom_chat_list()
height = driver.execute_script("return document.evaluate('//div[@id=\"pane-side\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
element = driver.find_element(By.XPATH, "//div[@data-testid='chat-list']")
element.send_keys(Keys.PAGE_DOWN)
elements = [element for element in driver.find_elements(By.XPATH, "//div[@data-testid='cell-frame-container']")]

find_elements = []
for element in elements:
    driver.execute_script("arguments[0].scrollIntoView();", element)
    element.click()
    if re.search('^(([0]?[1-9]|1[0-2])(:)([0-5][0-9]))$', element.text):
        find_elements.append(element)