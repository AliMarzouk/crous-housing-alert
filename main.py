from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List

FROM_ADDRESS = 'crous.housing.bot@local.host'


def get_number_search_results() -> int:
    driver = webdriver.Firefox()
    driver.get("https://trouverunlogement.lescrous.fr")
    wait = WebDriverWait(driver, 10)
    elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#PlaceAutocomplete + div input")))
    elem.clear()
    elem.send_keys('Île-de-France')
    suggestion = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "#PlaceAutocomplete + div .PlaceAutocomplete__list:not(.hidden) li")))
    suggestion.click()
    for e in driver.find_elements(By.TAG_NAME, "button"):
        if e.text == "Lancer une recherche":
            e.click()
    search_result_title_elem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "SearchResults-desktop")))
    search_result_title_text = search_result_title_elem.text
    driver.close()
    return 0 if search_result_title_text.split(' ')[0] == 'Aucun' else int(search_result_title_text.split(' ')[0])


def send_email(to_addresses: List[str], nb_results: int):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    port_number = 8025
    msg = MIMEMultipart()
    msg['From'] = FROM_ADDRESS
    msg['To'] = ';'.join(to_addresses)
    msg['Subject'] = '[CROUS BOT] - Results found'
    message = f'{nb_results} result(s) were found.'
    msg.attach(MIMEText(message))
    mailserver = smtplib.SMTP('localhost', port_number)
    mailserver.sendmail(FROM_ADDRESS, to_addresses, msg.as_string())
    mailserver.quit()
