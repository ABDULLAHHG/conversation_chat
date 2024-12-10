from sqlalchemy import create_engine, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
import os
import datetime as dt

from modules.utils.encode_decode import hash_password , check_password

# Load environment variables

# MySQL database connection details
mysql_user = os.getenv("mysql_user")
mysql_password = os.getenv("mysql_password")
mysql_host = os.getenv("mysql_host")
mysql_port = os.getenv("mysql_port")
mysql_database = os.getenv("mysql_database")

# Create MySQL engine and session
mysql_engine = create_engine(f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}')
Session = sessionmaker(bind=mysql_engine)
Base = declarative_base()

def insert_user(username, email , password , phone):
    session = Session()
    try:

        # encrypt the password 
        password = hash_password(password)
        
        new_user = {
            'username': username,
            'email': email,
            'password': password,
            'phone': phone,
        }

        statement = text(
            """INSERT INTO users (username, email, password, phone) 
               VALUES (:username, :email, :password, :phone)"""
        )

        session.execute(statement , new_user )
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error inserting message: {e}")
    finally:
        print("register complete")
        session.close()

def try_to_close_connection(connection):
    try:
        connection.close()
    except Exception as e:
        print(f"Error closing connection: {e}")


def is_username_taken(username):
    """Checks if a username is already in use."""
    session = Session()
    try:
        result = session.execute(text(f"SELECT 1 FROM users WHERE username = '{username}'")).fetchone()
        return result is not None  
    except Exception as e:
        print(f"Error checking username: {e}")
        return False 
    finally:
        session.close()


def is_phone_number_taken(phone_number : str ):
    """Checks if a phone number is already in use."""
    session = Session()
    try:
        result = session.execute(text(f"SELECT 1 FROM users WHERE phone = '{phone_number}'")).fetchone()
        return result is not None
    except Exception as e:
        print(f"Error checking phone number: {e}")
        return False
    finally:
        session.close()


def is_email_taken(email : str):
    """Checks if an email address is already in use."""
    session = Session()
    try:
        result = session.execute(text(f"SELECT 1 FROM users WHERE email = '{email}'")).fetchone()
        return result is not None
    except Exception as e:
        print(f"Error checking email: {e}")
        return False
    finally:
        session.close()



def login(email : str , password : str) -> str | None:
    session = Session()
    try:
        email = session.execute(text("SELECT * FROM users WHERE email = :email"),{"email":email}).fetchone()
        if email:
            if check_password(hashed_password=email.password , password=password):
                return email.username
            else:
                print("Invaild password")
        else:
            print("User not found")
    except Exception as e:
        print(f"Error during Login {e}")
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

def show_messages():
    session = Session()
    try:
        messages = session.execute(text("SELECT * FROM messages")).fetchall()
        if messages:
            for message in messages:
                print(f"Message ID: {message.message_id}")
                print(f"User ID: {message.user_id}")
                print(f"User Name: {message.username}")
                print(f"Message: {message.message}")
                print(f"Is Insult: {message.isInsult}")
                # print(f"Bot Response: {message.bot_response}")
                print("-" * 20)  
        else:
            print("No messages found in the database.")
    except Exception as e:
        print(f"Error retrieving messages: {e}")
    finally:
        session.close()

def show_messages()->None:
    session = Session()
    try:
        messages = session.execute(text("SELECT * FROM messages")).fetchall()
        if messages:
            for message in messages:
                print(f"Message ID: {message.message_id}")
                print(f"User ID: {message.user_id}")
                print(f"User Name: {message.username}")
                print(f"Message: {message.message}")
                print(f"Is Insult: {message.isInsult}")
                # print(f"Bot Response: {message.bot_response}")
                print("-" * 20)  
        else:
            print("No messages found in the database.")
    except Exception as e:
        print(f"Error retrieving messages: {e}")
    finally:
        session.close()


def get_user_conversations(user : str)->list:
    # Establish database connection
    session = Session()

    # SQL query to find which users talk to each other
    query = text("""
    SELECT u1.username AS user1, u2.username AS user2
    FROM conversation_participants cp1
    JOIN conversation_participants cp2 ON cp1.conversation_id = cp2.conversation_id
    JOIN users u1 ON cp1.user_id = u1.user_id
    JOIN users u2 ON cp2.user_id = u2.user_id
    WHERE u1.user_id <> u2.user_id;
    """)

    results = []

    try:
        session.execute(query)
        results = session.fetchall()
        
    except session.connector.Error as err:
        print(f"Error: {err}")
        
    finally:
        session.close()

    return results

