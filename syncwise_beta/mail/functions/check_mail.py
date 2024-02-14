def check_mail(creds):
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        # Get unread messages
        no_mssg = int(input("Enter the amount of messages you want to see (max 25): "))
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread", maxResults=100).execute()
        messages = results.get('messages', [])

        if not messages:
            print("You have no new messages")
        else:
            print(f"You have {len(messages)} unread messages.")

            new_message_choice = input("Would you like to see your unread messages: ").lower()

            if new_message_choice.startswith("y"):
                mss_count = 0
                for message in messages[:min(25, no_mssg)]:
                    mss_count += 1
                    msg = service.users().messages().get(userId='me', id=message['id']).execute()
                    email_data = msg['payload']['headers']

                    for values in email_data:
                        if values["name"] == "From":
                            from_name = values["value"]
                            print(f"You have a new message from: {from_name}")
                            print(msg['snippet'] + "...")
                            print("\n")
                            time.sleep(1)
                            


            else:
                print("Good-Bye_____:)")

    except HttpError as error:
        # TODO(developer) - Handle errors from Gmail API.
        print(f"An error occurred: {error}")