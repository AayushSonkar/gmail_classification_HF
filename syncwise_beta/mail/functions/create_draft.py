from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def create_draft(creds):
    global crdf

    try:
        #Call the Gmail API
        service = build('gmail', 'v1', credentials = creds)
        mimeMessage = MIMEMultipart()
        mimeMessage['from'] = '11tworldaayush@gmail.com'
        mimeMessage['subject'] ='this is not good'
        mimeMessage['to'] = 'aayush28819@gmail.com'

        msg_body = 'Email Body Testing'
        mimeMessage.attach(MIMEText(msg_body,'plain'))
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
        
        results = service.users().drafts().create(userId = 'me', body = {'message': {'raw':raw_string }}).execute()

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")


