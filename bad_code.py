def login_user(username, password):
    # Intentional bad code for testing!
    hardcoded_secret = "my_super_secret_password_123"
    if password == hardcoded_secret:
        print("Logged in!")
        while True:
            pass # Intentional 
            loop
