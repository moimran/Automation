import os,time
import win32com.client

class Utility:
    email_outlook = win32com.client.Dispatch("Outlook.Application")

    @staticmethod
    def find_latest_file(path):
        files = (fle for rt, _, f in os.walk(path) for fle in f if time.time() - os.stat(os.path.join(rt, fle)).st_mtime < 120)
        return list(files)

    @staticmethod
    def send_message(to, subject, body):
        mail = outlook.CreateItem(0)
        mail.Recipients.Add(to)
        mail.Subject = subject
        mail.Body = body
        mail.Send()

    @staticmethod
    def send_message_attach(to, body, subject, attach_files):
        mail = Utility.email_outlook.CreateItem(0)
        mail.Recipients.Add(to)
        mail.Subject = subject
        mail.Body = body
        for attach in attach_files:
            mail.Attachments.Add(attach)
        #mail.Send()
        mail.Display(True)

    @staticmethod
    def send_email(config):
        to_email, body, subject = config.email_data
        file_list = Utility.find_latest_file(config.get_show_output_path)
        file_path_list = []
        for file_path in file_list:
            file_path_list.append('{}/{}'.format(config.get_show_output_path,file_path))
        Utility.send_message_attach(to_email, body, subject, file_path_list)


if __name__ == "__main__":
    Utility.find_latest_file('C:/Users/imran.mohammed/PycharmProjects/Automation/configfiles/showoutput')