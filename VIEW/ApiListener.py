import telebot as telebot
import datetime as datetime
import MODEL.sqlConnection as sqlcon
import MODEL.sqlCommands as sqlcomands
import CONTROLLER.server_config as  ServerConfig
from threading import Thread
import schedule as schedule
import time as time

class ApiTelegramListener:
    def __init__(self) -> None:
        self.__config = ServerConfig.ServerConfig() #faz a leitura das configs
        self.bot = telebot.TeleBot(f"{self.__config.apikey}")
        bot = self.bot
        
    
        @bot.message_handler(commands=['start'])
        def start(message):
            # print(message) 
            bot.reply_to(message, f"Opa {message.chat.first_name}, ta beleza ? Ainda estou em desenvolvimento. Versão atual 0.1\n/novoLembrete - Salva novo lembrete \n/verLembretes - Ver lembretes salvos")

        @bot.message_handler(commands=['novoLembrete'])
        def lembrete(message):
            lembreteMensagem = {'mensagem' : '','mensagemid':''}
            lembreteData = {'mensagemData' : '','mensageDataid':''}
            lembreteHora = {'mensagemHora' : '','mensageHoraid':''}
            bot.reply_to(message, f"Oque você quer que eu te lembre ?")

            @bot.message_handler(func=lambda message: True)
            def saveLembreteMensagem(message):
                if message.id != lembreteMensagem['mensagemid'] and lembreteMensagem['mensagemid'] == '':
                    lembreteMensagem['mensagem'] = message.text
                    lembreteMensagem['mensagemid'] = message.id  
                    bot.reply_to(message, f"Quando você quer que eu te lembre ? DIGITE APENAS A DATA NO FORMATO DD-MM-AA(DIA-MÊS-ANO)") 
                else:
                    if message.id != lembreteData['mensageDataid'] and lembreteData['mensageDataid'] == '':
                        # print(lembreteData['mensagemData'])
                        try:
                            testData = datetime.datetime.strptime(message.text,'%d-%m-%Y')
                            lembreteData['mensagemData'] = message.text
                            lembreteData['mensageDataid'] = message.id
                            bot.reply_to(message, f"Que horas ? DIGITE APENAS A HORA NO FORMATO HH:MM(HORA:MINUTOS)")
                            
                        except:
                            bot.reply_to(message, f"{message.chat.first_name} sua data <b><i><u>{lembreteData['mensagemData']}</u></i></b> está fora do padrão...\nCaso você discorde digite 'EU DISCORDO' e o caso será verificado.\n/start -Iniciar novamente",parse_mode='HTML')  
                            lembreteMensagem['mensagem'] = ''
                            lembreteMensagem['mensagemid'] = ''
                            lembreteData['mensagemData'] = ''
                            lembreteData['mensageDataid'] = ''
                            lembreteHora['mensageHoraid'] = ''
                            lembreteHora['mensagemHora'] = ''
                    elif message.id != lembreteHora['mensageHoraid'] and lembreteHora['mensageHoraid'] == '' and lembreteData['mensageDataid'] != '':
                        try:
                            datahora = lembreteData['mensagemData'] + f' {message.text}'
                            testData = datetime.datetime.strptime(datahora,'%d-%m-%Y %H:%M')
                            if testData > datetime.datetime.now(): 
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
                        except:
                            bot.reply_to(message, f"{message.chat.first_name} sua hora <b><i><u>{lembreteHora['mensagemHora']}</u></i></b> está fora do padrão...\nCaso você discorde digite 'EU DISCORDO' e o caso será verificado.\n/start -Iniciar novamente",parse_mode='HTML')
                            lembreteMensagem['mensagem'] = ''
                            lembreteMensagem['mensagemid'] = ''
                            lembreteData['mensagemData'] = ''
                            lembreteData['mensageDataid'] = ''
                            lembreteHora['mensageHoraid'] = ''
                            lembreteHora['mensagemHora'] = ''  
                        
                    elif message.id != lembreteData['mensageDataid'] and lembreteData['mensageDataid'] != '':
                        if str(message.text).upper() == 'SIM' or str(message.text).upper() == 'S':
                            bot.reply_to(message, f"Salvando..")
                            try:
                                connection = sqlcon.SlqConection().conecta()
                                comands = sqlcomands.SqlCommands()
                                data = lembreteData['mensagemData'] + ' '+lembreteHora['mensagemHora']
                                ComandoAdicionaLembrete = comands.addLembrete(message.from_user.id,message.chat.id,lembreteMensagem['mensagem'],data)
                                cursor = connection.cursor()
                                cursor.execute(ComandoAdicionaLembrete)
                                connection.commit()
                                connection.close()
                            except Exception as e:
                                lembreteMensagem['mensagem'] = ''
                                lembreteMensagem['mensagemid'] = ''
                                lembreteData['mensagemData'] = ''
                                lembreteData['mensageDataid'] = ''
                                lembreteHora['mensageHoraid'] = ''
                                lembreteHora['mensagemHora'] = ''
                                pass    
                            lembreteMensagem['mensagem'] = ''
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
                connection = sqlcon.SlqConection().conecta()
                comands = sqlcomands.SqlCommands()
                ComandoRetornaLembretes = comands.getLembretes(userid,chatid)
                cursor = connection.cursor()
                cursor.execute(ComandoRetornaLembretes)
                result : list[tuple] = [row for row in cursor.fetchall()]  # type: ignore | cria uma lista com os valores do resultado
                columns : list = [column[0] for column in cursor.description] # type: ignore  | cria uma lista com as colunas do resultado
                strResults = ''
                if result: #caso exista algum resultado
                    for index in range(len(result)):
                        strResults +='<b><i><u>ID</u></i></b>: '+'\n'+ str(result[index][0]) +'\n'+'<b><i><u>Lembrete</u></i></b>: '+'\n'+ result[index][1] + '\n' + '<b><i><u>Data</u></i></b>: '+'\n' + result[index][2] + '\n' + '<b><i><u>Enviado</u></i></b>: '+'\n'+ ('Sim ✅' if result[index][3]  == 1 else 'Não ❌') +'\n-------------------------------\n'
                    bot.reply_to(message,strResults + '\n/del + ID - para apagar um Lembrete em específico. Ex: Del 6 : Apaga o Lembrete de ID 6\n/del all - Apaga todos os Lembretes\n/del enviados - Apaga todos os Lembretes já disparados(Os mesmos são apagados automáticamente após 1 dia.)\n/start -Iniciar novamente',parse_mode='HTML')
                else:
                    bot.reply_to(message,'Não existem lembretes pra você nesse chat\n/start -Iniciar novamente')
                
                connection.commit()
                cursor.close()
                connection.close()
                
            except Exception as e:
                print(e)

        @bot.message_handler(commands=['del'])
        def deletaLembrete(message):
            userid = message.from_user.id
            chatid = message.chat.id
            connection = sqlcon.SlqConection().conecta()
            comands = sqlcomands.SqlCommands()
            try:
                arg = message.text.split()[1]
                # print(arg)
                try:
                    arg = int(arg)
                    ComandoDeletaLembretes = comands.delLembretes(userid,chatid,arg)
                    cursor = connection.cursor()
                    cursor.execute(ComandoDeletaLembretes)
                    connection.commit()
                    cursor.close()
                    connection.close()
                    bot.reply_to(message,f'Caso exista, o lembrete de id {arg} foi apagado.\n/start -Iniciar novamente')
                    arg = ''
                except:
                    if arg.upper() == 'ALL':
                        ComandoDeletaLembretes = comands.delLembretes(userid,chatid)
                        cursor = connection.cursor()
                        cursor.execute(ComandoDeletaLembretes)
                        connection.commit()
                        cursor.close()
                        connection.close()
                        arg = ''
                        bot.reply_to(message,'Todos os seus lembretes neste chat foram apagados.\n/start -Iniciar novamente')
                    elif arg.upper() == 'ENVIADOS':
                        ComandoDeletaLembretes = comands.delLembretes(userid,chatid,'null',1)
                        cursor = connection.cursor()
                        cursor.execute(ComandoDeletaLembretes)
                        connection.commit()
                        cursor.close()
                        connection.close()
                        arg = ''
                        bot.reply_to(message,f'Caso existam, os lembretes que já foram enviados foram apagados\n/start -Iniciar novamente')      
                    else:
                        bot.reply_to(message, f"Favor passar argumentos válidos\n/del + ID - para apagar um Lembrete em específico. Ex: Del 6 : Apaga o Lembrete de ID 6\n/del all - Apaga todos os Lembretes\n/del enviados - Apaga todos os Lembretes já disparados(Os mesmos são apagados automáticamente após 1 dia.)\n/start -Iniciar novamente")
            except:
                bot.reply_to(message, f"Favor passar argumentos válidos\n/del + ID - para apagar um Lembrete em específico. Ex: Del 6 : Apaga o Lembrete de ID 6\n/del all - Apaga todos os Lembretes\n/del enviados - Apaga todos os Lembretes já disparados(Os mesmos são apagados automáticamente após 1 dia.)\n/start -Iniciar novamente")
            
        def verificaLembretes():
            dataatual = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')
            # print(dataatual)
            connection = sqlcon.SlqConection().conecta()
            comands = sqlcomands.SqlCommands()
            ComandoverificaLembretes = comands.verificaLembretes(dataatual)
            cursor = connection.cursor()
            cursor.execute(ComandoverificaLembretes)
            result : list[tuple] = [row for row in cursor.fetchall()]
            ids = []
            if result:
                
                for results in result:
                    id = results[0]
                    ids.append(id)
                    mensagem = results[1]
                    dataLembrete = results[2]
                    idchat = results[3]
                    bot.send_message(idchat,f'SEGUE O LEMBRETE SOLICITADO!(id do lembrete = {id})\n\n{mensagem}')
                    time.sleep(5)
                for id in ids:
                    comands = sqlcomands.SqlCommands()
                    ComandoatualizaLembretesEnviados = comands.atualizaLembretesEnviados(id)
                    cursor.execute(ComandoatualizaLembretesEnviados)
            connection.commit()

            connection.close()

        def iniciaScheduler():
            schedule.every().minute.at(":00").do(verificaLembretes)
            while True:
                schedule.run_pending()
                time.sleep(1)
        
        t1 =Thread(target=bot.infinity_polling).start()
        t2 =Thread(target=iniciaScheduler).start()
        
        