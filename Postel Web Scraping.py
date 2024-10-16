from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
from selenium.webdriver.chrome.service import Service


chrome_driver_path = 'C:/Users/javie/Documents/Software/chromedriver-win64/chromedriver-win64/chromedriver.exe'
service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service)
driver.maximize_window()

url = "https://sertifikasi.postel.go.id/sertifikat/sertifikat-terbit" 
driver.get(url)

wait = WebDriverWait(driver, 10)


columns = ['Certificate Number', 'Issued Date', 'PLG ID', 'Name Of Applicant', 'Device Name', 'Merk', 'Model', 'Marketing Name', 'Country']

header_saved = False

try:
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  

    while True:
    
        wait.until(EC.presence_of_element_located((By.XPATH, "//table")))
        rows = driver.find_elements(By.XPATH, "//table[@id='vgt-table']/tbody/tr")

        for row in rows:
            columns_data = row.find_elements(By.TAG_NAME, "td")
            data = [col.text for col in columns_data]
            print(data)

            df = pd.DataFrame([data], columns=columns)
            df.to_csv('C:/Users/javie/Documents/Kuliah/Semester 7/Big Data/scraped_data3.csv', mode='a', header=not header_saved, index=False)
            header_saved = True  

        try:
            next_button = driver.find_element(By.XPATH, "//button[contains(@class, 'footer__navigation__page-btn')]//span[text()='Next']")
            next_button.click()
            time.sleep(2)  
        except:
            print("Halaman terakhir sudah dicapai.")
            break

except TimeoutException:
    print("Terjadi kesalahan: elemen tidak ditemukan dalam waktu yang ditentukan.")

print("Data scraping selesai.")

driver.quit()
