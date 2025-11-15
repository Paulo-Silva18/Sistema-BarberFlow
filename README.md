INSTRUÇÕES PARA USO DO PROJETO TCD

Requisitos do ambiente
1. instalar a última versão do Python em https://www.python.org/ftp/python/3.14.0/python-3.14.0-amd64.exe

2. Instalar o MySQL em https://dev.mysql.com/downloads/workbench/

3. Ter um computador com suporte a navegador, de preferência Google Chrome

4. Ter o VSCODE instalado em https://code.visualstudio.com/download

Comandos para instalação
No MySQL Workbench: CREATE DATABASE barbearia_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

Abra o PowerShell e dentro dele faça as seguintes instruções:
1. Navegue até a pasta do Sistema de agendamento usando o comando cd (Ex: cd "C:\Users\Paulo Henrique\Documents\Sistema de agendamento"). 
2. Crie uma máquina virtual (venv) usando o comando python -m venv sistema_de_agendamento na pasta navegada.
3. Ative a venv usando o comando .\sistema_de_agendamento\Scripts\Activate.ps1
4. Após isso, navegue até a pasta barbearia_project dentro da pasta Sistema de agendamento usando o comando cd (Ex: cd "C:\Users\Paulo Henrique\Documents\Sistema de agendamento\barbearia_project")
5. Use o comando pip install -r requirements.txt e espere instalar todas as bibliotecas

Feche o PowerShell e abra o VSCODE na pasta Sistema de agendamento. Ao abrir, acesse o arquivo settings.py em Sistema de agendamento\barbearia_project\barbearia_project. Acessando o arquivo vá até na parte do código na print abaixo:
<img width="595" height="325" alt="image" src="https://github.com/user-attachments/assets/594627f8-02dc-4cbf-99e9-b0bbee4eb0a7" />

 

Altere o USER para o seu usuário do banco, o PASSWORD para a sua senha do banco, o 	HOST para o seu host do banco e a PORT para a sua porta do banco.

Abra o terminal do VSCODE e navegue até a pasta do Sistema de agendamento usando o comando cd (Ex: cd "C:\Users\Paulo Henrique\Documents\Sistema de agendamento"). Após estar na pasta, use o comando .\sistema_de_agendamento\Scripts\Activate.ps1. Após ativar a máquina virtual, acesse a pasta barbearia_project dentro da pasta Sistema de agendamento usando o comando cd (Ex: cd "C:\Users\Paulo Henrique\Documents\Sistema de agendamento\barbearia_project"). Após acessar a pasta. Rode o comando python manage.py migrate que irá criar as tabelas no MySQL e espere até que o processo seja concluído.

Após rodar o migrate, use o comando python manage.py createsuperuser e siga as instruções do python para criar o super usuário. Ele é necessário para ter um super usuário para navegar em uma parte do sistema. Após a criação, rode o comando python manage.py runserver e abra o navegador colocando a URL http://127.0.0.1:8000/admin/.  

O acessar o link, digite o usuário e senha usados na criação do super usuário e clique em acessar:
<img width="614" height="484" alt="image" src="https://github.com/user-attachments/assets/5da4e7d3-1bed-4b3c-911f-3782f732242d" />
 

Após isso é necessário cadastrar os serviços e os barbeiros, além de completar os dados do seu super usuário.

Na aba Administração do Site, vá até a linha Servicos e clique em adicionar:
<img width="709" height="48" alt="image" src="https://github.com/user-attachments/assets/6441a4b5-ce5c-451d-8fd4-c0f34d234772" />


Preencha os dados do serviço e clique no botão em salvar

Faça o mesmo processo para o Barbeiro:
<img width="381" height="56" alt="image" src="https://github.com/user-attachments/assets/944b753f-d2c5-45ed-a25a-ed23c8cb0639" />

 

Cadastro: Acesse a URL: http://127.0.0.1:8000/cadastro/
Crie uma nova conta de cliente. Você será logado automaticamente.
Login: Se já tiver conta, acesse http://127.0.0.1:8000/login/ e entre.
Agendar: Na página inicial (/), você (agora logado) verá o formulário.
Selecione o Barbeiro, o Serviço e a Data e Hora.
Clique em "Agendar".
O sistema validará as regras de negócio (não permite horários ocupados e nem aos domingos).
Listar/Editar/Excluir: Acesse http://127.0.0.1:8000/lista-agendamentos/ para ver seus agendamentos futuros.
Você pode editar (mudar o horário) ou excluir um agendamento.
