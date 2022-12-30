import telebot as telebot
import datetime as datetime
import MODEL.sqlConnection as sqlcon
import MODEL.sqlCommands as sqlcomands
import CONTROLLER.server_config as  ServerConfig

class ApiTelegramListener:
    def __init__(self) -> None:
        self.__config = ServerConfig.ServerConfig() #faz a leitura das configs
        self.bot = telebot.TeleBot(f"{self.__config.apikey}")
        bot = self.bot
        
    
        @bot.message_handler(commands=['start'])
        def start(message):
            # print(message)
            bot.reply_to(message, f"Opa {message.chat.first_name}, ta beleza ? Ainda estou em desenvolvimento. Versão atual 0.1\n /novoLembrete - Salva novo lembrete")

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
                        print(lembreteData['mensagemData'])
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
                                data = lembreteData['mensagemData'] + ' '+lembreteHora['mensagemHora'] + ':00'
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
                     
        bot.infinity_polling()