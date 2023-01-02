import telebot as telebot #utilizado para usar a api do telegram
import datetime as datetime #utilizado para trabalhar com datas
import MODEL.sqlConnection as sqlcon #utilizado para conectar com o banco
import MODEL.sqlCommands as sqlcomands #utilizado para pegar os comandos do banco
import CONTROLLER.server_config as  ServerConfig #utilizado pegar as configurações
from threading import Thread #utilizado para rodar programas em paralelo
import schedule as schedule #utilizado como task scheduler pra verificar se tem novos lembretes para enviar
import time as time #utilizado para dar um timeout entre algumas requisições para o telegram e para verificação do scheduler

class ApiTelegramListener:

    def __init__(self) -> None:
    
        self.__config = ServerConfig.ServerConfig() #faz a leitura das configs
    
        self.bot = telebot.TeleBot(f"{self.__config.apikey}") #Inicia a API do telegram
    
        bot = self.bot #associa o bot a uma variável
        
    
        @bot.message_handler(commands=['start']) #Comando /start
        def start(message):
            #mensagem inicial
            bot.reply_to(message, f"Opa {message.from_user.first_name}, ta tudo beleza ? Ainda estou em desenvolvimento. Versão atual 1.0 - ultima atualização - 30-12-2022 04:27\n/novoLembrete - Salva novo lembrete \n/verLembretes - Ver lembretes salvos")

        @bot.message_handler(commands=['novoLembrete']) #Comando /novoLembrete
        def lembrete(message):
    
            lembreteMensagem = {'mensagem' : '','mensagemid':''} #Dicionário para salvar a mensagem do user
    
            lembreteData = {'mensagemData' : '','mensageDataid':''}#Dicionário para salvar a data que o usuário escolheu
    
            lembreteHora = {'mensagemHora' : '','mensageHoraid':''}#Dicionário para salvar a hora que o usuário escolheu
    
            bot.reply_to(message, f"Oque você quer que eu te lembre ?")

            @bot.message_handler(func=lambda message: True)
            def saveLembreteMensagem(message):
    
                if message.id != lembreteMensagem['mensagemid'] and lembreteMensagem['mensagemid'] == '':#Verificando se o usuário enviou uma nova mensagem
    
                    lembreteMensagem['mensagem'] = message.text #salvando texto da mensagem
    
                    lembreteMensagem['mensagemid'] = message.id  #salvando id da mensagem
    
                    bot.reply_to(message, f"Quando você quer que eu te lembre ? DIGITE APENAS A DATA NO FORMATO DD-MM-AA(DIA-MÊS-ANO)") 
    
                else:
    
                    if message.id != lembreteData['mensageDataid'] and lembreteData['mensageDataid'] == '':#verificando se o usuário enviou uma nova data
                        # print(lembreteData['mensagemData'])
                        try:#verificação se a data do usuário ta no padrão
                        
                            testData = datetime.datetime.strptime(message.text,'%d-%m-%Y') #colocando data passada no padrão
                        
                            lembreteData['mensagemData'] = message.text #salvando data
                        
                            lembreteData['mensageDataid'] = message.id #salvando id da mensagem 
                        
                            bot.reply_to(message, f"Que horas ? DIGITE APENAS A HORA NO FORMATO HH:MM(HORA:MINUTOS)")
                            
                        except:#Caso ela não esteja...
                        
                            bot.reply_to(message, f"{message.chat.first_name} sua data <b><i><u>{lembreteData['mensagemData']}</u></i></b> está fora do padrão...\nCaso você discorde digite 'EU DISCORDO' e o caso será verificado.\n/start -Iniciar novamente",parse_mode='HTML')  
                        
                            lembreteMensagem['mensagem'] = ''
                        
                            lembreteMensagem['mensagemid'] = ''
                        
                            lembreteData['mensagemData'] = ''
                        
                            lembreteData['mensageDataid'] = ''
                        
                            lembreteHora['mensageHoraid'] = ''
                        
                            lembreteHora['mensagemHora'] = ''
                    
                    elif message.id != lembreteHora['mensageHoraid'] and lembreteHora['mensageHoraid'] == '' and lembreteData['mensageDataid'] != '':#verificando se o cara enviou um novo horario. So cai aqui se já tiver data
                    
                        try:#verificação se a data + hora se encaixa no padrão
                    
                            datahora = lembreteData['mensagemData'] + f' {message.text}' #concatena data e horario
                    
                            testData = datetime.datetime.strptime(datahora,'%d-%m-%Y %H:%M') #tenta converter pro formato de data do python
                    
                            if testData > datetime.datetime.now(): #verifica se o horario do lembrete é maior que o horario atual 
                    
                                lembreteHora['mensagemHora'] = message.text
                    
                                lembreteHora['mensageHoraid'] = message.id
                    
                                bot.reply_to(message, f"Você quer que eu te lembre o seguinte :\n<b><i><u>{lembreteMensagem['mensagem']}</u></i></b>\nNesse dia aqui\n<b><i><u>{lembreteData['mensagemData']} {lembreteHora['mensagemHora']}</u></i></b>\n Isso mesmo ?\nDIGITE <b><i><u>'SIM'</u></i></b> OU <b><i><u>'NÃO'</u></i></b> ",parse_mode='HTML')
                    
                            else:
                    
                                bot.reply_to(message, f"A data escolhida:\n<b><i><u>{lembreteData['mensagemData']} {message.text}</u></i></b>\n É menor que a data atual que é {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}\n/start -Iniciar novamente\n",parse_mode='HTML')
                    
                                lembreteMensagem['mensagem'] = ''
                    
                                lembreteMensagem['mensagemid'] = ''
                    
                                lembreteData['mensagemData'] = ''
                    
                                lembreteData['mensageDataid'] = ''
                    
                                lembreteHora['mensageHoraid'] = ''
                    
                                lembreteHora['mensagemHora'] = ''
                    
                                pass
                    
                        except:#caso não se encaixe...
                    
                            bot.reply_to(message, f"{message.chat.first_name} sua hora <b><i><u>{lembreteHora['mensagemHora']}</u></i></b> está fora do padrão...\nCaso você discorde digite 'EU DISCORDO' e o caso será verificado.\n/start -Iniciar novamente",parse_mode='HTML')
                    
                            lembreteMensagem['mensagem'] = ''
                    
                            lembreteMensagem['mensagemid'] = ''
                    
                            lembreteData['mensagemData'] = ''
                    
                            lembreteData['mensageDataid'] = ''
                    
                            lembreteHora['mensageHoraid'] = ''
                    
                            lembreteHora['mensagemHora'] = ''  
    
                    elif message.id != lembreteData['mensageDataid'] and lembreteData['mensageDataid'] != '':#So entra aqui depois que o usuário digitar o lembrete, a data e a hora

                        if str(message.text).upper() == 'SIM' or str(message.text).upper() == 'S':#Verifica se o usuário quer salvar a mensagem. No caso de sim

                            bot.reply_to(message, f"Salvando..")

                            try:

                                connection = sqlcon.SlqConection().conecta() #Conecta no banco

                                comands = sqlcomands.SqlCommands()#Instancia objeto de comandos do SQL

                                data = lembreteData['mensagemData'] + ' '+lembreteHora['mensagemHora'] #cria data com data + hora

                                ComandoAdicionaLembrete = comands.addLembrete(message.from_user.id,message.chat.id,lembreteMensagem['mensagem'],data) #monta o comando

                                cursor = connection.cursor() #inicia o cursor

                                cursor.execute(ComandoAdicionaLembrete)#insere lembrete no banco

                                connection.commit()#commita o insert

                                connection.close()#fecha a conexão

                            except Exception as e: #em caso de erro ele zera todos os dicionarios

                                lembreteMensagem['mensagem'] = ''

                                lembreteMensagem['mensagemid'] = ''

                                lembreteData['mensagemData'] = ''

                                lembreteData['mensageDataid'] = ''

                                lembreteHora['mensageHoraid'] = ''

                                lembreteHora['mensagemHora'] = ''

                                pass    

                            lembreteMensagem['mensagem'] = '' #zera todos os dicionarios

                            lembreteMensagem['mensagemid'] = ''

                            lembreteData['mensagemData'] = ''

                            lembreteData['mensageDataid'] = ''

                            lembreteHora['mensageHoraid'] = ''

                            lembreteHora['mensagemHora'] = ''

                            bot.reply_to(message,'Lembrete salvo 🙏🤙✅\n/start -Iniciar novamente"')

                        elif str(message.text).upper() == 'NÃO' or str(message.text).upper() == 'NAO' or str(message.text).upper() == 'N':

                            bot.reply_to(message,"/start -Iniciar novamente")

                            lembreteMensagem['mensagem'] = ''

                            lembreteMensagem['mensagemid'] = ''

                            lembreteData['mensagemData'] = ''

                            lembreteData['mensageDataid'] = ''

                            lembreteHora['mensageHoraid'] = ''

                            lembreteHora['mensagemHora'] = ''

                        else:

                            bot.reply_to(message, f"Desculpe, Não entendi.\n/start -Iniciar novamente")

                            lembreteMensagem['mensagem'] = ''

                            lembreteMensagem['mensagemid'] = ''

                            lembreteData['mensagemData'] = ''

                            lembreteData['mensageDataid'] = ''

                            lembreteHora['mensageHoraid'] = ''

                            lembreteHora['mensagemHora'] = ''

        @bot.message_handler(commands=['verLembretes'])
        def verLembretesSalvos(message):
        
            userid = message.from_user.id
        
            chatid = message.chat.id
        
            try:
        
                connection = sqlcon.SlqConection().conecta() #Conecta no banco
        
                comands = sqlcomands.SqlCommands() #Instancia objeto de comandos do SQL
        
                ComandoRetornaLembretes = comands.getLembretes(userid,chatid) #Monta o comando
        
                cursor = connection.cursor() #Inicia cursor
        
                cursor.execute(ComandoRetornaLembretes)#Executa query
        
                result : list[tuple] = [row for row in cursor.fetchall()]  #cria uma lista com os valores do resultado
        
                columns : list = [column[0] for column in cursor.description] #cria uma lista com as colunas do resultado
        
                strResults = '' #Aqui vão ser salvos todos os resultados
        
                if result: #caso exista algum resultado
        
                    for index in range(len(result)):#para cada resultado complementa a string
        
                        strResults +='<b><i><u>ID</u></i></b>: '+'\n'+ str(result[index][0]) +'\n'+'<b><i><u>Lembrete</u></i></b>: '+'\n'+ result[index][1] + '\n' + '<b><i><u>Data</u></i></b>: '+'\n' + result[index][2] + '\n' + '<b><i><u>Enviado</u></i></b>: '+'\n'+ ('Sim ✅' if result[index][3]  == 1 else 'Não ❌') +'\n-------------------------------\n'
        
                    bot.reply_to(message,strResults + '\n/del + ID - para apagar um Lembrete em específico. Ex: Del 6 : Apaga o Lembrete de ID 6\n/del all - Apaga todos os Lembretes\n/del enviados - Apaga todos os Lembretes já disparados(Os mesmos são apagados automáticamente após 1 dia.)\n/start -Iniciar novamente',parse_mode='HTML')
        
                else:
        
                    bot.reply_to(message,'Não existem lembretes pra você nesse chat\n/start -Iniciar novamente')
                
                connection.commit() #commita conexão
        
                cursor.close() #fecha cursor
        
                connection.close() #fecha conexão

            except Exception as e:

                print(e)

        @bot.message_handler(commands=['del'])
        def deletaLembrete(message):

            userid = message.from_user.id

            chatid = message.chat.id

            connection = sqlcon.SlqConection().conecta() #Conecta no banco

            comands = sqlcomands.SqlCommands()  #Instancia objeto de comandos do SQL

            try:

                arg = message.text.split()[1] #verifica se o cara passou um argumento

                # print(arg)

                try: #verifica se o argumento que ele passou é um inteiro

                    arg = int(arg)

                    ComandoDeletaLembretes = comands.delLembretes(userid,chatid,arg) # monta comando

                    cursor = connection.cursor() #declara cursor

                    cursor.execute(ComandoDeletaLembretes) #tenta deletar o id que ele passou

                    connection.commit() #commita conexao

                    cursor.close() #fechar cursor

                    connection.close() #fecha conexao

                    bot.reply_to(message,f'Caso exista, o lembrete de id {arg} foi apagado.\n/start -Iniciar novamente')

                    arg = '' #zera args

                except:#caso não seja um inteiro

                    if arg.upper() == 'ALL': #caso o user queira apagar todos os lembretes dele no chat

                        ComandoDeletaLembretes = comands.delLembretes(userid,chatid) #monta comando

                        cursor = connection.cursor() #cria cursor 

                        cursor.execute(ComandoDeletaLembretes) #executa o comando

                        connection.commit()#commita a conexao

                        cursor.close()#fecha o cursor

                        connection.close() #fecha a conexao

                        arg = '' #zera os args

                        bot.reply_to(message,'Todos os seus lembretes neste chat foram apagados.\n/start -Iniciar novamente')

                    elif arg.upper() == 'ENVIADOS': #caso o user queira apagar so os que ja foram enviados

                        ComandoDeletaLembretes = comands.delLembretes(userid,chatid,'null',1) #monta comando

                        cursor = connection.cursor() #cria cursor

                        cursor.execute(ComandoDeletaLembretes) #executa cursor

                        connection.commit() #commita conexao

                        cursor.close() #fecha cursor

                        connection.close() #fecha conexao

                        arg = '' #zera args

                        bot.reply_to(message,f'Caso existam, os lembretes que já foram enviados foram apagados\n/start -Iniciar novamente')      

                    else: #se o usuário não passar um argumento conhecido cai aqui

                        bot.reply_to(message, f"Favor passar argumentos válidos\n/del + ID - para apagar um Lembrete em específico. Ex: Del 6 : Apaga o Lembrete de ID 6\n/del all - Apaga todos os Lembretes\n/del enviados - Apaga todos os Lembretes já disparados(Os mesmos são apagados automáticamente após 1 dia.)\n/start -Iniciar novamente")

            except: #se o usuário não passar argumentos cai aqui

                bot.reply_to(message, f"Favor passar argumentos válidos\n/del + ID - para apagar um Lembrete em específico. Ex: Del 6 : Apaga o Lembrete de ID 6\n/del all - Apaga todos os Lembretes\n/del enviados - Apaga todos os Lembretes já disparados(Os mesmos são apagados automáticamente após 1 dia.)\n/start -Iniciar novamente")
            
        def verificaLembretes():

            dataatual = datetime.datetime.now().strftime('%d-%m-%Y %H:%M') #pega data atual
            # print(dataatual)
            connection = sqlcon.SlqConection().conecta() # cria conexao
            
            comands = sqlcomands.SqlCommands() #cria objeto de comando sql
            print(dataatual)
            ComandoverificaLembretes = comands.verificaLembretes(dataatual) #cria o comando
            print(ComandoverificaLembretes)
            cursor = connection.cursor() #cria o cursor
            
            cursor.execute(ComandoverificaLembretes) #executa o cursor
            
            result : list[tuple] = [row for row in cursor.fetchall()] #cria uma lista com os resultados
            
            ids = [] #cria a lista de ids
            
            if result:#se houver um resultado...
    
                for results in result:#para cada resultado

                    id = results[0]

                    ids.append(id) #adiciono o id do resultado na lista pra colocar enviado = 1 depois

                    mensagem = results[1]

                    dataLembrete = results[2]

                    idchat = results[3]

                    bot.send_message(idchat,f'SEGUE O LEMBRETE SOLICITADO!(id do lembrete = {id})\n\n{mensagem}') #envia o lembrete salvo no banco

                    time.sleep(5)

                for id in ids: #para cada id na lista de ids do resultado

                    comands = sqlcomands.SqlCommands() #instancia classe de comando

                    ComandoatualizaLembretesEnviados = comands.atualizaLembretesEnviados(id)#cria comando

                    cursor.execute(ComandoatualizaLembretesEnviados)#executa comando

            connection.commit()#commita conexão

            connection.close()#fecha conexão

        def iniciaScheduler():#task scheduler

            schedule.every().minute.at(":00").do(verificaLembretes) #a cada minuto roda a verificação de lembretes

            while True:

                schedule.run_pending()

                time.sleep(1)
        
        t1 =Thread(target=bot.infinity_polling).start() #cria thread com o bot

        t2 =Thread(target=iniciaScheduler).start() #cria thread com o task scheduler
        
        