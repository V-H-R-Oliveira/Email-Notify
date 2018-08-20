import imaplib
import email
from bs4 import BeautifulSoup

class EmailNotify(object):
    def __init__(self, login, senha):
        self.setLogin(login)
        self.setSenha(senha)
        self.__server = "imap.gmail.com"
        self.__port = 993

    def setLogin(self, login):
        self.__login = login

    def getLogin(self):
        return self.__login

    def setSenha(self, senha):
        self.__senha = senha

    def getSenha(self):
        return self.__senha

    def conectar(self):
        try:
            mail = imaplib.IMAP4_SSL(self.__server, self.__port)
            mail.login(self.getLogin(), self.getSenha())
            return mail
        except (ConnectionError, OSError) as err:
            print(err)

    def notify(self):
        mail = self.conectar()
        mail.select('inbox')
        resultado, dados = mail.search(None, 'UNSEEN')

        if resultado == 'OK':
            lista_inbox = dados[0].split()

            if len(lista_inbox) == 0:
                print("Não existem novos emails")
                return 0
            print("Emails não lidos:", len(lista_inbox))

            for dado in lista_inbox:
                result, dta = mail.fetch(str.encode(str(int(dado))), "(RFC822)")
                raw_email = dta[0][1].decode('utf-8')
                email_message = email.message_from_string(raw_email)
                remetente = email_message['From']
                destinatario = email_message['To']
                assunto = email_message['Subject']
                c = 1

                for part in email_message.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue

                    filename = part.get_filename()
                    if not filename:
                        ext = 'html'
                        filename = 'msg-part-%08d%s' %(c, ext)
                    c += 1

                print("Remetente:", remetente)
                print("Destinatário:", destinatario)
                print('Assunto:', assunto)
                op = input('Deseja exibir o conteúdo da msg?:').lower()
                if op == 's' or op == 'y':
                    html_ = part.get_payload()
                    soup = BeautifulSoup(html_, "lxml")
                    print('Corpo da mensagem:', soup.get_text())
                else:
                    pass