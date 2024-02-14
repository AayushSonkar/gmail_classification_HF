def check_mail(creds):

    global msg

    try:
        #Call the Gmail API
        service = build('gmail', 'v1', credentials = creds)

        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread", maxResults = 5 ).execute()
        messages = results.get('messages', [])

        if not messages:
            print("you have no new messages")
        else:
            message_count = 0
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                
                message_count = message_count + 1
                #change to return statement for GUI 
            print("You have " + str(message_count) + " unread messages.")

            new_message_choice = input("Would youb like to see your unread messages:").lower()
            #Comment all below for GUI
            if new_message_choice == "yes" or "y":
                for message in messages:
                    msg = service.users().messages().get(userId='me', id=message['id']).execute()
                    email_data = msg['payload']['headers']
                    
                    for values in email_data:
                
                        name = values["name"]
                        
                        if name == "From":
                            print("k")
                            from_name = values["value"]
                            print("You have a new message from: "+ from_name)
                            print(msg['snippet'] + "...")
                            print("\n")
                            time.sleep(1)

            else:
                print("Good-Bye_____:)")

    
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")

 