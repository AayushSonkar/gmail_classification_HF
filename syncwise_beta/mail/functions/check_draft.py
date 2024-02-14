def check_drafts(creds):

    global dft

    try:
        #Call the Gmail API
        service = build('gmail', 'v1', credentials = creds)

        results = service.users().drafts().list(userId='me' ).execute()
        drafts = results.get('drafts', [])

        draft_count = 0
        for draft in drafts:
            dft = service.users().drafts().get(userId='me', id=draft['id']).execute()
            print(dft["message"])
            draft_count = draft_count + 1
            #change to return statement for GUI 
        print("You have " + str(draft_count) + " drafts.")

    
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")

 