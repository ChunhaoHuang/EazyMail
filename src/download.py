import imaplib, email, getpass, modified_utf7, os, re
from email.header import decode_header

imap_server = 'imap.exmail.qq.com'
my_email = 'hch@smail.nju.edu.cn'
password = getpass.getpass(prompt="Type your password and press enter: ")
folder_name = '其他文件夹/离散作业'
save_path = "D:\\离散作业"

with imaplib.IMAP4_SSL(imap_server) as server:
    server.login(my_email, password)

    # list all folders:
    # for i in server.list()[1]:
    #     l = modified_utf7.decode_modified_utf7(i).split(' "/" ')
    #     print(l[0] + " = " + l[1])
    
    server.select(modified_utf7.encode_modified_utf7(folder_name))
    status, response = server.search(None, 'UNSEEN')
    if status != 'OK':
        print("No unseen emails found.")
        exit()
    for id in response[0].split():
        # Fetch the email by its ID (RFC822 format for full email)
        status, data = server.fetch(id, '(RFC822)')
        raw_email = data[0][1]

        # Parse the email content
        email_message = email.message_from_bytes(raw_email)

        # get subject (no need temporarily)
        # subject, sub_charset = decode_header(email_message.get('Subject'))[0]
        # if sub_charset != None:
        #     subject = subject.decode(sub_charset)
        
        for part in email_message.walk():
            content_disposition = part.get("Content-Disposition")
            # Check for attachment in the part
            if part.get_content_maintype() == 'multipart' or content_disposition is None:
                continue
            filename = part.get_filename()
            if filename:
                filename, filename_charset = decode_header(filename)[0]
                if filename_charset != None:
                    filename = filename.decode(filename_charset)
                while filename[-4:] == '.pdf':
                    filename = filename[:-4]
                match = re.match(r'(.*)(A)(\d+)', filename)
                if match is None:
                    continue
                n = match.groups()[2]
                save_path_w = save_path + '\\A' + n
                filename += '.pdf'
                # Save the attachment to a file
                if not os.path.exists(save_path_w):
                    os.makedirs(save_path_w)
                with open(os.path.join(save_path_w, filename), 'wb') as f:
                    f.write(part.get_payload(decode=True))
                print(filename + " downloaded")
        server.store(id, '+FLAGS', '\Seen')