def get_user_contacts(username: str) -> list:
    # Establish database connection
    session = Session()

    # SQL query to find contacts and their corresponding conversation IDs for the specified user
    query = text("""
    SELECT DISTINCT 
        u.username, 
        c.conversation_id
    FROM conversations c
    JOIN users u ON (u.user_id = c.user1_id OR u.user_id = c.user2_id)
    WHERE (c.user1_id = (SELECT user_id FROM users WHERE username = :username) 
           OR c.user2_id = (SELECT user_id FROM users WHERE username = :username))
    AND u.username <> :username;
    """)

    results = []

    try:
        result = session.execute(query, {'username': username})
        # Collect username and conversation_id pairs
        results = [{'username': row.username, 'conversation_id': row.conversation_id} for row in result]
        
    except Exception as err:
        print(f"Error: {err}")
        
    finally:
        session.close()

    return results


def create_conversation_with_user(username: str, current_user: str):
    session = Session()
    try:
        # Step 1: Get user IDs for both users
        user_id_query = "SELECT user_id FROM users WHERE username = :username"
        current_user_id = session.execute(text(user_id_query), {'username': current_user}).scalar()
        user_id = session.execute(text(user_id_query), {'username': username}).scalar()

        if not current_user_id or not user_id:
            raise ValueError("One or both users do not exist")

        # Step 2: Check if a conversation already exists between these users
        existing_conversation_query = """
            SELECT c.conversation_id
            FROM conversations c
            WHERE (c.user1_id = :current_user_id AND c.user2_id = :user_id)
            OR (c.user1_id = :user_id AND c.user2_id = :current_user_id);
        """

        existing_conversation = session.execute(
            text(existing_conversation_query),
            {'current_user_id': current_user_id, 'user_id': user_id}
        ).scalar()

        if existing_conversation:
            print(f"Conversation already exists with ID: {existing_conversation}")
            return existing_conversation

        # Step 3: Create a new conversation if none exists
        # Ensure user1_id is always less than user2_id for consistent uniqueness
        user1_id, user2_id = sorted([current_user_id, user_id])

        session.execute(
            text("INSERT INTO conversations (user1_id, user2_id) VALUES (:user1_id, :user2_id)"),
            {'user1_id': user1_id, 'user2_id': user2_id}
        )
        session.commit()

        # Step 4: Get the new conversation ID
        conversation_id = session.execute(text("SELECT LAST_INSERT_ID()")).scalar()

        print(f"New conversation created with ID: {conversation_id}")
        return conversation_id

    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

       
def insert_message(conversation_id, sender_id, message):
    """Insert a message into the messages table."""
    session = Session()
    try:
        insert_query = text("""
            INSERT INTO messages (conversation_id, sender_id, message)
            VALUES (:conversation_id, :sender_id, :message)
        """)
        session.execute(insert_query, {
            'conversation_id': conversation_id,
            'sender_id': sender_id,
            'message': message
        })
        session.commit()
        return True
    except Exception as err:
        session.rollback()
        print(f"Error inserting message: {err}")
        return False
    finally:
        session.close()

def get_messages(conversation_id):
    """Retrieve messages for a specific conversation."""
    session = Session()
    try:
        query = text("""
            SELECT m.message_id, m.sender_id, m.message, m.timestamp
            FROM messages m
            WHERE m.conversation_id = :conversation_id
            ORDER BY m.timestamp ASC
        """)
        result = session.execute(query, {'conversation_id': conversation_id})
        messages = [{
            "message_id": row.message_id,
            "sender_id": row.sender_id,
            "message": row.message,
            "timestamp": row.timestamp.isoformat()
        } for row in result]
        return messages
    except Exception as err:
        print(f"Error retrieving messages: {err}")
        return []
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

def get_last_messages_for_user(user_id):
    """
    Retrieves the last message sent to a specified user, including sender username and timestamp.

    Args:
        user_id: The ID of the user to retrieve messages for.

    Returns:
        A list of dictionaries, where each dictionary represents a last message with 
        'username', 'message', and 'timestamp' keys. Returns an empty list if no messages are found or an error occurs.
    """
        # Corrected SQL query with parameters
    query = text("""
        SELECT
            u.username,
            m.message,
            m.timestamp,
            m.conversation_id
        FROM users u
        JOIN (
            SELECT
                m1.conversation_id,
                m1.sender_id,
                m1.message,
                m1.timestamp
            FROM messages m1
            JOIN (
                SELECT conversation_id, MAX(timestamp) as max_timestamp
                FROM messages
                WHERE conversation_id IN (SELECT conversation_id FROM conversations WHERE user1_id = :user_id OR user2_id = :user_id)
                GROUP BY conversation_id
            ) m2 ON m1.conversation_id = m2.conversation_id AND m1.timestamp = m2.max_timestamp
        ) m ON u.user_id = m.sender_id
        ORDER BY m.timestamp DESC;  -- Added ORDER BY clause
    """)
    
    session = Session()
    try:
        result = session.execute(query, {"user_id": user_id}).fetchall()

        last_messages = [{
            "username": row.username,
            "message": row.message,
            "timestamp": row.timestamp,
            "conversation_id": row.conversation_id
        } for row in result]
        return last_messages

    except SQLAlchemyError as e:
        print(f"Error retrieving last messages: {e}")
        return []
    finally:
        session.close()
