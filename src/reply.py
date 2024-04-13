import smtplib, ssl, getpass, re, shutil
from email.message import EmailMessage
from email.utils import formataddr
from os import listdir
from os.path import isfile, join

port = 465  # For SSL
smtp_server = "smtp.exmail.qq.com"
my_email = "hch@smail.nju.edu.cn"
receiver_email_suffix = "@smail.nju.edu.cn"
password = getpass.getpass(prompt="Type your password and press enter: ")
attachment_folder = "D:\\离散作业\\toMail"
move_to_folder = "D:\\离散作业"

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(my_email, password)

    for filename in listdir(attachment_folder):
        file_full_path = join(attachment_folder, filename)
        if isfile(file_full_path) and filename[-4:] == '.pdf':
            match = re.match(r'([\u4e00-\u9fa5]+)(\d+)(A)(\d+)(\.pdf)', filename)
            if match is None:
                continue
            student_name, student_id, _, assignment_id, _ = match.groups()
            receiver_email = student_id + receiver_email_suffix

            # Create the email message
            msg = EmailMessage()
            msg['Subject'] = 'Re:离散作业 ' + filename[:-4]
            msg['From'] = formataddr(["黄春皓", my_email])
            msg['To'] = formataddr([student_name, receiver_email])
            # msg.set_content('中文测试This is the body of the email中文测试.')

            with open(file_full_path, 'rb') as file:
                msg.add_attachment(file.read(), maintype='application', subtype='pdf', filename=filename)

            server.sendmail(my_email, receiver_email, msg.as_string())
            shutil.move(file_full_path, move_to_folder + '\\A' + assignment_id + '\\' + filename)
            print(student_name, student_id, 'A' + assignment_id, 'delivered')

