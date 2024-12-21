from . import Session
from sqlalchemy.sql import text
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


def get_user_id_by_username(username):
    """Retrieve user_id from the users table based on the username."""
    session = Session()
    try:
        query = text("""
            SELECT user_id 
            FROM users 
            WHERE username = :username
        """)
        result = session.execute(query, {'username': username}).fetchone()

        if result:
            return result.user_id  # Return the user_id if found
        else:
            return None  # Return None if the username does not exist

    except Exception as err:
        print(f"Error retrieving user_id: {err}")
        return None  # Return None in case of an error

    finally:
        session.close()