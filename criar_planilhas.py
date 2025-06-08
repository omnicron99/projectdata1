import gspread
from google.oauth2.service_account import Credentials
import csv
import os

# Autenticação
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

# Abrir planilha mestre
spreadsheet_master = client.open_by_url("https://docs.google.com/spreadsheets/d/1Db1tQChukELH81zqVBVjm3DDydKBttHVwRVRC-SntvI")
sheet = spreadsheet_master.worksheet("Planilha1")

# Ler colunas
clientes = sheet.col_values(1)[1:]         # Coluna A (Cliente), pula o cabeçalho
ids = sheet.col_values(5)[1:]              # Coluna E (ID_ADS_ACCOUNT), pula o cabeçalho

# Verificar se CSV já existe
arquivo_csv = "planilhas_criadas.csv"
planilhas_existentes = set()

if os.path.exists(arquivo_csv):
    with open(arquivo_csv, newline="", encoding="utf-8") as f:
        next(f)  # pula cabeçalho
        for row in csv.reader(f):
            planilhas_existentes.add(row[0].strip())  # Nome do cliente já salvo

# Abre CSV para adicionar novas planilhas
with open(arquivo_csv, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    if os.stat(arquivo_csv).st_size == 0:
        writer.writerow(["Cliente", "ID_ADS_ACCOUNT", "Planilha URL"])

    for cliente, ads_id in zip(clientes, ids):
        cliente_nome = cliente.strip()
        ads_id = ads_id.strip()

        if not cliente_nome or not ads_id:
            continue

        if cliente_nome in planilhas_existentes:
            print(f"⏭️ Pulando {cliente_nome} — já existe.")
            continue

        nome_planilha = f"conta_{cliente_nome.replace(' ', '_')}"
        nova_planilha = client.create(nome_planilha)

        # Compartilhar com domínio
        nova_planilha.share("conversaojuridica.com.br", perm_type="domain", role="writer")

        # Registrar no CSV
        writer.writerow([cliente_nome, ads_id, nova_planilha.url])
        print(f"✅ Criada planilha para {cliente_nome} — {nova_planilha.url}")
