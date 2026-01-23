@echo off
TITLE Local File Transferer Launcher
CLS

echo ====================================================================
echo                Iniciando Local File Transferer
echo ====================================================================

:: 1 procura o python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Python nao enconcontrado. Instale o Python e marque a caixa "Add to PATH"
    pause
    exit
)

::2 verifica se existe uma venv e cria ela caso nao tenha
IF NOT EXIST ".venv" (
    echo [INFO] Criando ambiente virtual (.venv)
    python -m venv .venv
    echo [OK] Ambiente Criado.
) ELSE (
    echo [INFO] Ambiente Virtual Encontrado
)

::3 ativa a venv
call .\.venv\Scripts\activate

::4 instala os requirements
echo [INFO] Verificando dependencias
pip install -r requirements.txt
echo [OK] Dependencias instaladas.

::5navega até a pasta localFileTransferer com o django em si.
echo.
echo [START] Servidor iniciando. Aguarde.
echo.
cd localFileTransferer
IF NOT EXIST "static" (
    mkdir static
)

::6 faz as migrações do banco de dados
echo [INFO] Verificando banco de dados.
python manage.py migrate

::7cria um arquivo .configurado para marcar se é a primeira vez ou não do usuario rodando o programa
IF NOT EXIST ".configurado" (
    echo.
    echo [PRIMEIRA EXECUCAO DETECTADA]
    echo Crie um usuario administrador para acessar o painel.
    echo.
    python manage.py createsuperuser
    echo Setup Feito > .configurado
    echo.
    echo [OK] Usuário criado e configuracao salva.
)
echo [OK] Migracoes feitas
:: 8 imprimindo na tela o ip que deve ser acessado
cls
echo =======================================================
echo                    SERVIDOR ONLINE
echo =======================================================
echo.
echo   [PC]        Acesse: http://127.0.0.1:8000
echo.
echo  [REDE LOCAL] Acesse: 
:: pegando o ip do socket pra mostrar no terminal
        python -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(('8.8.8.8', 80)); print('  http://' + s.getsockname()[0] + ':8000'); s.close()"
echo.
echo =======================================================
echo  (Para desligar, feche esta janela ou pressione CTRL + C)

python manage.py runserver 0.0.0.0:8000 --noreload >nul 2>&1

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [PARADO] O servidor foi encerrado.
    pause
)