import smtplib, ssl
from email.mime.text import MIMEText
from email.utils import formataddr

def download_attachment(msg):
    subject = decode(msg.get('Subject'))  # 获取消息标题
    for part in msg.walk():  # 遍历整个msg的内容
        if part.get_content_disposition() == 'attachment':
            attachment_name = decode(part.get_filename())  # 获取附件名称
            attachment_content = part.get_payload(decode=True)  # 下载附件
            attachment_file = open('./' + attachment_name, 'wb') # 在指定目录下创建文件，注意二进制文件需要用wb模式打开
            attachment_file.write(attachment_content)  # 将附件保存到本地
            attachment_file.close()

def main():
    port = 465  # For SSL
    smtp_server = "smtp.exmail.qq.com"
    sender_email = "hch@smail.nju.edu.cn"
    receiver_email = "786478977@qq.com"
    password = input("Type your password and press enter: ")

    msg = MIMEText('this is just a test', 'plain', 'utf-8')
    msg['From'] = formataddr(["黄春皓", sender_email])
    msg['To'] = formataddr(["test", receiver_email])
    msg['Subject'] = "发送邮件测试"

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

if __name__ == "__main__":
    main()