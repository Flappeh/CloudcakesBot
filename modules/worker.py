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

class PenuhError(Exception):
    def __init__(self, message, errors):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
            
        # Now for your custom code...
        self.errors = errors
        
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
        except PageDisconnectedError:
            print("Error connection from proxy")
            self.result = "Proxy Timeout Error"
            self.set_temp_result()
            self.driver.close()
        except Exception as e:
            print(type(e))
            print("Continuing")
            
        try:
            tries = 0
            result = False
            while tries < 10 and result == False:
                self.driver.refresh()
                sleep(0.3)
                self.insert_creds()
                result = self.check_result()
                tries += 1
                
            if tries == 3 and result == False:
                self.result = "Proxy Timeout Error"
                self.driver.close()
            
            sleep(1)
            result = self.check_hasil()
            while result == False:
                self.driver.ele("text:Cek").click()
                result = self.check_hasil()
                sleep(randint(1,5))
                
        except PenuhError:
            print("Sudah penuh")
            self.driver.close()
        except Exception as e:
            print("Sudah penuh")
            self.driver.close()
            
        sleep(10)
        self.driver.get_screenshot(name=f"Result-{self.name}")
        sleep(10)
        self.driver.close()
    
    def check_hasil(self):
        data = self.driver.html
        if "Sedang Diproses" in data:
            return False
        else:
            return True
    def check_result(self):
        result = self.driver.html
        if "coba lagi" in result:
            return False
        if "saat ini" in result:
            return False
        if "sudah penuh" in result:
            raise PenuhError("Sudah penuh")
        else:
            return True
            
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
        
        