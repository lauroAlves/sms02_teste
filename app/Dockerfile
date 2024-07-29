# Use uma imagem oficial do Python como imagem base
FROM python:3.9-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos necessários para o diretório de trabalho no contêiner
COPY requirements.txt requirements.txt
COPY sms-webscraping.py sms-webscraping.py

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 8080 para o Flask
EXPOSE 8080

# Define o comando para rodar o aplicativo
CMD ["python", "sms-webscraping.py"]
