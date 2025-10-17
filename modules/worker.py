from DrissionPage import ChromiumPage, ChromiumOptions, SessionPage
from DrissionPage.errors import ElementNotFoundError, PageDisconnectedError
from DrissionPage.common import Actions
from modules import proxy as px
from modules.RecaptchaSolver import RecaptchaSolver
from time import sleep
from modules.config import LOGIN_URL, ENABLE_PROXY
from random import randint
from datetime import datetime, timedelta
import pause

class ValWorker():
    def __init__(self, name, phone, email, agent):
        try:
            co = ChromiumOptions().auto_port().set_user_agent(agent)
            if ENABLE_PROXY:
                prox_data = px.get_single()
                print(f"Using : {prox_data}")
                co = ChromiumOptions().auto_port().set_proxy(prox_data)
            self.driver = ChromiumPage(co)
            self.recapthaSolver = RecaptchaSolver(self.driver)
            self.proxy = prox_data if ENABLE_PROXY else ""
            self.name = name
            self.phone = phone
            self.email = email 
            self.result = ""
            
        except Exception as e:
            print(f"Error occured on initializing worker, details {e}")
    
    def start(self):
        try:
            # self.driver.set.window.mini()
            self.driver.get(
                url=LOGIN_URL,
                show_errmsg=False, 
                retry=None, 
                interval=None,
                timeout=30)
            t = datetime.today()
            start = datetime(t.year, t.month, t.day,t.hour,59,59)
            pause.until(start)
            sleep(0.5)
            self.driver.refresh()
        except TimeoutError:
            print("Error timeout")
            self.result = "Proxy Timeout Error"
            self.set_temp_result()
            self.driver.close()
        except ConnectionError:
            print("Error connection from proxy")
            self.result = "Proxy Timeout Error"
            self.set_temp_result()
            self.driver.close()
        except PageDisconnectedError:
            print("Error connection from proxy")
            self.result = "Proxy Timeout Error"
            self.set_temp_result()
            self.driver.close()
        except Exception as e:
            print(type(e))
            print("Continuing")
            
        # Wait for 10.00, keep refreshing
        try:
            tries = 0
            ready = self.check_timer()
            while tries < 30 and not ready :
                self.driver.refresh()
                sleep(1.5)
                ready = self.check_timer()
                tries += 1
                print(f"Refresh count : {tries}")
            if tries >= 30 and not ready:
                self.driver.close()
        except Exception as e:
            print(f"Error occured, {e}")
            
        try:
            print(f"Starting : {tries}")
            tries = 0
            result = False
            while tries < 3 and result == False:
                result = self.insert_creds()
                tries += 1
                
            if tries == 3 and result == False:
                self.result = "Proxy Timeout Error"
                self.set_temp_result()
                self.driver.close()
            print("Done input")
        except Exception as e:
            print("Final error occured when entering credentials")
            
            
        # try:
        #     self.solve_captcha()
        # except PageDisconnectedError:
        #     print("Error connection from proxy")
        #     self.result = "Proxy Timeout Error"
        #     self.set_temp_result()
        #     self.driver.close()
        # except Exception as e:
        #     print(type(e))
        #     print("Error solving captcha")
        
        # self.click_continue()
        # self.result = self.check_result()
        # self.set_temp_result()
        print(self.name)
        sleep(100)
        self.driver.get_screenshot(name=f"Result-{self.name}")
        sleep(10)
    
    def check_result(self):
        result = self.driver.html
        if "We are not able to validate the information provided. Please try again." in result:
            return "NOT"
        elif "Your account is already registered" in result:
            return "VALID"
        else:
            return "Unknown result"
    
    def check_timer(self):
        result = self.driver.html
        if "Saat ini toko sedang tutup" in result:
            return False
        return True
    
    def solve_captcha(self):
        html_page = self.driver.html
        try:
            while "reCAPTCHA" not in html_page:
                sleep(1)
                html_page = self.driver.html
            sleep(3)
            self.recapthaSolver.solveCaptcha()
        except ElementNotFoundError:
            print("Element not found, trying to continue")
        except Exception as e:
            print(type(e))
            print("continuing from captcha")
            
    def insert_creds(self) -> bool:
        try:
            self.driver.ele('#name').input(self.name)
            self.driver.ele('#phone').input(self.phone)
            self.driver.ele('#email').input(self.email)
            self.driver.ele("text:Dapatkan").click()
            return True
        except:
            print("Error entering credentials")
            return False
    def click_continue(self):
        try:
            self.driver.ele("text=Continue").click()
            sleep(randint(3,10))
        except Exception:
            print("Error occured when clicking continue ")
    
    def set_temp_result(self):
        try:
            with open("data/temp_result.txt", 'a') as g:
                g.write(f"'{self.card_num}',{self.code},{self.result},{self.proxy}\n")
        except:
            print("Error saving temp result")
    # def check_results(self):
        