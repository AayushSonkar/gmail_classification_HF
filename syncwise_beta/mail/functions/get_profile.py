def get_profile(creds):
    try:
        service = build("gmail", "v1", credentials = creds)
        results = service.users().getProfile(userId = 'me').execute()
        
        print("Email-Id :")
        print(results)
    
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")