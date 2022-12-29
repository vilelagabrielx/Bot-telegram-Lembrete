class SqlCommands:
    def __init__(self) -> None:
        pass

    def getLogin(self, login : str) -> str:
        return f'select login,senha from t_login where login = "{login}"'

    def getOrder(self) -> str:
        return 's_verifica_pedidos_on'

    def addLembrete(self,idUsuario,idChat,Mensagem,dataLembrete) -> str:
        return f'insert into tb_mensagem_salva(idUsuario,idChat,Mensagem,data_lembrete) select {idUsuario},{idChat},{Mensagem},{dataLembrete}'