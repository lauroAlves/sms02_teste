
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import threading

app = Flask(__name__)

# Variável global para armazenar os dados
global_data = {}

# Configuração global do WebDriver
options = Options()
options.add_argument('--headless')  # Rodar em modo headless para não abrir uma janela do navegador
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Remote(command_executor='http://chrome:4444/wd/hub', options=options)

def collect_data():
    global global_data
    url = "https://sms02.esig.com.br/"
    while True:
        try:
            # Acessa a URL
            driver.get(url)
            time.sleep(2)  # Aguarda 2 segundos para garantir que a página carregue completamente

            # Coleta os dados do painel
            carga_bateria = int(driver.find_elements(By.CLASS_NAME, 'DigitalValor')[2].text.replace('%', ''))
            temperatura = int(driver.find_elements(By.CLASS_NAME, 'DigitalValor')[5].text.replace('ºC', ''))
            tensao_entrada = int(driver.find_elements(By.CLASS_NAME, 'DigitalValor')[0].text.replace('VAC', ''))
            tensao_saida = int(driver.find_elements(By.CLASS_NAME, 'DigitalValor')[3].text.replace('VAC', ''))

            # Inicializa os alertas
            alerta_carga_bateria = None
            alerta_temperatura = None
            alerta_tensao_entrada = None
            alerta_tensao_saida = None

            # Verifica a temperatura
            if temperatura > 35:
                alerta_temperatura = "Temperatura acima de 35°C!"

            # Verifica a carga da bateria
            if carga_bateria < 90:
                alerta_carga_bateria = "Bateria abaixo de 90%!"
            
            if tensao_entrada > 227:
                alerta_tensao_entrada = "Tensão de entrada está acima do indicado"
            elif tensao_entrada < 217:
                alerta_tensao_entrada = "Tensão de entrada está abaixo do indicado"

            if tensao_saida > 229:
                alerta_tensao_saida = "Tensão de saída está acima do indicado"
            elif tensao_saida < 219:
                alerta_tensao_saida = "Tensão de saída está abaixo do indicado"
            
            # Cria um dicionário com os dados coletados e os alertas
            global_data = {
                "carga_bateria": carga_bateria,
                "temperatura": temperatura,
                "tensao_entrada": tensao_entrada,
                "tensao_saida": tensao_saida,
                "alerta_carga_bateria": alerta_carga_bateria,
                "alerta_temperatura": alerta_temperatura,
                "alerta_tensao_entrada": alerta_tensao_entrada,
                "alerta_tensao_saida": alerta_tensao_saida 
            }

        except Exception as e:
            print(f"Erro ao coletar dados: {e}")

        # Aguarda 10 segundos antes de repetir
        time.sleep(10)

# Cria e inicia o thread para coleta de dados
data_collection_thread = threading.Thread(target=collect_data, daemon=True)
data_collection_thread.start()

@app.route('/data')
def get_data():
    return jsonify(global_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Configura o Flask para aceitar conexões externas na porta 8080

# Encerre o WebDriver quando o servidor for interrompido
import atexit
atexit.register(lambda: driver.quit())
