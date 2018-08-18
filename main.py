from getpass import getpass
from emailNotify import EmailNotify

email = input('Digite o seu email: ')
senha = getpass(prompt='Digite sua senha: ')

newInstance = EmailNotify(email, senha)
newInstance.conectar()
newInstance.notify()
