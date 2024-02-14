from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
# Create your views here.
from asgiref.sync import sync_to_async

#--------------------GMAIL--------------------------------
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


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://mail.google.com/"]
mail_data = {"from": [], "content": [], "topic": []}
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
          "./mail/storage/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  return creds



def check_mail(creds):
    mail_data_check = {"from": [], "content": [], "topic": []}  # Initialize mail_data

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
            #no_mssg = input("Enter the number of unread messages you want to read ")
            no_mssg = 10
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
                            mail_data_check["from"].append(from_name)
                            mail_data_check["content"].append(msg['snippet'])
                            mail_data_check["topic"].append(classify(str(msg['snippet'])))  # Assuming classify is a function to determine the topic

            else:
                print("Good-Bye:)")
    except HttpError as error:
        # TODO(developer) - Handle errors from Gmail API.
        print(f"An error occurred: {error}")

    return mail_data_check  # Return the mail_data dictionary

from transformers import pipeline

def classify(prompt):
    pipe = pipeline("text-classification", model="cardiffnlp/tweet-topic-21-multi")
    returned = pipe(prompt)[0]['label']
    return (returned)
#---------------------------------------------------------



def index(request):
    return render(request, 'core/index.html')



def go_syncwise(request):
    # Assume you have some data to populate the table
    creds = get_authentication()
    #print( "Email : " + get_profile(creds))
    
    mail_data = check_mail(creds) # Get the mail
    # Return the data as JSON response
    return JsonResponse({"result": mail_data})

