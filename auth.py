import bcrypt
import os

#defining user data file
USER_DATA_FILE = "users.txt"

def hash_password(password_str):
    #encoding password to bytes
    password_bytes = password_str.encode('utf-8')
    #generating salt using bcrypt.gensalt()
    salt = bcrypt.gensalt()
    #hashing password using bcrypt.hashpw()
    password_hash = bcrypt.hashpw(password_bytes, salt)
    #decode the hash back to a string to store in text file
    hashed_str = password_hash.decode('utf-8')
    return hashed_str

def verify_password(password_str, hashed_str):
    #encoding the plaintext password and the stored hash to bytes
    password_bytes = password_str.encode('utf-8')
    password_hash_bytes = hashed_str.encode('utf-8')
    #using bcrypt.checkpw() to verify the password
    return bcrypt.checkpw(password_bytes, password_hash_bytes)

def register_user(username, password):
    #check if username already exists 
    if user_exists(username):
        return False
    #hashing the password
    hashed_password = hash_password(password)
    #appending new user to the file
    with open(USER_DATA_FILE, "a") as f: #if file does not exist then "a" causes python to automatically create the file
        f.write(f"{username},{hashed_password}\n")
    return True

def user_exists(username):
    try:
        with open(USER_DATA_FILE, "r") as f:
            for line in f:
                #removing the newline and making username and password into a list
                stored_username = line.strip().split(",")[0] #[0] selects the username which index 0 from the list
                if stored_username == username:
                    print("Username already exists. Please select another username.")
                    return True
                
    except FileNotFoundError:
        #happens in case when no user has been registered yet
        return False
    return False

def login_user(username, password):
    try:
        with open(USER_DATA_FILE, "r") as f:
            lines = f.readlines() #handling case where no users are registered yet
            if not lines:
                print("No users are registered.")
                return "No users" 
            
            for line in lines:
                stored_username, stored_hash = line.strip().split(",")
                if stored_username == username: #searching for username in file
                    if verify_password(password, stored_hash): #verifying password if username matches
                        return "correct"
                    else:
                        return "wrong"

            return "Username not found."

    except FileNotFoundError:
    #case where username was not found
        return "No users"
    
def validate_username(username):

    if len(username) < 3:
        return False, "Username must be at least 5 characters"
    if len(username) > 20:
        return False, "Username cannot be longer than 20 characters"
    
    return True, ""

def validate_password(password):

    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if len(password) > 50:
        return False, "Password must not be more than 50 characters"
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    return True, ""

def display_menu():
#display the main menu options
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

def main():
    #Main program loop.
    print("\nWelcome to the Week 7 Authentication System!")
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
    
        if choice == '1':
            #registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            #validating username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()
            
            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            # Register the user
            if register_user(username, password):
                print(f"Success: User '{username}' registered successfully!")
            else:
                print("Registration failed: Username already exists.")

        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            # Attempt login
            result = login_user(username, password)

            if result == "correct":
                print(f"\nSuccess, welcome {username}!")
            elif result == "wrong":
                print("Error: Invalid password.")
            elif result == "Username not found.":
                print("Error: Username not found.")
            else:
                print("Error: No users registered.")
       
            input("\nPress Enter to return to main menu...")

        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break
        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()