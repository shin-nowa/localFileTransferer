#  🇧🇷 🇺🇸 Local File Transferer #

<div align="center">
  <img src=".\localFileTransferer\assets\print.png" alt="Demonstração do Local File Transferer" width="700">
</div>

## Servidor Local para transferência de arquivos entre dispositivos ##
### Criado utilizando Python (Django) ###

## Local Server for transfering files between devices. ##
### Created utilizing Python (Django) ###


# 🇧🇷 Utilização #
1. Clone o repositório.
2. Crie e ative um ambiente virtual (venv).
3. Instale as dependências (` pip install -r requirements.txt `)
4. Navege para a pasta localFileTransferer  
``` bash
    cd localFileTransferer
```
5. Execute as migrações para criar um banco de dados local:
 ``` bash
    python manage.py migrate
```
6. Crie seu usuário com:
``` bash
  python manage.py createsuperuser
```
7. **Edite o arquivo  `.env.example`:**
Renomeie o arquivo `.env.example` para `.env` em `/localFileTransferer/.env`, abra com um editor e substitua o texto `YOUR_IP` pelo seu endereço de IPv4 local.

    > ⚠️ **Importante:** Não apague `127.0.0.1` ou `localhost`. Apenas adicione seu IP à lista, separado por vírgulas.

    **Exemplo:**
    ```ini
    # Antes:
    ALLOWED_HOSTS_CSV=,127.0.0.1,localhost, YOUR_IP

    # Depois:
    ALLOWED_HOSTS_CSV=127.0.0.1,localhost, 10.0.0.1
    ```
7. Execute o servidor (` python manage.py runserver 0.0.0.0:8000 `)

# 🇺🇸 Usage #
1. Clone the repository.
2. Create and activave a virtual enviroment (venv).
3. Install dependencies. (` pip install -r requirements.txt `)
4. Navigate to the folder localFileTransferer  
``` bash
    cd localFileTransferer
```
5. Execute migrations to create a local database:
 ``` bash
    python manage.py migrate
```
6. Create your user with:
``` bash
  python manage.py createsuperuser
```
7. **Editing the file `.env.example`:**
Rename the file named `.env.example` to `.env` located on `/localFileTransferer/.env`, open with a text editor and replace the text `YOUR_IP` by your local IPv4 IP.

    > ⚠️ **Important:** DO NOT DELETE `127.0.0.1` or `localhost`. Only add your ip to the list with commas.

    **Example:**
    ```ini
    # Before:
    ALLOWED_HOSTS_CSV=,127.0.0.1,localhost, YOUR_IP

    # After:
    ALLOWED_HOSTS_CSV=127.0.0.1,localhost, 10.0.0.1
    ```
7. Execute the server (` python manage.py runserver 0.0.0.0:8000 `)
