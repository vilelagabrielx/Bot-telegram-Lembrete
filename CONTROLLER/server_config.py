from json import load
from CONTROLLER.cripto import Cripto



class ServerConfig:

    def __init__(self) -> None:

        self.__encoding : str = 'utf-8' #json está em utf8 e será aberto na linha debaixo

        self.__JSON : dict[str, str] = load(open('./MODEL/server-config.json', mode='r', encoding='utf-8')) #abre o json de conexão

        self.__CRIPTO = Cripto(self.__JSON['criptokey']) #instancia o objeto de criptografia

        self.apikey = self.__JSON['apikey'] #key da API do telegram 

        self.host : str = self.__CRIPTO.decriptar( #decripta a conexão
    
            bytes(self.__JSON['host'], self.__encoding)
    
        ).decode(self.__encoding)

        self.user : str = self.__CRIPTO.decriptar( #decripta o user
    
            bytes(self.__JSON['user'], self.__encoding)
    
        ).decode(self.__encoding)

        self.password : str = self.__CRIPTO.decriptar( #decripta a senha
    
            bytes(self.__JSON['password'], self.__encoding)
    
        ).decode(self.__encoding)

        self.database : str = self.__CRIPTO.decriptar( #decripta o database
    
            bytes(self.__JSON['database'], self.__encoding)
    
        ).decode(self.__encoding)

    