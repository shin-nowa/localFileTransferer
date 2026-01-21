@echo off
TITLE Local File Transferer Launcher
CLS

echo ====================================================================
echo                Iniciando Local File Transferer
echo ====================================================================

python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Python nao enconcontrado. Instale o Python e marque a caixa "Add to PATH"
    pause
    exit
)

IF NOT EXIST ".venv" (
    echo [INFO] Criando ambiente virtual (.venv)
    python -m venv .venv
    echo [OK] Ambiente Criado.
) ELSE (
    echo [INFO] Ambiente Virtual Encontrado
)

call .\.venv\Scripts\activate

echo [INFO] Verificando dependencias
pip install -r requirements.txt
echo [OK] Dependencias instaladas.

echo.
echo [START] Servidor iniciando. Pressione CTRL + C para parar.
echo.
cd localFileTransferer
echo [INFO] Criando migracoes no banco de dados local.
python manage.py migrate
echo [OK] Migracoes feitas

echo [INFO] Crie seu usuario administrador
python manage.py createsuperuser

echo [INFO] Servidor iniciando.
python manage.py runserver 0.0.0.0:8000

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [PARADO] O servidor foi encerrado.
    pause
)