class SqlCommands:

    def __init__(self) -> None:
    
        pass

    def addLembrete(self,idUsuario,idChat,Mensagem,dataLembrete) -> str:
        #insere os lembretes
        return f'insert into tb_mensagem_salva(idUsuario,idChat,Mensagem,data_lembrete,enviado) select {idUsuario},{idChat},"{Mensagem}","{dataLembrete}",0'
    
    def getLembretes(self,idUsuario,idChat) -> str:
        #retorna os lembretes
        return f'select id,Mensagem,data_lembrete,enviado from tb_mensagem_salva where idusuario= {idUsuario} and idChat = {idChat}'
    
    def delLembretes(self,idUsuario,idChat,id= 'null',enviado = 'null') -> str:
        #delete os lembretes
        if id == 'null' and enviado == 'null': #deleta todos os lembretes do user
    
            return f'delete from tb_mensagem_salva where idusuario= {idUsuario} and idChat = {idChat}'
        
        elif id == 'null' and enviado != 'null' : #deleta os lembretes enviados
    
            return f'delete from tb_mensagem_salva where idusuario= {idUsuario} and idChat = {idChat} and enviado = 1'
        
        else: #deleta um lembrete especifico
    
            return f'delete from tb_mensagem_salva where idusuario= {idUsuario} and idChat = {idChat} and id = {id}'
    
    def verificaLembretes(self,data):
    
        return f'select id,Mensagem,data_lembrete,idChat from tb_mensagem_salva where  STR_TO_DATE( data_lembrete , "%d-%m-%Y %H:%i" ) <= STR_TO_DATE( "{data}" , "%d-%m-%Y %H:%i" ) and enviado = 0'
    
    def atualizaLembretesEnviados(self,id):
    
        return f'update tb_mensagem_salva set enviado = 1 where id = {id}'
       