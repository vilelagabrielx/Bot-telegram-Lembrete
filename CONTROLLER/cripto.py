from cryptography.fernet import Fernet

class Cripto:
    def __init__(self) -> None:
        
        self.__KEY : str = 'zUN8HANMfa1njXCCfPpcvMkqfeFyrAdlgGS0ay19mS8=' #chave secreta utilizada atualmente

        self.__fernet = Fernet(self.__KEY) #Instancia a classe de criptografia com a chave

    def encriptar(self, object : bytes) -> bytes: #função de criptografar 
        return self.__fernet.encrypt(object)

    def decriptar(self, object : bytes) -> bytes: #função de decriptografar
        return self.__fernet.decrypt(object)

# print(Cripto().encriptar(b'129.148.45.165'))