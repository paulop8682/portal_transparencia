from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import sys
import db_sql
import sqlite3
from selenium.common.exceptions import TimeoutException

# Configurações do Chrome no modo headless
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080") 

# Inicializa o WebDriver com ChromeDriverManager e opções headless
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=chrome_options
)

driver.maximize_window()
driver.get('https://itambacuri-mg.portaltp.com.br/consultas/pessoal/planocarreiras.aspx')


def eh_divisao_inteira(num1, num2):
    if num2 == 0:
        return False  # Evitar divisão por zero
    return num1 % num2 == 0


def clicar_elemento_generico(driver, data_args=None, role=None, timeout=10):
    try:
        # Cria a expressão XPath com base nos atributos fornecidos
        xpath = "//a"
        if data_args:
            xpath += f"[@data-args='{data_args}']"
        if role:
            xpath += f"[@role='{role}']"
        
        # Espera até que o elemento esteja clicável e clica nele
        elemento = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        elemento.click()
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


#abre as informacoes
start_count = 0
end_count = 10
check_count = 0
conn = sqlite3.connect('portal.db')
cursor = conn.cursor()


while True:
    for count_botton in range(start_count,end_count):
        check_count += 1
        #Clica no botao
        wait = WebDriverWait(driver, 10)
        botton = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="ctl00_containerCorpo_grdData_DXDataRow{count_botton}"]/td[1]/button')))
        actions = ActionChains(driver)
        actions.move_to_element(botton).perform() 
        driver.execute_script("arguments[0].click();", botton)

        #Espera a informacoes ficarem visiveis
        wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="ctl00_containerCorpo_grdData_dxdt{count_botton}_ctl00_DXDataRow{0}"]/td[3]')))

        #quantidade de paginas por servico
        driver.save_screenshot('img_head.png')
        
        qntd_pag_servico = int(driver.find_element(By.CSS_SELECTOR, ".dxbs-pager").text.split(' ')[3])
        if qntd_pag_servico != 24:

            start_qntd_servidores = 0
            qntd_servidores = len(driver.find_element(By.XPATH, f'//*[@id="ctl00_containerCorpo_grdData_dxdt{count_botton}_ctl00_DXMainTable"]').text.split('\n')) - 7

            for pag in range(qntd_pag_servico):
        
                #Printa informacoes
                try:
                    for servidores in range(start_qntd_servidores,qntd_servidores):

                        nome_pessoa = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="ctl00_containerCorpo_grdData_dxdt{count_botton}_ctl00_DXDataRow{servidores}"]/td[3]')))

                        dados = (nome_pessoa.text,
                            driver.find_element(By.XPATH, f'//*[@id="ctl00_containerCorpo_grdData_DXDataRow{count_botton}"]/td[2]').text,
                            driver.find_element(By.XPATH, f'//*[@id="ctl00_containerCorpo_grdData_DXDataRow{count_botton}"]/td[5]').text,
                            driver.find_element(By.XPATH, f'//*[@id="ctl00_containerCorpo_grdData_dxdt{count_botton}_ctl00_DXDataRow{servidores}"]/td[5]').text,
                            driver.find_element(By.XPATH, f'//*[@id="ctl00_containerCorpo_grdData_dxdt{count_botton}_ctl00_DXDataRow{servidores}"]/td[6]').text,
                            driver.find_element(By.XPATH, f'//*[@id="ctl00_containerCorpo_grdData_dxdt{count_botton}_ctl00_DXDataRow{servidores}"]/td[7]').text)
                        
                        cursor.execute('''
                                        INSERT INTO DT_PORTAL_BRONZE (NOME, CARGO, SALARIO, TIPO_VINCULO, DATA_CONTRATACAO, DATA_DEMISSAO)
                                        VALUES (?, ?, ?, ?, ?, ?)
                                        ''', dados)
                        conn.commit()
                        
                    qntd_servidores += 10
                    start_qntd_servidores += 10
                    
                    clicar_elemento_generico(driver, data_args="PBN", role="button")
                    
                except Exception as e:
                    
                    erro_str = str(e)
    
                    if "Message:" in erro_str and "Stacktrace:" in erro_str:
                        pass
                    else:
                        print(f'Erro na iteracao de servidores por servico {erro_str}')
                        print(f'count block: {count_botton} \n quantidade servidores: {servidores}')
                        sys.exit(1)
                    
        else:
            #conta a quantidade de servidores no cargo
            qntd_servidores = len(driver.find_element(By.XPATH, f'//*[@id="ctl00_containerCorpo_grdData_dxdt{count_botton}_ctl00_DXMainTable"]').text.split('\n')) - 7

            #Printa informacoes
            for servidores in range(qntd_servidores):

                nome_pessoa = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="ctl00_containerCorpo_grdData_dxdt{count_botton}_ctl00_DXDataRow{servidores}"]/td[3]')))

                dados = (nome_pessoa.text,
                   driver.find_element(By.XPATH, f'//*[@id="ctl00_containerCorpo_grdData_DXDataRow{count_botton}"]/td[2]').text,
                   driver.find_element(By.XPATH, f'//*[@id="ctl00_containerCorpo_grdData_DXDataRow{count_botton}"]/td[5]').text,
                   driver.find_element(By.XPATH, f'//*[@id="ctl00_containerCorpo_grdData_dxdt{count_botton}_ctl00_DXDataRow0"]/td[5]').text,
                   driver.find_element(By.XPATH, f'//*[@id="ctl00_containerCorpo_grdData_dxdt{count_botton}_ctl00_DXDataRow0"]/td[6]').text,
                   driver.find_element(By.XPATH, f'//*[@id="ctl00_containerCorpo_grdData_dxdt{count_botton}_ctl00_DXDataRow0"]/td[7]').text)

                cursor.execute('''
                                INSERT INTO DT_PORTAL_BRONZE (NOME, CARGO, SALARIO, TIPO_VINCULO, DATA_CONTRATACAO, DATA_DEMISSAO)
                                VALUES (?, ?, ?, ?, ?, ?)
                                ''', dados)
                conn.commit()
        

        #mude de pagina
        try:
            if eh_divisao_inteira(check_count,10) is True:
                start_count += 10
                end_count += 10
                clicar_elemento_generico(driver, data_args="PBN", role="button")
        except:
            if conn:
                conn.close()
            sys.exit(0)

