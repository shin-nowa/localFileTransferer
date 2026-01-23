#!/bin/bash

# Garante que roda na pasta do script
cd "$(dirname "$0")"

# --- CONFIGURAÇÃO DE CORES (TrueColor) ---
THEME_COLOR='\033[38;2;207;24;146m' # #cf1892 (Rosa)
TEXT_COLOR='\033[38;2;255;255;255m'  # #ffffff (Branco)
NC='\033[0m'

# Função para printar com estilo
print_msg() {
    echo -e "${THEME_COLOR}[$1] ${TEXT_COLOR}$2${NC}"
}

clear
echo -e "${THEME_COLOR}====================================================================${NC}"
echo -e "${THEME_COLOR}                Iniciando Local File Transferer                     ${NC}"
echo -e "${THEME_COLOR}====================================================================${NC}"

# 1. verificando o python
if ! command -v python3 &> /dev/null; then
    print_msg "ERRO" "Python3 nao encontrado. Instale via 'sudo pacman -S python'."
    read -p "Pressione Enter para sair..."
    exit 1
fi

# 2. criando/ verificando se a venv existe
if [ ! -d ".venv" ]; then
    print_msg "INFO" "Criando ambiente virtual (.venv)..."
    python3 -m venv .venv
    print_msg "OK" "Ambiente Criado."
else
    print_msg "INFO" "Ambiente Virtual Encontrado."
fi

# 3. ativando a venv
source .venv/bin/activate

# 4. instalando o requirements.txt
print_msg "INFO" "Verificando dependencias..."
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_msg "OK" "Dependencias instaladas."
else
    print_msg "ERRO" "Falha ao instalar dependencias."
fi

# 5. avisos
echo ""
echo -e "${THEME_COLOR}[START] ${TEXT_COLOR}Servidor iniciando. Aguarde.${NC}"
echo ""

cd localFileTransferer || { echo "Pasta não encontrada"; exit 1; }

if [ ! -d "static" ]; then
    mkdir static
fi

# 6. migracoes do banco de dados
print_msg "INFO" "Sincronizando banco de dados..."
python manage.py migrate > /dev/null 2>&1
print_msg "OK" "Migracoes do banco de dados feitas."

# 7. criando super user
if [ ! -f ".configurado" ]; then
    echo ""
    echo -e "${THEME_COLOR}[PRIMEIRA EXECUCAO]${NC} ${TEXT_COLOR}Crie seu usuario administrador:${NC}"
    python manage.py createsuperuser
    echo "Setup Feito" > .configurado
    echo ""
    print_msg "OK" "Usuario criado."
fi

# 8. print final
clear
echo -e "${THEME_COLOR}=======================================================${NC}"
echo -e "${TEXT_COLOR}                    SERVIDOR ONLINE                    ${NC}"
echo -e "${THEME_COLOR}=======================================================${NC}"
echo ""
echo -e "${THEME_COLOR}  [PC]           ${TEXT_COLOR}Acesse: http://127.0.0.1:8000${NC}"
echo ""

# script pra pegar o ip
PY_CMD="import socket; s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(('8.8.8.8', 80)); print('http://' + s.getsockname()[0] + ':8000'); s.close()"
IP_REDE=$(python3 -c "$PY_CMD" 2>/dev/null)

echo -e "${THEME_COLOR}  [REDE LOCAL]   ${TEXT_COLOR}Acesse: $IP_REDE${NC}"
echo ""
echo -e "${THEME_COLOR}=======================================================${NC}"
echo -e "${TEXT_COLOR}  (Para desligar, pressione CTRL + C)${NC}"

# rodando o server
python manage.py runserver 0.0.0.0:8000 --noreload > /dev/null 2>&1

echo ""
echo -e "${THEME_COLOR}[PARADO]${TEXT_COLOR} O servidor foi encerrado.${NC}"