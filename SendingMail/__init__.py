from DbReader import AdminDbReader
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from string import Template
import sys
sys.path.append('./')


class MaillingService():
    def __init__(self):
        pass

    def read_template(self):
        filename = './file-templates/EmailTemplate.txt'
        with open(filename, 'r', encoding='utf-8') as template_file:
            template_file_content = template_file.read()
        return Template(template_file_content)

    def send_mail(self, dest_email, dbname, felink, belink, npmpackage, npmpackageid = ''):
        s = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
        s.ehlo()
        s.login('easywebnotification@gmail.com', 'hoangvuong1999')

        msg = MIMEMultipart()
        message_template = self.read_template()
        message = message_template.substitute(
            dbName=dbname, feLink=felink, beLink=belink, npmLink=npmpackage, npmPackageId=npmpackageid)
        msg['From'] = 'EasyWeb Notification System'
        msg['To'] = dest_email
        msg['Subject'] = "EasyWeb - Your website is ready"
        msg.attach(MIMEText(message, 'plain'))
        s.send_message(msg)
        del msg

    def send_result(self, dbguid, apilink, npmpackage='', clientapplink='', npmpackageid=''):
        email, dbName, beLink, feLink = AdminDbReader().get_email_of_user_by_db_guid(dbguid)
        if email != None:
            self.send_mail(email, dbName, clientapplink, apilink, npmpackage, npmpackageid)