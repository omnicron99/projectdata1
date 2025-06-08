import gspread
import requests
import csv
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials

# Configs
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

token = "EAAYHCb4Hp6sBOx744Q1J3PPzu9Qgwo40hZBZBp5GkS6LJa6DKIS4N8A7XRAsRH46m72tybE9qVneh7Q8bqpd93JCZCUmc05cbupicXCScV1rvpNsCCea7y8Y2Q1kCPlxZCO5ZCixJgWIXfWIudYaBXpJQjrRC6EkMnDd9yVg1UNM1qybX53BQJRwKHM7yMjmX9AZDZD"
fields = [
    "campaign_name",
    "reach",
    "impressions",
    "clicks",
    "spend",
    "onsite_conversion.messaging_conversation_started_7d",
    "cpm",
    "cpc"
]

# Data de ontem
ontem = datetime.now() - timedelta(days=1)
data_formatada = ontem.strftime("%d-%m-%Y")
data_api = ontem.strftime("%Y-%m-%d")

# Lê planilhas criadas
with open("planilhas_criadas.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        ad_account_id = row["ID_ADS_ACCOUNT"].strip()
        sheet_url = row["Planilha URL"].strip()

        try:
            planilha = client.open_by_url(sheet_url)
            aba = planilha.sheet1

            # Pega dados de campanha
            url = (
                f"https://graph.facebook.com/v19.0/act_{ad_account_id}/insights"
                f"?fields={','.join(fields)}"
                f"&time_range={{\"since\":\"{data_api}\",\"until\":\"{data_api}\"}}"
                f"&access_token={token}"
            )

            response = requests.get(url)
            data = response.json()

            campanhas = data.get("data", [])
            if not campanhas:
                aba.append_row([data_formatada, "Sem dados", 0, 0, 0, 0, 0, 0, 0])
                print(f"⚠️ Sem dados para conta {ad_account_id}, linha vazia registrada.")
                continue

            for campanha in campanhas:
                nome = campanha.get("campaign_name", "")
                alcance = int(campanha.get("reach", 0))
                impressoes = int(campanha.get("impressions", 0))
                cliques = int(campanha.get("clicks", 0))
                gasto = float(campanha.get("spend", 0))
                conversas = int(campanha.get("onsite_conversion.messaging_conversation_started_7d", 0))
                cpm = float(campanha.get("cpm", 0))
                cpc = float(campanha.get("cpc", 0))
                cpl = round(gasto / conversas, 2) if conversas > 0 else 0

                aba.append_row([
                    data_formatada,
                    nome,
                    alcance,
                    impressoes,
                    cliques,
                    gasto,
                    conversas,
                    cpm,
                    cpc,
                    cpl
                ])

            print(f"✅ Dados preenchidos para conta {ad_account_id}")

        except Exception as e:
            print(f"Erro com {ad_account_id}: {e}")
