from PySide6.QtCore import QThread, Signal
from selenium       import webdriver
from selenium.webdriver.chrome.service  import Service
from selenium.webdriver.chrome.options  import Options
from selenium.webdriver.common.by       import By
from webdriver_manager.chrome           import ChromeDriverManager

import time

class ScraperWorker(QThread):
    # Signals
    data_received = Signal(list)
    status_update = Signal(str)

    def run(self):
        self.status_update.emit("Stay Calm... Launching Browser")

        # Setup Chrome Options
        chrome_options = Options()
        """
        Headless Mode is OFF so that the user can see the login page for myUnisa
        chrome_options.add_argument("--headless")
        """

        # INIT Driver
        service = Service(ChromeDriverManager().install())
        driver  = webdriver.Chrome(service=service, options=chrome_options)

        try:
                # Navigate to myModules
                #URL to myModules:
                self.status_update.emit("Attempting to connect to myModules...")
                driver.get("https://mymodules.dtls.unisa.ac.za/login/index.php")

                # AFTER LOGIN - We wait until the 'Dashboard' or 'My Courses' appears after login.
                # We'll use a loop to check if we are logged in every second.
                logged_in  = False
                timeout    = 300
                start_time = time.time()

                while not logged_in and (time.time() - start_time) < timeout:
                        if "dashboard" in driver.current_url.lower() or "my" in driver.current_url.lower():
                                logged_in = True
                        time.sleep(1)

                if not logged_in:
                        self.status_update.emit("Login timed out. Try again later.")
                        driver.quit()
                        return

                self.status_update.emit("Login Successful!")

                # Scrape the assignments
                results = []
                events = driver.find_elements(By.CLASS_NAME, "event-name")

                for event in events:
                     # We try to find a date sibling or child; for now, we just grab the name
                     results.append([event.text, "Date Peniding"])

                if not results:
                        results = [["No assignments found", "N/A"]]
                self.data_received.emit(results)
                self.status_update.emit("Scrape complete. See, no need to panic!")

        except Exception as e:
                self.status_update.emit(f"Error: {str(e)}")



