import bcrypt
import time
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


def check_password_strength(password):

    is_too_short = False
    is_medium_length = False
    is_long_enough = False
    has_ucase = False
    has_lcase = False
    has_digit = False
    has_special = False
    is_common = False
    common_password = ['password', '123456', '123456789', 'qwerty', 'abc123', '111111', '123123', 'letmein', 'iloveyou', 'admin', 'welcome', 'monkey', 'dragon', 'football', 'sunshine', 'princess', 'baseball', 'password1', 'superman', 'qwerty123']
    special_char = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '[', ']', '{', '}', ';', ':', ',', '.', '<', '>', '/', '?', '|', '`', '~']

    #for loop to check type of letter in the password using string methods
    for x in password:
        if x.isupper():
            has_ucase = True
        elif x.islower():
            has_lcase = True
        elif x.isdigit():
            has_digit = True

    #comparing password to a generated list of 20 common passwords
    for y in common_password:
        if y == password:
            is_common = True

    #checking password length
    if (len(password) > 7) and (len(password) < 10):
        is_too_short = True
    elif (len(password) > 9) and (len(password) < 13): 
        is_medium_length = True
    else:
        is_long_enough = True 

    #checking if there are special characters in the password
    for z in password:
        if z in special_char:
            has_special = True

    #checking types of characters in password to determine strength of password
    char_types = has_ucase + has_lcase + has_digit + has_special

    if is_common:
        return "Weak (common password)"
    
    if is_too_short or char_types <= 1:
        return "Weak"
    
    if is_medium_length and char_types >= 2:
        return "Medium"
    
    if is_long_enough and char_types >= 4:
        return "Strong"

    return "Medium"


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

            #checking password strength
            password_strength = check_password_strength(password)
            print(password_strength)

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