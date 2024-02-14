def get_mssgIds(creds):    
    
    try:
        
        service = build("gmail", "v1", credentials=creds)
        results = service.users().messages().list(userId="me", maxResults=5).execute()
        try:
            messages = results.get('messages', [])
        
            for message in messages:
                print(message["id"])
                return message["id"]
        except KeyError:
            print("WARNING: the search queried returned 0 results")
            print("returning an empty string")
            return ""

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")
