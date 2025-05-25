# backend/scraping.py
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def extrair_dados():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get("https://painelcemadenrj.defesacivil.rj.gov.br/monitoramento/v2/municipio/?action=geo")

    wait = WebDriverWait(driver, 15)
    valor_3 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dataTable"]/tbody/tr[17]/td[3]'))).text
    valor_4 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dataTable"]/tbody/tr[17]/td[4]'))).text

    dados = {
        "Risco atual": valor_3,
        "Última atualização": valor_4,
        "Hora da extração": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    
    print(f"Valores encontrados: {valor_3}, {valor_4}")

    with open(r"E:\vscode_projects\geosirene_project\geosirene\backend\geosirene\dados_chuva.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    driver.quit()
    
extrair_dados()