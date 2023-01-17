# Bot de lembretes no telegram


## DESCRIÇÃO

Este projeto é um bot simples para Telegram que permite aos usuários criar e receber lembretes. Ele utiliza a API do Telegram para interagir com o usuário, o banco de dados MySQL para armazenar os lembretes e threads para garantir a execução simultânea do módulo de conversa com o usuário e o módulo de envio de lembretes. As funcionalidades implementadas incluem:
  
    -Criação de lembretes que serão enviados na data escolhida.
  
    -Listagem de todos os lembretes, tanto enviados quanto não enviados.
  
    -Deleção de lembretes pelo ID do mesmo.
    
    -Deleção de todos os lembretes que já foram enviados.
    
    -Deleção de todos os lembretes.

## FUNCIONALIDADES

- Criação de lembretes que serão enviados na data escolhida
  - **É necessário inicializar o bot com "/start" > "/novoLembrete" > "Insira oque quer ser lembrado" > Coloque a data no formato DD-MM-AA(DIA-MÊS-ANO) > coloque a Hora no formato HH:MM(HORA:MINUTOS)(A DATA/HORA ESCOLHIDA PRECISA SER MAIOR QUE A DATA/HORA ATUAL) > Após isso é necessário digitar 'SIM'**.
 
 ## Exemplo de fluxo de criação de lembrete:
 
 ![image](https://user-images.githubusercontent.com/61162949/212970080-8a8e80ce-4dbd-4c9e-80a7-5ba4427bffeb.png)

 ## Exemplo do envio do lembrete:
 
 Quando o horário atual for igual ao horário salvo para envio do lembrete, o mesmo será enviado.
 
![image](https://user-images.githubusercontent.com/61162949/212970733-0fedd7a7-48c6-469f-9d8e-f40297fd33f4.png)

- Listagem de todos os lembretes, tanto enviados quanto não enviados.
  - **É necessário inicializar o bot com "/start" > "/verLembretes"**

 ## Exemplo de listagem dos lembretes:
 
![image](https://user-images.githubusercontent.com/61162949/212972242-46fdbdb4-66a7-424a-b3f9-21fb2fb043d9.png)

- Deleção de lembretes pelo ID do mesmo.
  - **É necessário inicializar o bot com "/start" > "/del + ID DO LEMBRETE"**

 ## Exemplo de deleção dos lembretes pelo ID do mesmo:
 
![image](https://user-images.githubusercontent.com/61162949/212973227-2e8742ec-aa31-4a1a-9fff-4321465a3f53.png)


- Deleção de todos os lembretes.
  - **É necessário inicializar o bot com "/start" > "/del all"**

## Exemplo de deleção de todos os lembretes:
![image](https://user-images.githubusercontent.com/61162949/212975404-a59a21ba-1364-44b4-b686-506f4aa5f603.png)

- Deleção de todos os lembretes que já foram enviados
  - **É necessário inicializar o bot com "/start" > "/del enviados"**


## Exemplo de deleção de todos os lembretes que já foram enviados:
![image](https://user-images.githubusercontent.com/61162949/212976128-73569f5e-6447-41e9-9d32-d1471c6b007c.png)


## Instalação

- Passo 1: Certifique-se que o Python 3 está instalado. A versão do python utilizada neste projeto foi a 3.6.9.

- Passo 2: Clone este repositório.

- Passo 3: Vá até o diretório raís da mesma e instale as dependencias usando o comando "pip install -m req.txt".

- passo 4: Renomeie o arquivo "server-config_example.json",que se encontra na pasta "MODEL", para "server-config.json".

- passo 5: Crie uma chave de criptografia da seguinte forma.

    - Crie um arquivo "criptografia.py" em qualquer diretorio e certifique-se que o *Fernet* esteja instalado(pip install cryptography). 

    - Coloque o seguinte código no arquivo "criptografia.py"

```  
from cryptography.fernet import Fernet 
key = Fernet.generate_key() 
f = Fernet(key) 
token = f.encrypt(b"welcome to geeksforgeeks") 
print(token)  

```  
- passo 8: Copie o token gerado e coloque no arquivo "server-config.json" na chave "criptokey".

- passo 9: Você precisa criptografar todas as informações necessárias para colocar no arquivo "server-config.json", menos a "apikey". Isso pode ser feito utilizando o módulo "CONTROLLER/cripto.py".

```  
from cryptography.fernet import Fernet

class Cripto:
    def __init__(self,key) -> None:
        
        self.__KEY : str = key #chave secreta utilizada atualmente

        self.__fernet = Fernet(self.__KEY) #Instancia a classe de criptografia com a chave

    def encriptar(self, object : bytes) -> bytes: #função de criptografar 
        
        return self.__fernet.encrypt(object)

    def decriptar(self, object : bytes) -> bytes: #função de decriptografar
        return self.__fernet.decrypt(object)

#No exemplo, o nome do banco(database) será criptografado
print(Cripto('SUA CHAVE DE CRIPTOGRAFIA AQUI').encriptar(b'bd_bot_telegram'))

```  
- passo 10 : Crie a seguinte tabela no MySQL

```  
CREATE TABLE `tb_mensagem_salva` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idUsuario` int(11) NOT NULL,
  `idChat` int(11) NOT NULL,
  `Mensagem` longtext,
  `data_lembrete` varchar(50) DEFAULT NULL,
  `enviado` bit(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;

```  
- passo 11 : Execute a aplicação.
