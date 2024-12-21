from sqlalchemy.sql import text
from . import Session

def create_conversation_with_user(username, current_user):
    session = Session()
    try:
        user_id_query = "SELECT user_id FROM users WHERE username = :username"
        current_user_id = session.execute(text(user_id_query), {'username': current_user}).scalar()
        user_id = session.execute(text(user_id_query), {'username': username}).scalar()

        if not current_user_id or not user_id:
            raise ValueError("One or both users do not exist")

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

        user1_id, user2_id = sorted([current_user_id, user_id])
        session.execute(
            text("INSERT INTO conversations (user1_id, user2_id) VALUES (:user1_id, :user2_id)"),
            {'user1_id': user1_id, 'user2_id': user2_id}
        )
        session.commit()
        conversation_id = session.execute(text("SELECT LAST_INSERT_ID()")).scalar()
        print(f"New conversation created with ID: {conversation_id}")
        return conversation_id

    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

def get_messages_from_conversation_id(conversation_id):
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


### idk where should i put them 


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
