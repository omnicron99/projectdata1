import gspread
from google.oauth2.service_account import Credentials

# Escopos necessários para acessar e deletar planilhas
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]

# Autenticação
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

# Lista de links das planilhas a serem deletadas
spreadsheet_urls = [
    "https://docs.google.com/spreadsheets/d/1h-aVttqz5rQgw1e_ws_OmBHxoZ0s7pIQRbBQbQ62CXc",
    "https://docs.google.com/spreadsheets/d/1F3ZFF82A594-G6C5YTA-dn6UI3LeREzqqzzptJMpKPs",
    "https://docs.google.com/spreadsheets/d/1KT430S0K9TLKiei3PAY4_eBRBEUVtPlX1figv8ax-2U",
    "https://docs.google.com/spreadsheets/d/1sZmVgCcOqHHwwnNEqtoNodiz6eAPuIXlmVsChha1g04",
    "https://docs.google.com/spreadsheets/d/1w1vs2KSXofE-lD6UmHSKofgoipughrz4krhFxPE0FjI",
    "https://docs.google.com/spreadsheets/d/1IczxdKtGwp8StLTk1lOxych1wJrwalW_a-wZoTpYEp8",
    "https://docs.google.com/spreadsheets/d/10GZB_w7U-vA7uWKM6mVfcDiLBpgMELSxIugNyijP09s"
]

# Deletar uma a uma
for url in spreadsheet_urls:
    try:
        sheet = client.open_by_url(url)
        file_id = sheet.id
        client.del_spreadsheet(file_id)
        print(f"Planilha deletada com sucesso: {url}")
    except Exception as e:
        print(f"Erro ao deletar {url}: {e}")
