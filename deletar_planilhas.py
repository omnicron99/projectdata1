import gspread
from google.oauth2.service_account import Credentials
import csv

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

with open("planilhas_criadas.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        url = row["Planilha URL"].strip()
        try:
            sheet = client.open_by_url(url)
            file_id = sheet.id
            client.del_spreadsheet(file_id)
            print(f"✅ Planilha deletada com sucesso: {url}")
        except Exception as e:
            print(f"❌ Erro ao deletar {url}: {e}")