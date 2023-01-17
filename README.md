# Bot-telegram-Lembrete


## DESCRIÇÃO

Um bot simples para gravar e receber lembretes no telegram que implemente as seguintes funcionalidas:
  
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


