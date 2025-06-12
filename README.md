# projectdata1

## 📜 Procedimentos úteis

### 🧪 Como ativar o venv (ambiente virtual)
```bash
python -m venv venv
.
.\venv\Scripts\Activate   # Windows PowerShell
# ou
venv\Scripts\activate.bat  # Windows CMD
```

Se der erro de permissão (ExecutionPolicy), rode o PowerShell como **Administrador** e execute:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### 📦 Como clonar o repositório em um novo ambiente
```bash
cd pasta/desejada
https://github.com/omnicron99/projectdata1.git
cd projectdata1
python -m venv venv
.
env\Scripts\Activate
pip install -r requirements.txt
```

> 🔐 Lembre-se de adicionar o `credentials.json` manualmente (não vem do GitHub).

---

### 💾 Como fazer commit e push para o GitHub
```bash
git add .
git commit -m "mensagem do commit"
git push origin main
```

> Certifique-se de estar na branch correta (`main` ou outra).

---

### ❌ Como remover arquivos sensíveis do repositório
```bash
git rm --cached credentials.json
echo "credentials.json" >> .gitignore
git add .gitignore
git commit -m "remover credentials do repo"
git push origin main
```

## ⚙️ Ambiente necessário

Crie dois arquivos locais antes de executar:

- `credentials.json`: credenciais do Google Sheets
- `meta_token.txt`: token de acesso à API Meta

Esses arquivos não estão no repositório por segurança.

### Como converter arquivos para base64 no powershell

Abra o terminal no pc e digite:

[Convert]::ToBase64String([IO.File]::ReadAllBytes("credentials.json")) > base64.txt

