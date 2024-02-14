def search_messages(creds, search_string):
    
    try:
        service = build("gmail", "v1", credentials = creds)
        results = service.users().messages().list(userId ='me', q=search_string).execute()
        try:
            messages = results.get('messages', [])
            print(messages)
        except KeyError:
            print("WARNING: the search queried returned 0 results")
            print("returning an empty string")
            return ""
    except (errors.HttpError, error):
        print("An error occured: %s") % error

