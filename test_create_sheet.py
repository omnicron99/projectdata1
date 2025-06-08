import gspread
from google.oauth2.service_account import Credentials

# Autenticação
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

# Nome da planilha
sheet_name = "conta_123456789"

# Criação da planilha
spreadsheet = client.create(sheet_name)

# Pega a URL da planilha criada
print(f"Planilha criada: {spreadsheet.url}")
