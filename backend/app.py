from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps 
import datetime 
import jwt 
import os 

from modules.register import register 
from modules.database import update_refresh_token
from modules.login import login 
from modules.database import is_username_taken
from modules.database import get_user_conversations
from modules.database import get_user_contacts
from modules.database import create_conversation_with_user
from modules.database import insert_message
from modules.database import get_messages
from modules.database import get_user_id_by_username
from modules.database import get_last_messages_for_user
from modules.utils.get_private_ip import get_private_ip
from modules.utils.get_private_ip import write_ip_to_file


private_ip = get_private_ip()
write_ip_to_file(private_ip)


app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
CORS(app, resources={r"/*": {"origins": "*"}})

reg = register()
log = login()
refresh_tokens = {}

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json() 
        name = data.get('Name').lower()
        email = data.get('Email').lower()
        phone_number = data.get('Number')
        password = data.get('Password')
        errors = reg.register(name , email , password , phone_number)
        print(errors)

        if not errors:
            return jsonify({'message': 'User registered successfully'}), 201 # 201 Created status code
        else:
            print(errors)
            return jsonify({'errors': errors}), 500
        
    except Exception as e:
        print(f"Error registering user: {e}")
        return jsonify({'error': 'Failed to register user'}), 500
        


def token_required(f):
    @wraps(f)
    def decorated(*args , **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message" : "Token is missing"})
        
        try:
            jwt.decode(token , app.config["SECRET_KEY"] ,algorithms = ["HS256"])
        except Exception as e: 
            return jsonify({"message" : "Token is invalid"})
        return f(*args , **kwargs)
    return decorated


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() 
    print(data["email"] , data["password"])
    username = log.login(data["email"].lower() , data["password"])
    if not username:
        return jsonify({'message': 'Could not verify'}), 401
    
    # create access token 
    access_token = jwt.encode({
        "sub" : username,
        "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    } , app.config["SECRET_KEY"])

    refresh_token = jwt.encode({
        "sub" : username,
        "exp" : datetime.datetime.utcnow() + datetime.timedelta(days = 30)
    }, app.config["SECRET_KEY"])
    update_refresh_token(username = username , new_refresh_token=refresh_token)
    refresh_tokens[refresh_token] = username
    return jsonify({"access_token" : access_token , "refresh_token":refresh_token}), 200


@app.route("/refresh" , methods = ["POST"])
def refresh():
    refresh_token = request.get("refresh_token")
    if not refresh_token or refresh_token not in refresh_tokens:
        return jsonify({"message" : "invalid refresh token!"})
    
    try:
        payload = jwt.decode(refresh_token ,app.config["SECRET_KEY"] , algorithms = ["HS256"])
        username = payload["sub"]

        # create new access token 
        new_access_token = jwt.encode({
            "sub" : username,
            "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config["SECRET_KEY"])
        return jsonify({"access_token":new_access_token})
    
    except jwt.ExpiredSignatureError :
        return jsonify({"message" : "Refresh token expired!"}) , 401
    except jwt.InvalidTokenError:
        return jsonify({"message" : "Invalid refresh token!"}) , 401

@app.route('/protected')
def protected():
    #Add authentication here to check the access token
    token = request.headers.get('Authorization').split()[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        print(payload)
        return jsonify({'protected': "protect" })
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

@app.route('/username')
def username():
    #return username
    token = request.headers.get('Authorization').split()[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        print(payload)
        return jsonify({'username': payload['sub'] })
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
    
    
@app.route('/check_username', methods=['GET'])
def user_conversations():
    # Retrieve the username from the query parameters
    token = request.headers.get('Authorization').split()[1]
    username = find_username(token)
    
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    try:
        conversations = get_user_conversations(username)        
        if conversations is None:
            return jsonify({"error": "No conversations found for this user"}), 404
        
        return jsonify(conversations), 200
    
    except Exception as e:
        print(f"Error retrieving conversations: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    

@app.route('/get_contacts', methods=['POST'])
def user_contacts():
    # Retrieve the username from the query parameters
    token = request.headers.get('Authorization').split()[1]
    username = find_username(token)
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    try:
        contacts = get_user_contacts(username)
        print(contacts)
        
        if not contacts:
            return jsonify({"error": "No contacts found for this user"}), 404
        
        return jsonify(contacts), 200
    
    except Exception as e:
        print(f"Error retrieving contacts: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    



@app.route('/search_user/<username>', methods=['GET'])
def check_username(username):
    # username = request.args.get('username')
    token = request.headers.get('Authorization').split()[1]  # Use headers to retrieve the token

    if not username:
        return jsonify({'exists': False, 'message': 'Username is required'}), 400
    
    current_user = find_username(token)  # This should handle token validation
    if not current_user:
        return jsonify({'exists': False, 'message': 'Invalid token or user not found'}), 401


    exists = is_username_taken(username)
    if exists:

        conversation_id = create_conversation_with_user(username, current_user)
        if conversation_id:
            return jsonify({'exists': True, 'conversation_id': conversation_id}), 200
        else:
            return jsonify({'exists': True, 'message': 'Failed to create conversation'}), 500

    return jsonify({'exists': False}), 200

def find_username(token:str)->str:
    #return username
    try :
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        print(payload)
        return payload['sub']
    except Exception as e:
        print(e)


@app.route('/sendmessage', methods=['POST'])
def send_message():
    data = request.json
    token = request.headers.get('Authorization')  # Get the token from headers
    conversation_id = data.get('conversation_id')
    message_text = data.get('message')

    sender_id = get_user_id_by_username(find_username(token=token))
    print(sender_id)
    print(conversation_id)
    if not message_text or not conversation_id or not sender_id:
        return jsonify({"error": "Message, conversation_id, and sender_id cannot be empty"}), 400

    if insert_message(conversation_id, sender_id, message_text):
        return jsonify({"message": "Message sent successfully"}), 200
    else:
        return jsonify({"error": "Failed to send message"}), 500

@app.route('/receivedmessage', methods=['GET'])
def receive_messages():
    token = request.headers.get('Authorization')  # Get the token from headers
    user_id = get_user_id_by_username(find_username(token=token))
    conversation_id = request.args.get('conversation_id')
    if not conversation_id:
        return jsonify({"error": "conversation_id cannot be empty"}), 400

    messages = get_messages(conversation_id)
    for message in messages:
        message["current_user_id"] = user_id

    print(messages)
    if messages or isinstance(messages , list):
        return jsonify(messages), 200
    else:
        return jsonify({"error": "Failed to retrieve messages"}), 500

@app.route('/get_communication_history', methods=['GET'])
def get_communication_history():
    """
    Retrieves the last message for each conversation involving the authenticated user.
    """
    try:
        token = request.headers.get('Authorization').split()[1]  # Get the token from headers
        user_id = get_user_id_by_username(find_username(token=token)) # Get the user ID from the JWT payload
        print(user_id)
        # Assuming get_last_messages_for_user returns a list of dictionaries
        last_messages = get_last_messages_for_user(user_id)

        return jsonify(last_messages), 200

    except Exception as e:
        print(f"Error in get_communication_history: {e}")
        return jsonify({"error": "Failed to retrieve communication history"}), 500


if __name__ == '__main__':
    app.run(host = "0.0.0.0" , debug=True)


    

    