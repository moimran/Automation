import win32com.client

class OutlookClient:

    def __init__(self):
        self.outlook = win32com.client.Dispatch("Outlook.Application")
        self.session = self.outlook.GetNamespace('MAPI')

    def send_message(self, to, subject, body):
        mail = self.outlook.CreateItem(0)
        mail.Recipients.Add(to)
        mail.Subject = subject
        mail.Body = body
        mail.Send()

    def send_message_attach(self, to, body, subject, attach_files):
        mail = self.outlook.CreateItem(0)
        mail.Recipients.Add(to)
        mail.Subject = subject
        mail.Body = body
        print(attach_files)
        for attach in attach_files:
            mail.Attachments.Add(attach)
        mail.Send()

if __name__ == "__main__":
    body = 'This email alert is auto generated. Please do not respond.'
    to = 'postme.imran@gmail.com'
    subject = 'from python'
    mail = OutlookClient()
    mail.send_message(to , subject, body)
