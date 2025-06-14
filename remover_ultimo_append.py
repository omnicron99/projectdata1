import gspread
import csv
from google.oauth2.service_account import Credentials
from collections import defaultdict

# Autenticação com Google
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

with open("planilhas_criadas.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        nome_conta = row["Cliente"].strip()
        url = row["Planilha URL"].strip()

        try:
            planilha = client.open_by_url(url)
            aba = planilha.sheet1
            linhas = aba.get_all_values()

            if len(linhas) <= 1:
                print(f"⚠️ Planilha {nome_conta} só tem cabeçalho.")
                continue

            # Agrupa linhas por data
            dados_por_data = defaultdict(list)
            for i, linha in enumerate(linhas[1:], start=2):  # começa do índice 2 (linha 2 em diante)
                data = linha[0]
                dados_por_data[data].append(i)

            # Encontra a última data registrada
            ultima_data = sorted(dados_por_data.keys(), reverse=True)[0]
            linhas_para_remover = sorted(dados_por_data[ultima_data], reverse=True)

            for linha_index in linhas_para_remover:
                aba.delete_rows(linha_index)

            print(f"✅ Removidas {len(linhas_para_remover)} linhas da data {ultima_data} — conta {nome_conta}")

        except Exception as e:
            print(f"❌ Erro com {nome_conta}: {e}")
