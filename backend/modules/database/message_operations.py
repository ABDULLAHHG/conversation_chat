from sqlalchemy.sql import text
from . import Session

def insert_message(conversation_id, sender_id, message):
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

def get_last_messages_for_user(user_id):
    session = Session()
    try:
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
            ORDER BY m.timestamp DESC;
        """)
        result = session.execute(query, {"user_id": user_id}).fetchall()
        last_messages = [{
            "username": row.username,
            "message": row.message,
            "timestamp": row.timestamp,
            "conversation_id": row.conversation_id
        } for row in result]
        return last_messages
    except Exception as e:
        print(f"Error retrieving last messages: {e}")
        return []
    finally:
        session.close()