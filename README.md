# Local File Transferer

<div align="center">
  <img src=".\localFileTransferer\assets\print1.png" alt="Demonstração do Local File Transferer" width="700">
    <p>
  <img src = ".\localFileTransferer\assets\terminal.png" alt = "Terminal rodando o serivdor" width = "400px">
</div>

---

## :: O problema e a Motivação
Transferir arquivos pesados ou diretórios inteiros entre dispositivos mesmo que na mesma rede frequentemnete exigem intermédiarios ineficientes (como upload em serviços de nuvem, seguido de download) ou o uso de HDs externos ou pendrives.

O **Local File Transferer** foi desenvolvido para resolver esse gargalo criando um servidor local seguro via Django que permite a transferência direta (p2p indireto na sub-rede) de arquivos via browser. O foco do projeto foi garantir alta velocidade de I/O, baixo consumo de memória e privacidade total dos arquivos transferidos.

## :: Arquitetura e Decisões Técnicas

Para garantir que a aplicação suprotasse arquivos grandes sem derrubar o servidor por falta de memória RAM, as seguintes decisões foram tomadas:

* **Otimização de Upload (Chunking vs RAM):** Ao invés de carregar o arquivo inteiro na memória (que causaria Out of Memory durante a transferência de arquivos pesados), o sistema utiliza leitura e escrita em blocos (`uploaded_file.chunks()`), gravando diretamente no disco do servidor conforme os pacotes chegam.
* **Otimização de Download (FileResponse):** Para o download de arquivos utilizou-se o `FileResponse` do Django, que realiza o streaming direto do *file system* para a rede, mantendo o uso da CPU e RAM próximos de zero durante o processo.
* **Zipagem de Diretórios em Memória (In-Memory ZIP):** Para o download de pastas inteiras, o sistema cria um `.zip` sob demanda na memória ram (`io.BytesIO()`).
  * *Trade-off:* Isso evita a criação de arquivos temporários ("lixo") no disco do servidor e acelera o tempo de resposta inicial, embora exija atenção ao limite de RAM para diretórios massivos.
* **Automação de Rede e Usabilidade (UX):** Para evitar que o usuário final precise manipular comandos de terminal para descobrir qual seu IPv4 para que o servidor possa ser acessado em outra máquina, implementei scripts de inicialização (start.bat e start.sh). Eles automatizam a descoberta de rede, inicializando o servidor exposto para a rede local e entregam o IP final formatado na tela. Isso reduz o atrito e torna a experiência muito mais rápida.

## :: Funcionalidades Principais
- [x] **Navegação de Diretórios:** Interface web para navegar pelo diretório definido do host.
- [x] **Perfis:** Cada usuário possui um diretório base ativo (`active_directory`) isolado.
          *Estatísticas:* Cálculo de volumetria total trafegada (Upload/Download convertidos dinamicamente para KB, MB e GB) salvo no perfil do usuário.
- [x] **Auditoria e Logs:** Rastreamento completo de ações registrando IP de origem, tamanho da transferência e tipo de operação via modelo `TransferLog`.
- [x] **Suporte a Diretórios:** Compactação automática de pastas inteiras em formato `.zip` para download com um clique.

---

## >_ Como Executar

O projeto conta com scripts automatizados para facilitar o acesso ao ambiente.

### Windows
1. Clone este repositório.
2. Na raiz do projeto, execute o script de inicialização:
`cmd`
`start.bat`

### Linux
1. Clone este repositório.
2. Na raiz do projeto, dê permissão e execute o script:
`chmod +x start.sh`
`./start.sh`