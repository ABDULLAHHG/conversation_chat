from modules.utils.encode_decode import hash_password, check_password
from sqlalchemy.sql import text
from . import Session

def insert_user(username, email, password, phone):
    session = Session()
    try:
        password = hash_password(password)  # Encrypt the password
        new_user = {
            'username': username,
            'email': email,
            'password': password,
            'phone': phone,
        }
        statement = text("""INSERT INTO users (username, email, password, phone) 
                            VALUES (:username, :email, :password, :phone)""")
        session.execute(statement, new_user)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error inserting user: {e}")
    finally:
        print("Register complete")
        session.close()

def is_username_taken(username):
    session = Session()
    try:
        result = session.execute(text("SELECT 1 FROM users WHERE username = :username"), {"username": username}).fetchone()
        return result is not None
    except Exception as e:
        print(f"Error checking username: {e}")
        return False
    finally:
        session.close()

def is_email_taken(email):
    session = Session()
    try:
        result = session.execute(text("SELECT 1 FROM users WHERE email = :email"), {"email": email}).fetchone()
        return result is not None
    except Exception as e:
        print(f"Error checking email: {e}")
        return False
    finally:
        session.close()

def is_phone_number_taken(phone_number):
    session = Session()
    try:
        result = session.execute(text("SELECT 1 FROM users WHERE phone = :phone_number"), {"phone_number": phone_number}).fetchone()
        return result is not None
    except Exception as e:
        print(f"Error checking phone number: {e}")
        return False
    finally:
        session.close()

def login(email, password):
    session = Session()
    try:
        user = session.execute(text("SELECT * FROM users WHERE email = :email"), {"email": email}).fetchone()
        if user:
            if check_password(hashed_password=user.password, password=password):
                return user.username
            else:
                print("Invalid password")
        else:
            print("User not found")
    except Exception as e:
        print(f"Error during login: {e}")
    finally:
        session.close()


def update_refresh_token(username : str , new_refresh_token : str)-> None:
    session = Session()
    try: 
        query = "UPDATE users SET refresh_token = :refresh_token WHERE username = :username" 
        session.execute(text(query),{"refresh_token":new_refresh_token , "username":username})
        session.commit()
    except Exception as e:
        print(f"The Error is {e}")
    finally:
        session.close()
