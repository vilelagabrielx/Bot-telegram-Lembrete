from mysql.connector import connect
from CONTROLLER.server_config import ServerConfig
from mysql.connector import CMySQLConnection,MySQLConnection


class SlqConection:
    def __init__(self) -> None:
        self.__config = ServerConfig() #faz a leitura das configs do server de banco de dados
        

    def conecta(self) -> CMySQLConnection | MySQLConnection:
        return connect( #retorna uma conexão com a connection string abaixo
            host=self.__config.host, 
            user=self.__config.user, 
            password=self.__config.password, 
            database=self.__config.database
        )