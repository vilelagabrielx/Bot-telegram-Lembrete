import telebot as telebot
import datetime as datetime
import MODEL.sqlConnection as sqlcon
import MODEL.sqlCommands as sqlcomands
bot = telebot.TeleBot("5699376581:AAE4oP3RuikBSsIleFAuTg2mR7gxmKkNb-c")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # print(message)
    bot.reply_to(message, f"Opa {message.chat.first_name}, ta beleza ? Ainda estou em desenvolvimento. Versão atual 0.1\n /novoLembrete - Salva novo lembrete")

@bot.message_handler(commands=['novoLembrete'])
def send_welcome(message):
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
                    try:
                        connection = sqlcon.SlqConection().conecta()
                        comands = sqlcomands.SqlCommands()
                        data = lembreteData['mensagemData'] + ' '+lembreteHora['mensagemHora']
                        ComandoAdicionaLembrete = comands.addLembrete(message.from_user.id,message.chat.id,lembreteMensagem['mensagem'],data)
                        cursor = connection.cursor()
                        cursor.execute(ComandoAdicionaLembrete)
                        print('deu bom')
                    except Exception as e:
                        print('deu ruim')
                        print(e)
                        pass    
                    bot.reply_to(message, f"Salvando..")
                    lembreteMensagem['mensagem'] = ''
                    lembreteMensagem['mensagemid'] = ''
                    lembreteData['mensagemData'] = ''
                    lembreteData['mensageDataid'] = ''
                    lembreteHora['mensageHoraid'] = ''
                    lembreteHora['mensagemHora'] = ''
                    pass
                elif str(message.text).upper() == 'NÃO' or str(message.text).upper() == 'NAO' or str(message.text).upper() == 'N':
                    lembreteMensagem['mensagem'] = ''
                    lembreteMensagem['mensagemid'] = ''
                    lembreteData['mensagemData'] = ''
                    lembreteData['mensageDataid'] = ''
                    lembreteHora['mensageHoraid'] = ''
                    lembreteHora['mensagemHora'] = ''
                else:
                    bot.reply_to(message, f"Desculpe, Não entendi.")
                    lembreteMensagem['mensagem'] = ''
                    lembreteMensagem['mensagemid'] = ''
                    lembreteData['mensagemData'] = ''
                    lembreteData['mensageDataid'] = ''
                    lembreteHora['mensageHoraid'] = ''
                    lembreteHora['mensagemHora'] = ''
                    # bot.reply_to(message,"gdfhgfgdfhgj")
                

bot.infinity_polling()