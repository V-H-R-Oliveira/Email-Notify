import imaplib
import email
from bs4 import BeautifulSoup

class EmailNotify(object):
    def __init__(self, login, senha):
        self.login = login
        self.senha = senha
        self.server = "imap.gmail.com"
        self.port = 993

    def __repr__(self):
        return "Login: {}\nSenha: {}".format(self.login, self.senha)

    def conectar(self):
        try:
            mail = imaplib.IMAP4_SSL(self.server, self.port)
            mail.login(self.login, self.senha)
            return mail
        except ConnectionError as err:
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
                    soup = BeautifulSoup(html_, "html.parser")
                    body = soup.get_text()
                    print('Corpo da mensagem:', body)
                else:
                    pass