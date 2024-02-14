

import os.path
import time
import base64 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import torch
from transformers import AutoModel, AutoTokenizer
from datasets import load_dataset
from torch.utils.data import DataLoader, TensorDataset
mail_data = { 'from': [], 'snippet': [],'topic': [], }

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://mail.google.com/"]

def get_authentication():

  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "./syncwise_beta/mail/storage/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  return creds


def check_mail(creds):
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        # Get unread messages
        
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread", maxResults=500).execute()
        messages = results.get('messages', [])

        if not messages:
            print("You have no new messages")
        else:
            print(f"You have {len(messages)} unread messages.")
            no_mssg = input("Enter the number of unread messages you want to view ")
            new_message_choice = "y"
            if new_message_choice.startswith("y"):
                mss_count = 0
                for message in messages[:min(25, int(no_mssg))]:
                    mss_count += 1
                    msg = service.users().messages().get(userId='me', id=message['id']).execute()
                    email_data = msg['payload']['headers']

                    for values in email_data:
                        if values["name"] == "From":
                            from_name = values["value"]
                            
                            time.sleep(1)
                            mail_data["from"].append({from_name})
                            mail_data["snippet"].append(msg['snippet'])
                            mail_data['topic'].append((classify(str(mail_data['snippet']))))


            else:
                print("Good-Bye:)")

    except HttpError as error:
        # TODO(developer) - Handle errors from Gmail API.
        print(f"An error occurred: {error}")



def main():
    creds = get_authentication()
    #print( "Email : " + get_profile(creds))
    check_mail(creds)
    for i, (sender, content, topic) in enumerate(zip(mail_data['from'], mail_data['snippet'], mail_data['topic'])):
      print(f"\nNumber - {i+1}")
      print(f"From: {list(sender)[0]}")
      print(f"Content: {content}")
      print(f"Topic: {topic}")



if __name__ == "__main__":
    main()