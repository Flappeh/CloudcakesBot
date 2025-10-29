from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.errors import PageDisconnectedError
from DrissionPage.common import wait_until
from modules import proxy as px
from time import sleep
from modules.config import LOGIN_URL, ENABLE_PROXY
from random import randint
from datetime import datetime, timedelta

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
            self.check_time()
            self.driver.refresh()
            sleep(0.5)
            self.check_result()
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
        except PenuhError:
            print("Sudah penuh")
            self.driver.close()
        except Exception as e:
            print("Continuing")
            
        try:
            tries = 0
            result = False
            while tries < 10 and result == False:
                self.driver.refresh()
                self.insert_creds()
                result = self.check_result()
                tries += 1
                
            if tries == 3 and result == False:
                self.result = "Proxy Timeout Error"
                self.driver.close()
            
            sleep(1)
            result = self.check_hasil()
            start_time = datetime.now()
            while result == False:
                self.driver.ele("text:Cek").click()
                result = self.check_hasil()
                elapsed = datetime.now() - start_time
                if elapsed >= timedelta(seconds=60):
                    result = True
                sleep(randint(1,5))
            
        except PenuhError:
            print("Sudah penuh")
            self.driver.close()
        except Exception as e:
            print("Sudah penuh")
            self.driver.close()
        
        if "Dapatkan" in self.driver.html:
            self.driver.close()
            return
        
        sleep(100)
        self.driver.get_screenshot(name=f"Result-{self.name}")
        sleep(10)
        self.driver.close()
    
    def check_time(self):
        try:
            now = datetime.now()
            target = datetime(now.year, now.month, now.day, 9, 59, 59)
            if now > target:
                return
            delta = target - now
            if delta > timedelta(0):
                sleep(delta.total_seconds())
            return
        except Exception:
            print("Error occured")
            
    def check_hasil(self):
        data = self.driver.html
        if "Jangan tutup" in data:
            return False
        else:
            return True
    def check_result(self):
        result = self.driver.html
        if "besuk" in result:
            return False
        if "coba lagi" in result:
            return False
        if "saat ini" in result:
            return False
        if "sudah penuh" in result:
            raise PenuhError("Sudah penuh")
        else:
            return True
            
    def insert_creds(self):
        try:
            # Wait until element exists and is visible
            ele = self.driver.wait.ele_displayed('#name', timeout=5)
            ele.input(self.name)
        except Exception:
            print("Tried entering name")

        try:
            ele = self.driver.wait.ele_displayed('#email', timeout=5)
            ele.input(self.email)
        except Exception:
            print("Tried entering email")

        try:
            ele = self.driver.wait.ele_displayed('#phone', timeout=5)
            ele.input(self.phone)
        except Exception:
            print("Tried entering phone")

        try:
            btn = self.driver.wait.ele_displayed('text:Dapatkan', timeout=5)
            btn.click()
        except:
            print("Tried Clicking")
        
        