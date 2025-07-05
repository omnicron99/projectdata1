import gspread
import requests
import csv
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials
import logging
import traceback

# Configurar logs
logging.basicConfig(
    filename="logs_execucao.txt",
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

# Configs
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

with open("meta_token.txt", "r") as token_file:
    token = token_file.read().strip()

# Data de ontem
ontem = datetime.now() - timedelta(days=1)
data_formatada = ontem.strftime("%d-%m-%Y")
data_api = ontem.strftime("%Y-%m-%d")

# Lê planilhas criadas
with open("planilhas_criadas.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        nome_conta = row["Cliente"].strip()
        ad_account_id = row["ID_ADS_ACCOUNT"].strip()
        if not ad_account_id.startswith("act_"):
            ad_account_id = f"act_{ad_account_id}"

        sheet_url = row["Planilha URL"].strip()

        try:
            planilha = client.open_by_url(sheet_url)
            aba = planilha.sheet1

            # Pega dados de campanha (nível de campanha)
            url = (
                f"https://graph.facebook.com/v19.0/{ad_account_id}/insights"
                f"?fields=campaign_name,reach,impressions,clicks,spend,actions,cpm,cpc"
                f"&level=campaign"
                f"&time_range={{\"since\":\"{data_api}\",\"until\":\"{data_api}\"}}"
                f"&access_token={token}"
            )

            response = requests.get(url)
            data = response.json()

            campanhas = data.get("data", [])
            if not campanhas:
                aba.append_row([data_formatada, "Sem dados", 0, 0, 0, 0, 0, 0, 0, 0])
                msg = f"⚠️ Sem dados para conta {nome_conta}, linha vazia registrada."
                print(msg)
                logging.warning(msg)
                continue

            for campanha in campanhas:
                nome = campanha.get("campaign_name", "")
                alcance = int(campanha.get("reach", 0))
                impressoes = int(campanha.get("impressions", 0))
                cliques = int(campanha.get("clicks", 0))
                gasto = float(campanha.get("spend", 0))
                cpm = float(campanha.get("cpm", 0))
                cpc = float(campanha.get("cpc", 0))

                # Buscar conversas iniciadas
                conversas = 0
                for action in campanha.get("actions", []):
                    if action.get("action_type") == "onsite_conversion.messaging_conversation_started_7d":
                        conversas = int(float(action.get("value", 0)))
                        break

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

            msg = f"✅ Dados preenchidos para conta {nome_conta}"
            print(msg)
            logging.info(msg)

        except Exception as e:
            msg = f"❌ Erro com conta {nome_conta}: {e}"
            print(msg)
            logging.error(msg)
            traceback.print_exc()
