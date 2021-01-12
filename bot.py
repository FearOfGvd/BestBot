import os
import bs4
import sys
import time
import atexit
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from configparser import ConfigParser

def exit_handler():
    config.remove_section('link')
    config.remove_section('security')
    with open(file, 'w') as configfile:
        config.write(configfile)
    print('Config.ini information has been cleared.')
    driver.quit()

file = 'config.ini'
config = ConfigParser()
config.read(file)

accountSid = ''
authToken = ''
client = Client(accountSid, authToken)

while not config.has_section('phone') or not config.has_section('directory') or not config.has_section('link') or not config.has_section('security'):
    if not config.has_section('phone'):
        phone_num_receiver = input('Enter your mobile phone number to receive alerts, or enter 0 deny phone notifications. (Format = +1XXXXXXXXXX): ')
        if '+1' in phone_num_receiver and len(phone_num_receiver) == 12:
            config.add_section('phone')
            config.set('phone', 'number', phone_num_receiver)

            with open(file, 'w') as configfile:
                config.write(configfile)

            print(config['phone'])
            print(list(config['phone']))
            print('Phone number to receive texts: ' + config['phone']['number'])
        elif input(phone_num_receiver) == 0:
            break
        else:
            continue

    if not config.has_section('directory'):
        directory_receiver = input('Enter your Firefox web driver path. (Format = "C:\\Users\\(user)\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\XXXXXXXX.default-release"): ')
        if 'Roaming\Mozilla\Firefox\Profiles' in directory_receiver:
            config.add_section('directory')
            config.set('directory', 'path', directory_receiver)

            with open(file, 'w') as configfile:
                config.write(configfile)

            print(config['directory'])
            print(list(config['directory']))
            print('Firefox web driver path: ' + config['directory']['path'])
        else:
            continue
    
    if not config.has_section('link'):
        link_receiver = input('Enter the product link. (Format = https://www.bestbuy.com/site/searchpage.jsp?...): ')
        if 'https://www.bestbuy.com/site/' in link_receiver:
            config.add_section('link')
            config.set('link', 'product', link_receiver)

            with open(file, 'w') as configfile:
                config.write(configfile)

            print(config['link'])
            print(list(config['link']))
            print('Best Buy product link: ' + config['link']['product'])
        else:
            continue
    
    if not config.has_section('security'):
        security_receiver = input('Enter your credit card\'s security code. (Format = "123"): ')
        if len(security_receiver) == 3:
            config.add_section('security')
            config.set('security', 'code', security_receiver)

            with open(file, 'w') as configfile:
                config.write(configfile)

            print(config['security'])
            print(list(config['security']))
        else:
            continue

def timeSleep(x, driver):
    start = time.time()
    # checks for page refresh
    for i in range(x, 0, 1):
        sys.stdout.write('\r')
        sys.stdout.flush()
        time.sleep(1)
    driver.refresh()
    sys.stdout.write('\r')
    end = time.time()
    final_time = end-start
    sys.stdout.write('Page took {:0.2f} seconds to refresh\n'.format(final_time))
    sys.stdout.flush()

def createDriver():
    # creates web driver
    options = Options()
    options.headless = True  # change to false to see the firefox browser
    profile = webdriver.FirefoxProfile(config['directory']['path'])
    driver = webdriver.Firefox(profile, options = options, executable_path = GeckoDriverManager().install())
    return driver

def driverWait(driver, findType, selector):
    # wait for web driver settings
    while True:
        if findType == 'css':
            try:
                driver.find_element_by_css_selector(selector).click()
                break
            except NoSuchElementException:
                driver.implicitly_wait(0.2)

        elif findType == 'name':
            try:
                driver.find_element_by_name(selector).click()
                break
            except NoSuchElementException:
                driver.implicitly_wait(0.2)


def findingCards(driver):
    # scans product card
    driver.get(config['link']['product'])
    while True:
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, 'html.parser')
        wait = WebDriverWait(driver, 5) # original value is 15
        wait2 = WebDriverWait(driver, 2)
        
        try:
            findAllCards = soup.find('button', {'class': 'btn btn-primary btn-sm btn-block btn-leading-ficon add-to-cart-button'})
            if findAllCards:
                print(f'Button Found: {findAllCards.get_text()}')
                client.messages.create(to = config['phone']['number'], from_ = '', body = 'Item '+config['link']['product']+' is in stock!')

                # click add to cart
                driverWait(driver, 'css', '.add-to-cart-button')
                time.sleep(1) # original value is 2

                # going to cart
                driver.get('https://www.bestbuy.com/cart')

                # check if item was removed from cart
                try:
                    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='btn btn-lg btn-block btn-primary']")))
                    driver.find_element_by_xpath("//*[@class='btn btn-lg btn-block btn-primary']").click()
                    print('Item Is Still In Cart.')
                except (NoSuchElementException, TimeoutException):
                    print('Item is not in cart anymore. Retrying..')
                    timeSleep(1, driver) # original value is 3
                    findingCards(driver)
                    return

                # log into account
                print('Attempting to Login.')

                # clicks the shipping option
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#fulfillment_1losStandard0')))
                    time.sleep(1)
                    driverWait(driver, 'css', '#fulfillment_1losStandard0')
                    print('Clicking Shipping Option.')
                except (NoSuchElementException, TimeoutException):
                    pass

                # tries to add cvv number
                try:
                    print('Trying CVV Number.')
                    security_code = driver.find_element_by_id('credit-card-cvv')
                    time.sleep(1)
                    security_code.send_keys(config['security']['code'])  # You can enter your CVV number here.
                except (NoSuchElementException, TimeoutException):
                    pass

                # text message updates
                try:
                    wait2.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#text-updates')))
                    driverWait(driver, 'css', '#text-updates')
                    print('Selecting Text Updates.')
                except (NoSuchElementException, TimeoutException):
                    pass

                # checksout product
                try:
                    wait2.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn-primary')))
                    driverWait(driver, 'css', '.btn-primary')
                except (NoSuchElementException, TimeoutException, ElementNotInteractableException):
                    try:
                        wait2.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn-secondary')))
                        driverWait(driver, 'css', '.btn-secondary')
                        timeSleep(1, driver) # original value is 5
                        wait2.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn-primary')))
                        time.sleep(1)
                        driverWait(driver, 'css', '.btn-primary')
                    except (NoSuchElementException, TimeoutException, ElementNotInteractableException):
                        print('Could Not Complete Checkout.')

                # completed checkout
                print('Order Placed!')
                atexit.register(exit_handler)

                try:
                    client.messages.create(to = config['phone']['number'], from_ = '', body = 'Order for '+config['link']['product']+' has been placed!')
                except (NameError, TwilioRestException):
                    pass
                for i in range(1): # original value is 3
                    print('\a')
                    time.sleep(1)
                time.sleep(1) # original value is 1800
                driver.quit()
                exit()
            else:
                pass

        except NoSuchElementException:
            pass
        timeSleep(5, driver)

if __name__ == '__main__':
    try:
        driver = createDriver()
        findingCards(driver)
    except KeyboardInterrupt:
        print('\nKeyboardInterrupt')
        atexit.register(exit_handler)
        sys.exit(1)